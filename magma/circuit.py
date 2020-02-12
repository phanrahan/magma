import ast
import textwrap
import inspect
from functools import wraps
from collections import namedtuple, Counter
import os

import six
from .config import get_compile_dir, set_compile_dir
# TODO: Remove circular dependency required for `circuit.bind` logic
import magma as m
from . import cache_definition
from .clock import ClockTypes
from .interface import *
from .wire import *
from .config import get_debug_mode
from .debug import get_callee_frame_info, debug_info
from .logging import root_logger
from .is_definition import isdefinition
from .ref import AnonRef
from .array import Array
from .tuple import Tuple
from magma.syntax.combinational import combinational
from magma.syntax.sequential import sequential
from magma.syntax.verilog import combinational_to_verilog, \
    sequential_to_verilog
from magma.verilog_utils import value_to_verilog_name
from magma.view import InstView, PortView

__all__ = ['AnonymousCircuitType']
__all__ += ['AnonymousCircuit']

__all__ += ['CircuitType']
__all__ += ['Circuit']
__all__ += ['DeclareCircuit']
__all__ += ['DefineCircuit', 'EndDefine', 'EndCircuit']

__all__ += ['CopyInstance']
__all__ += ['circuit_type_method']
__all__ += ['circuit_generator']

circuit_type_method = namedtuple('circuit_type_method', ['name', 'definition'])

_logger = root_logger()


# Maintain a stack of nested definitions.
class _DefinitionBlock:
    __stack = []

    def __init__(self, defn):
        self.__defn = defn

    def __enter__(self):
        _DefinitionBlock.push(self.__defn)

    def __exit__(self, typ, value, traceback):
        _DefinitionBlock.pop()

    @classmethod
    def push(cls, defn):
        cls.__stack.append(defn)

    @classmethod
    def pop(cls):
        if not cls.__stack:
            return None
        return cls.__stack.pop()

    @classmethod
    def peek(cls):
        if not cls.__stack:
            return None
        return cls.__stack[-1]


def _setattrs(obj, dct):
    for k, v in dct.items():
        if isinstance(k, str):
            setattr(obj, k, v)


class CircuitKind(type):
    """Metaclass for creating circuits."""
    def __new__(metacls, name, bases, dct):
        # Override class name if supplied.
        name = dct.setdefault('name', name)

        dct.setdefault('renamed_ports', {})
        dct.setdefault('primitive', False)
        dct.setdefault('coreir_lib', 'global')
        dct["inline_verilog_strs"] = []
        dct["bind_modules"] = {}

        # If in debug_mode is active and debug_info is not supplied, attach
        # callee stack info.
        dct.setdefault("debug_info", None)
        if get_debug_mode() and not dct["debug_info"]:
            callee_frame = inspect.getframeinfo(
                inspect.currentframe().f_back.f_back)
            module = inspect.getmodule(inspect.stack()[2][0])
            dct["debug_info"] = debug_info(callee_frame.filename,
                                           callee_frame.lineno, module)

        cls = type.__new__(metacls, name, bases, dct)

        for method in dct.get('circuit_type_methods', []):
            setattr(cls, method.name, method.definition)

        # Create interface for this circuit class.
        if hasattr(cls, 'IO') and not isinstance(cls.IO, InterfaceKind):
            cls.IO = DeclareInterface(*cls.IO)
            cls.interface = cls.IO(defn=cls,
                                   renamed_ports=dct["renamed_ports"])
            _setattrs(cls, cls.interface.ports)

        return cls

    def __call__(cls, *largs, **kwargs):
        if get_debug_mode():
            debug_info = get_callee_frame_info()
            kwargs["debug_info"] = debug_info
        self = super(CircuitKind, cls).__call__(*largs, **kwargs)
        if hasattr(cls, 'IO'):
            interface = cls.IO(inst=self, renamed_ports=cls.renamed_ports)
            self.setinterface(interface)
        return self

    def __str__(cls):
        interface = ""
        if hasattr(cls, "interface"):
            interface = ", ".join(f"{name}: {_type}"
                                  for name, _type in cls.interface.items())
            interface = f"({interface})"
        return f"{cls.__name__}{interface}"

    def __repr__(cls):
        if not hasattr(cls, 'IO'):
            return super().__repr__()

        name = cls.__name__
        args = str(cls.IO)

        if not hasattr(cls, "instances"):
            return f"{name} = DeclareCircuit(\"{name}\", {args})"
        s = f"{name} = DefineCircuit(\"{name}\", {args})\n"
        sorted_instances = sorted(cls.instances, key=lambda x: x.name)
        # Emit instances.
        for instance in sorted_instances:
            s += repr(instance) + '\n'
        # Emit wires from instances.
        for instance in sorted_instances:
            s += repr(instance.interface)
        s += repr(cls.interface)
        s += "EndCircuit()"
        return s

    def rename(cls, new_name):
        if cls.verilogFile:
            raise Exception("Can not rename a verilog wrapped file")

        old_name = cls.name
        cls.name = new_name
        cls.coreir_name = new_name
        cls.verilog_name = new_name
        cls.__name__ = new_name

        # NOTE(rsetaluri): This is a very hacky way to try to rename wrapped
        # verilog. We simply replace the first instance of "module <old_name>"
        # with "module <new_name>". This ignores the possibility of "module
        # <new_name>" existing anywhere else, most likely in comments etc. The
        # more robust way to do this would to modify the AST directly and
        # generate the new verilog code.
        #
        # Instead, at the top of this function, we raise an exception for
        # verilog wrapped files. That is, for now it is considered an error to
        # try to rename a verilog wrapped circuit.
        if cls.verilogFile:
            find_str = f"module {old_name}"
            replace_str = f"module {new_name}"
            assert cls.verilogFile.find(find_str) != -1
            cls.verilogFile = cls.verilogFile.replace(find_str, replace_str, 1)

    def find(cls, defn):
        name = cls.__name__
        if not isdefinition(cls):
            return defn
        for i in cls.instances:
            type(i).find(defn)
        if name not in defn:
            defn[name] = cls
        return defn

    def inline_verilog(cls, inline_str, **kwargs):
        format_args = {}
        for key, arg in kwargs.items():
            if isinstance(arg, m.Type):
                arg = value_to_verilog_name(arg)
            elif isinstance(arg, PortView):
                arg = value_to_verilog_name(arg)
            format_args[key] = arg
        cls.inline_verilog_strs.append(
            inline_str.format(**format_args))


@six.add_metaclass(CircuitKind)
class AnonymousCircuitType(object):
    """Abstract base class for circuits"""
    def __init__(self, *largs, **kwargs):
        self.kwargs = dict(**kwargs)

        if "debug_info" in self.kwargs:
            # Not an instance parameter, internal debug argument.
            del self.kwargs["debug_info"]

        if hasattr(self, 'default_kwargs'):
            for key in self.default_kwargs:
                if key not in kwargs:
                    self.kwargs[key] = self.default_kwargs[key]

        self.name = kwargs['name'] if 'name' in kwargs else ""
        self.loc = kwargs['loc'] if 'loc' in kwargs else None
        if self.loc and len(self.loc) == 2:
            self.loc = (self.loc[0], self.loc[1], 0)
        self.interface = None
        self.defn = None
        self.used = False
        self.is_instance = True
        self.debug_info = kwargs.get("debug_info", None)

    def set_debug_info(self, debug_info):
        self.debug_info = debug_info

    def __str__(self):
        if self.name:
            return f"{self.name}<{type(self)}>"
        name = f"AnonymousCircuitInst{id(self)}"
        interface = ", ".join(f"{name}: {type(value)}"
                              for name, value in self.interface.ports.items())
        return f"{name}<{interface}>"

    def __repr__(self):
        args = []
        for k, v in self.interface.ports.items():
            args.append(f"\"{k}\"")
            args.append(repr(v))
        args = ", ".join(args)
        typ = type(self).__name__
        if self.name:
            return f"{self.name} = {typ}({args})"
        return f"{typ}({args})"

    def __getitem__(self, key):
        return self.interface[key]

    def wireoutputs(self, outputs, debug_info):
        """Wire a list of outputs to the circuit's inputs"""
        inputs = self.interface.inputs()
        ni = len(inputs)
        no = len(outputs)
        if ni != no:
            msg = (
                f"Number of inputs is not equal to the number of outputs, "
                f"expected {ni} inputs, got {no}. Only {min(ni,no)} will be "
                f"wired.")
            _logger.warning(msg, debug_info=debug_info)
        for i in range(min(ni, no)):
            wire(outputs[i], inputs[i], debug_info)

    def wire(self, output, debug_info):
        """Wire a single output to the circuit's inputs"""
        if hasattr(output, 'interface'):
            # Wire the circuit's outputs to this circuit's inputs.
            self.wireoutputs(output.interface.outputs(), debug_info)
            return
        if isinstance(output, m.MagmaProtocol):
            output = output._get_magma_value_()
        # Wire the output to this circuit's input (should only have 1 input).
        inputs = []
        for inp in self.interface.inputs():
            if isinstance(inp, m.MagmaProtocol):
                inp = inp._get_magma_value_()
            inputs.append(inp)
        ni = len(inputs)
        if ni == 0:
            msg = ("Wiring an output to a circuit with no input arguments, "
                   "skipping")
            _logger.warning(msg, debug_info=debug_info)
            return
        if ni != 1:
            msg = (f"Wiring an output to a circuit with more than one input "
                   f"argument, using the first input {inputs[0].debug_name}")
            _logger.warning(msg, debug_info=debug_info)
        inputs[0].wire(output, debug_info)

    @property
    def debug_name(self):
        defn_str = ""
        if hasattr(self, 'defn') and self.defn is not None:
            defn_str = str(self.defn.name)
        return f"{defn_str}.{self.name}"

    def __call__(input, *outputs, **kw):
        debug_info = None
        if get_debug_mode():
            debug_info = get_callee_frame_info()

        no = len(outputs)
        if len(outputs) == 1:
            input.wire(outputs[0], debug_info)
        elif len(outputs) >= 1:  # In case there are only kw
            input.wireoutputs(outputs, debug_info)

        # Wire up extra arguments, name to name.
        # TODO(rsetaluri): This code should be changed to use clock types.
        for key, value in kw.items():
            if key == 'enable':
                key = 'CE'
            elif key == 'reset':
                key = 'RESET'
            elif key == 'set':
                key = 'SET'  # NYI
            elif key == 'ce':
                key = 'CE'  # deprecated
            if hasattr(input, key):
                i = getattr(input, key)
                wire(value, getattr(input, key), debug_info)
            else:
                msg = f"Instance {input.debug_name} does not have input {key}"
                _logger.warning(msg, debug_info=debug_info)

        o = input.interface.outputs()
        return o[0] if len(o) == 1 else tuple(o)

    def setinterface(self, interface):
        _setattrs(self, interface.ports)
        self.interface = interface
        return self

    def on(self):
        self.used = True
        return self

    def off(self):
        self.used = False
        return self

    def rename(self, name):
        self.name = name
        return self

    def isclocked(self):
        return self.interface.isclocked()

    def clockargs(self):
        return self.interface.clockargs()

    def inputargs(self):
        return self.interface.inputargs()

    def outputargs(self):
        return self.interface.outputargs()


def AnonymousCircuit(*decl):
    """
    AnonymousCircuits are like macros - the circuit instances are not placed
    """
    if len(decl) == 1:
        decl = decl[0]
    return AnonymousCircuitType().setinterface(Interface(decl))


class CircuitType(AnonymousCircuitType):
    """Placed circuit - instances placed in a definition"""
    def __init__(self, *largs, **kwargs):
        super(CircuitType, self).__init__(*largs, **kwargs)
        # Circuit instances are placed if within a definition.
        top = _DefinitionBlock.peek()
        if top:
            top.place(self)

    def __repr__(self):
        args = []
        for k, v in self.kwargs.items():
            if isinstance(v, tuple):
                # {   # Format identifier
                # 0:  # first parameter
                # #   # use "0x" prefix
                # 0   # fill with zeroes
                # {1} # to n characters (including 0x), per the second parameter
                # x   # hexadecimal number, using lowercase letters for a-f
                # }   # End of format identifier
                if len(v) == 2:
                    v = "{0:#0{1}x}".format(v[0], v[1] // 4)
            else:
                v = f"\"{v}\""
            args.append(f"{k}={v}")
        args = ", ".join(args)
        typ = type(self).__name__
        if self.name:
            return f"{self.name} = {typ}({args})"
        return f"{typ}({args})"


def DeclareCircuit(name, *decl, **args):
    """DeclareCircuit Factory"""
    if get_debug_mode():
        debug_info = get_callee_frame_info()
    else:
        debug_info = None
    dct = dict(IO=decl,
               debug_info=debug_info,
               is_definition=False,
               primitive=args.get('primitive', True),
               stateful=args.get('stateful', False),
               simulate=args.get('simulate'),
               firrtl_op=args.get('firrtl_op'),
               circuit_type_methods=args.get('circuit_type_methods', []),
               coreir_lib=args.get('coreir_lib', "global"),
               coreir_name=args.get('coreir_name', name),
               coreir_genargs=args.get('coreir_genargs', None),
               coreir_configargs=args.get('coreir_configargs', {}),
               verilog_name=args.get('verilog_name', name),
               default_kwargs=args.get('default_kwargs', {}),
               renamed_ports=args.get('renamed_ports', {}))
    return CircuitKind(name, (CircuitType, ), dct)


class DefineCircuitKind(CircuitKind):
    def __new__(metacls, name, bases, dct):
        if 'name' not in dct:
            # Check if we are a subclass of something other than Circuit.
            for base in bases:
                if base is not Circuit:
                    if not issubclass(base, Circuit):
                        raise Exception(f"Must subclass from Circuit or a "
                                        f"subclass of Circuit. {base}")
                    # If so, we will inherit the name of the first parent.
                    dct['name'] = base.name
                    break
            else:
                dct['name'] = name
        name = dct['name']
        dct["renamed_ports"] = dct.get("renamed_ports", {})

        self = CircuitKind.__new__(metacls, name, bases, dct)

        self.verilog = None
        self.verilogFile = None
        self.verilogLib = None

        self.verilog_name = dct.get('verilog_name', name)
        self.coreir_name = dct.get('coreir_name', name)
        self.coreir_genargs = dct.get('coreir_genargs', None)
        self.coreir_configargs = dct.get('coreir_configargs', {})
        self.default_kwargs = dct.get('default_kwargs', {})
        self.firrtl = None

        self._instances = []
        self.instanced_circuits_counter = Counter()
        self.instance_name_counter = Counter()
        self.instance_name_map = {}
        self._is_definition = dct.get('is_definition', False)
        self.is_instance = False

        if hasattr(self, 'IO'):
            # Create circuit definition.
            if hasattr(self, 'definition'):
                with _DefinitionBlock(self):
                    self.definition()
                    self.check_unconnected()
                    self._is_definition = True

        return self

    def check_unconnected(self):
        for port in self.interface.ports.values():
            if issubclass(type(port), ClockTypes):
                continue
            if port.is_input() and not port.driven():
                msg = f"Output port {self.name}.{port.name} not driven"
                _logger.error(msg, debug_info=self.debug_info)

        for inst in self.instances:
            for port in inst.interface.ports.values():
                if issubclass(type(port), ClockTypes):
                    continue
                if port.is_input() and not port.driven():
                    msg = f"Input port {inst.name}.{port.name} not driven"
                    _logger.error(msg, debug_info=inst.debug_info)

    @property
    def is_definition(self):
        return self._is_definition or self.verilog or self.verilogFile

    @property
    def instances(self):
        return self._instances

    def inspect_name(cls, inst):
        # Try to fetch instance name.
        with open(inst.debug_info.filename, "r") as f:
            line = f.read().splitlines()[inst.debug_info.lineno - 1]
            tree = ast.parse(textwrap.dedent(line)).body[0]
            # Simple case when <Name> = <Instance>().
            if isinstance(tree, ast.Assign) and len(tree.targets) == 1 \
                    and isinstance(tree.targets[0], ast.Name):
                name = tree.targets[0].id
                # Handle case when we've seen a name multiple times (e.g. reused
                # inside a loop).
                if cls.instance_name_counter[name] == 0:
                    inst.name = name
                    cls.instance_name_counter[name] += 1
                else:
                    if cls.instance_name_counter[name] == 1:
                        # Append `_0` to the first instance with this name.
                        orig = cls.instance_name_map[name]
                        orig.name += "_0"
                        del cls.instance_name_map[name]
                        cls.instance_name_map[orig.name] = orig
                    inst.name = f"{name}_{cls.instance_name_counter[name]}"
                    cls.instance_name_counter[name] += 1

    def place(cls, inst):
        """Place a circuit instance in this definition"""
        if not inst.name:
            if get_debug_mode():
                cls.inspect_name(inst)
            if not inst.name:
                # Default name if we could not find one or debug mode is off.
                inst_count = cls.instanced_circuits_counter[type(inst).name]
                inst.name = f"{type(inst).name}_inst{str(inst_count)}"
                cls.instanced_circuits_counter[type(inst).name] += 1
                cls.instance_name_counter[inst.name] += 1
        else:
            cls.instance_name_counter[inst.name] += 1
        for sub_inst in getattr(type(inst), "instances", []):
            setattr(inst, sub_inst.name, InstView(sub_inst, inst))
        cls.instance_name_map[inst.name] = inst
        inst.defn = cls
        if get_debug_mode():
            inst.stack = inspect.stack()
        cls.instances.append(inst)

    def gen_bind_port(cls, mon_arg, bind_arg):
        if isinstance(mon_arg, Tuple) or isinstance(mon_arg, Array) and \
                not issubclass(mon_arg.T, m.Digital):
            result = []
            for child1, child2 in zip(mon_arg, bind_arg):
                result += cls.gen_bind_port(child1, child2)
            return result
        port = value_to_verilog_name(mon_arg)
        arg = value_to_verilog_name(bind_arg)
        return [(f".{port}({arg})")]

    def bind(cls, monitor, *args):
        bind_str = monitor.verilogFile

        ports = []
        for mon_arg, cls_arg in zip(monitor.interface.ports.values(),
                                    cls.interface.ports.values()):
            if str(mon_arg.name) != str(cls_arg.name):
                error_str = f"""
Bind monitor interface does not match circuit interface
    Monitor Ports: {list(monitor.interface.ports)}
    Circuit Ports: {list(cls.interface.ports)}
"""
                raise TypeError(error_str)
            ports += cls.gen_bind_port(mon_arg, cls_arg)
        extra_mon_args = list(
            monitor.interface.ports.values()
        )[len(cls.interface):]
        for mon_arg, bind_arg in zip(extra_mon_args, args):
            ports += cls.gen_bind_port(mon_arg, bind_arg)
        ports_str = ", ".join(ports)
        bind_str = f"bind {cls.name} {monitor.name} {monitor.name}_inst ({ports_str});"  # noqa
        if not os.path.isdir(".magma"):
            os.mkdir(".magma")
        curr_compile_dir = get_compile_dir()
        set_compile_dir("normal")
        # Circular dependency, need coreir backend to compile, backend imports
        # circuit (for wrap casts logic, we might be able to factor that out)
        m.compile(f".magma/{monitor.name}", monitor)
        set_compile_dir(curr_compile_dir)
        with open(f".magma/{monitor.name}.v", "r") as f:
            content = "\n".join((f.read(), bind_str))
        cls.bind_modules[monitor.name] = content


@six.add_metaclass(DefineCircuitKind)
class Circuit(CircuitType):
    pass


def DefineCircuit(name, *decl, **args):
    """DefineCircuit Factory"""
    debug_info = None
    if get_debug_mode():
        debug_info = get_callee_frame_info()
    dct = dict(IO=decl,
               is_definition=True,
               primitive=args.get('primitive', False),
               stateful=args.get('stateful', False),
               simulate=args.get('simulate'),
               debug_info=debug_info,
               verilog_name=args.get('verilog_name', name),
               coreir_name=args.get('coreir_name', name),
               coreir_lib=args.get('coreir_lib', "global"),
               coreir_genargs=args.get('coreir_genargs', None),
               coreir_configargs=args.get('coreir_configargs', None),
               default_kwargs=args.get('default_kwargs', {}),
               renamed_ports=args.get('renamed_ports', {}),
               kratos=args.get("kratos", None))
    defn = DefineCircuitKind(name, (Circuit,), dct)
    _DefinitionBlock.push(defn)
    return defn


def EndDefine():
    top = _DefinitionBlock.pop()
    if not top:
        raise Exception("EndDefine called without DefineCircuit")
    debug_info = get_callee_frame_info()
    top.end_circuit_filename = debug_info[0]
    top.end_circuit_lineno = debug_info[1]


EndCircuit = EndDefine


def CopyInstance(instance):
    circuit = type(instance)
    new_instance = circuit()
    new_instance.kwargs = instance.kwargs
    return new_instance


GeneratorArguments = namedtuple('GeneratorArguments', ['args', 'kwargs'])


def circuit_generator(func):
    @cache_definition
    @wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        # Store arguments to generate the circuit.
        result._generator_arguments = GeneratorArguments(args, kwargs)
        return result
    return wrapped


default_port_mapping = {
    "I": "in",
    "I0": "in0",
    "I1": "in1",
    "O": "out",
    "S": "sel",
    "CLK": "clk",
}


def DeclareCoreirCircuit(*args, **kwargs):
    return DeclareCircuit(*args, **kwargs,
                          renamed_ports=default_port_mapping)
