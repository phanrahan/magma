import ast
import enum
import textwrap
import inspect
from functools import wraps
import functools
import operator
from collections import namedtuple
import os

import six
from . import cache_definition
from .common import deprecated, setattrs, Stack, OrderedIdentitySet
from .interface import *
from .wire import *
from .config import get_debug_mode
from .debug import get_callee_frame_info, debug_info
from .logging import root_logger
from .is_definition import isdefinition
from .placer import Placer, StagedPlacer
from magma.syntax.combinational import combinational
from magma.syntax.sequential import sequential
from magma.syntax.verilog import combinational_to_verilog, \
    sequential_to_verilog
from .view import PortView
from magma.protocol_type import MagmaProtocol

__all__ = ['AnonymousCircuitType']
__all__ += ['AnonymousCircuit']

__all__ += ['CircuitType']
__all__ += ['Circuit']
__all__ += ['DeclareCircuit']
__all__ += ['DefineCircuit', 'EndDefine', 'EndCircuit']
__all__ += ['DefineCircuitKind']

__all__ += ['CopyInstance']
__all__ += ['circuit_type_method']
__all__ += ['circuit_generator']
__all__ += ['CircuitBuilder', 'builder_method']

circuit_type_method = namedtuple('circuit_type_method', ['name', 'definition'])

_logger = root_logger()

_VERILOG_FILE_OPEN = """
integer \_file_{filename} ;
initial \_file_{filename} = $fopen(\"{filename}\", \"{mode}\");
"""  # noqa

_VERILOG_FILE_CLOSE = """
final $fclose(\_file_{filename} );
"""  # noqa

_DEFAULT_VERILOG_LOG_STR = f"""
`ifndef MAGMA_LOG_LEVEL
    `define MAGMA_LOG_LEVEL 1
`endif"""


class _SyntaxStyle(enum.Enum):
    NONE = enum.auto()
    OLD = enum.auto()
    NEW = enum.auto()


class DefinitionContext:
    def __init__(self, placer):
        self.placer = placer
        self._inline_verilog = []
        self._displays = []
        self._insert_default_log_level = False
        self._files = []
        self._builders = []

    def add_builder(self, builder):
        self._builders.append(builder)

    def add_file(self, file):
        self._files.append(file)

    def _finalize_file_opens(self):
        for file in self._files:
            self.add_inline_verilog(
                _VERILOG_FILE_OPEN.format(filename=file.filename,
                                          mode=file.mode),
                {}, {})

    def _finalize_file_close(self):
        for file in self._files:
            self.add_inline_verilog(
                _VERILOG_FILE_CLOSE.format(filename=file.filename),
                {}, {})

    def add_inline_verilog(self, format_str, format_args, symbol_table):
        self._inline_verilog.append((format_str, format_args, symbol_table))

    def insert_default_log_level(self):
        self._insert_default_log_level = True

    def add_display(self, display):
        self._displays.append(display)

    def _finalize_displays(self):
        for display in self._displays:
            self.add_inline_verilog(*display.get_inline_verilog())

    def finalize(self, defn):
        self.placer = self.placer.finalize(defn)
        for builder in self._builders:
            inst = builder.finalize()
            self.placer.place(inst)
        if self._insert_default_log_level:
            self.add_inline_verilog(_DEFAULT_VERILOG_LOG_STR, {}, {})
        self._finalize_file_opens()  # so displays can refer to open files
        self._finalize_displays()
        self._finalize_file_close()  # close after displays


_definition_context_stack = Stack()


class _DefinitionContextManager:
    def __init__(self, context):
        self._context = context

    def __enter__(self):
        _definition_context_stack.push(self._context)

    def __exit__(self, typ, value, traceback):
        _definition_context_stack.pop()


def _has_definition(cls, port=None):
    if cls.instances:
        return True
    if cls._context_._inline_verilog:
        return True
    if port is None:
        interface = getattr(cls, "interface", None)
        if not interface:
            return False
        return any(_has_definition(cls, p) for p in interface.ports.values())
    flat = port.flatten()
    return any(not f.is_output() and f.value() is not None for f in flat)


def _get_interface_type(cls):
    if hasattr(cls, "IO") and hasattr(cls, "io"):
        _logger.warning("'IO' and 'io' should not both be specified, ignoring "
                        "'io'", debug_info=cls.debug_info)
    # TODO(setaluri): Simplify this logic and remove InterfaceKind check
    # (this is a artifact of the circuit_generator decorator).
    if hasattr(cls, 'IO'):
        cls._syntax_style_ = _SyntaxStyle.OLD
        _logger.warning("'IO = [...]' syntax is deprecated, use "
                        "'io = IO(...)' syntax instead",
                        debug_info=cls.debug_info)
        if isinstance(cls.IO, InterfaceKind):
            return None
        return make_interface(*cls.IO)
    if hasattr(cls, "io"):
        cls._syntax_style_ = _SyntaxStyle.NEW
        return cls.io.make_interface()
    return None


def _add_intermediate_value(value):
    """
    Add an intermediate value `value` to `values`, handling members of
    recursive types.  Used by `_get_intermediate_values` as part of
    `CircuitKind.__repr__`.
    """
    root = value.name.root()
    if root is None or root.const():
        return OrderedIdentitySet()
    return OrderedIdentitySet((root,))


def _get_intermediate_values(value):
    """
    Retrieve the intermediate values connected to `value` and put them into
    `values`

    Used in the implementation of `CircuitKind.__repr__` to emit the temporary
    values in a circuit.
    """
    if value.is_output():
        return OrderedIdentitySet()
    if value.is_mixed():
        # Mixed
        return functools.reduce(operator.or_,
                                (_get_intermediate_values(v) for v in value),
                                OrderedIdentitySet())
    driver = value.value()
    if driver is None:
        return OrderedIdentitySet()
    flat = value.flatten()
    if len(flat) > 1 and driver.name.anon():
        return functools.reduce(operator.or_,
                                (_get_intermediate_values(f) for f in flat),
                                OrderedIdentitySet())
    values = OrderedIdentitySet()
    while driver is not None:
        values |= _add_intermediate_value(driver)
        if not driver.is_input():
            break
        value = driver
        driver = driver.value()
    return values


class CircuitKind(type):
    def __prepare__(name, bases, **kwargs):
        context = DefinitionContext(StagedPlacer(name))
        _definition_context_stack.push(context)
        return type.__prepare__(name, bases, **kwargs)

    """Metaclass for creating circuits."""
    def __new__(metacls, name, bases, dct):
        # Override class name if supplied (and save class name).
        cls_name = dct.get("_cls_name_", name)
        name = dct.setdefault('name', name)

        dct.setdefault('renamed_ports', {})
        dct.setdefault('primitive', False)
        dct.setdefault('coreir_lib', 'global')
        dct.setdefault("inline_verilog_strs", [])
        dct["inline_verilog_generated"] = False
        dct["bind_modules"] = {}
        dct["bind_modules_bound"] = False

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
        cls._syntax_style_ = _SyntaxStyle.NONE
        IO = _get_interface_type(cls)
        if IO is not None:
            cls.IO = IO
            cls.interface = cls.IO(defn=cls, renamed_ports=dct["renamed_ports"])
            setattrs(cls, cls.interface.ports, lambda k, v: isinstance(k, str))
        try:
            context = _definition_context_stack.pop()
            assert context.placer.name == cls_name
            # Override staged context with '_context_' from namespace if
            # available.
            cls._context_ = dct.get("_context_", context)
            cls._context_.finalize(cls)
        except IndexError:  # no staged placer
            cls._context_ = DefinitionContext(Placer(cls))

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

        if not isdefinition(cls):
            return f"{name} = DeclareCircuit(\"{name}\", {args})"
        s = f"{name} = DefineCircuit(\"{name}\", {args})\n"
        sorted_instances = sorted(cls.instances, key=lambda x: x.name)

        values = []
        for instance in sorted_instances:
            values.extend(list(instance.interface.ports.values()))
        values.extend(cls.interface.ports.values())
        intermediate_values = (_get_intermediate_values(value)
                               for value in values)
        intermediate_values = functools.reduce(operator.or_,
                                               intermediate_values,
                                               OrderedIdentitySet())
        if intermediate_values:
            intermediate_values = (f"{value.name} = {repr(value)}"
                                   for value in intermediate_values)
            s += "\n".join(intermediate_values) + "\n"
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

    @deprecated(msg="cls.inline_verilog is deprecated, use m.inline_verilog"
                "instead")
    def inline_verilog(cls, inline_str, **kwargs):
        cls._context_.add_inline_verilog(inline_str, kwargs, None)


@six.add_metaclass(CircuitKind)
class AnonymousCircuitType(object):
    """Abstract base class for circuits"""
    def __init__(self, *largs, **kwargs):
        self.kwargs = dict(**kwargs)

        if "debug_info" in self.kwargs:
            # Not an instance parameter, internal debug argument.
            del self.kwargs["debug_info"]

        if hasattr(self, 'default_kwargs'):
            for key, value in self.default_kwargs.items():
                self.kwargs.setdefault(key, value)

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
        if isinstance(output, MagmaProtocol):
            output = output._get_magma_value_()
        # Wire the output to this circuit's input (should only have 1 input).
        inputs = []
        for inp in self.interface.inputs():
            if isinstance(inp, MagmaProtocol):
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
        setattrs(self, interface.ports, lambda k, v: isinstance(k, str))
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

    @classmethod
    def open(cls):
        return _DefinitionContextManager(cls._context_)


def AnonymousCircuit(*decl):
    """
    AnonymousCircuits are like macros - the circuit instances are not placed
    """
    if len(decl) == 1:
        decl = decl[0]
    return AnonymousCircuitType().setinterface(AnonymousInterface(decl))


class CircuitType(AnonymousCircuitType):
    """Placed circuit - instances placed in a definition"""
    def __init__(self, *largs, **kwargs):
        super(CircuitType, self).__init__(*largs, **kwargs)
        try:
            context = _definition_context_stack.peek()
            context.placer.place(self)
        except IndexError:  # instances must happen inside a definition context
            raise Exception("Can not instance a circuit outside a definition")

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


@deprecated(
    msg="DeclareCircuit factory method is deprecated, subclass Circuit instead")
def DeclareCircuit(name, *decl, **args):
    """DeclareCircuit Factory"""
    debug_info = None
    if get_debug_mode():
        debug_info = get_callee_frame_info()
    metacls = CircuitKind
    bases = (CircuitType,)
    dct = metacls.__prepare__(name, bases)
    dct.update(dict(IO=decl,
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
                    renamed_ports=args.get('renamed_ports', {})))
    return metacls(name, bases, dct)


class DefineCircuitKind(CircuitKind):
    def __new__(metacls, name, bases, dct):
        dct["_cls_name_"] = name  # save original name for debugging purposes
        if 'name' not in dct:
            dct['name'] = name
            # Check if we are a subclass of something other than Circuit; if so,
            # inherit the name of the first parent.
            for base in bases:
                if base is Circuit:
                    continue
                if not issubclass(base, AnonymousCircuitType):
                    raise Exception(f"Must subclass from AnonymousCircuitType "
                                    f"or a subclass of AnonymousCircuitType "
                                    f"({base})")
                dct['name'] = base.name
                break
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

        has_definition = _has_definition(self)
        self._is_definition = dct.get('is_definition', has_definition)
        self.is_instance = False

        run_unconnected_check = False
        if hasattr(self, "definition"):
            if self._syntax_style_ is _SyntaxStyle.OLD:
                _logger.warning("'definition' class method syntax is "
                                "deprecated, use inline definition syntax "
                                "instead", debug_info=self.debug_info)
                with _DefinitionContextManager(self._context_):
                    self.definition()
                self._is_definition = True
                run_unconnected_check = True
            elif self._syntax_style_ is _SyntaxStyle.NEW:
                _logger.warning("Supplying method 'definition' with new inline "
                                "definition syntax is not supported, ignoring "
                                "'definition'")
        run_unconnected_check = run_unconnected_check or (
            has_definition and self._syntax_style_ is _SyntaxStyle.NEW)
        run_unconnected_check = run_unconnected_check and not \
            dct.get("_ignore_undriven_", False)
        if run_unconnected_check:
            self.check_unconnected()

        return self

    def check_unconnected(self):
        for port in self.interface.inputs():
            if not port.driven():
                msg = f"Output port {self.name}.{port.name} not driven"
                _logger.error(msg, debug_info=self.debug_info)

        for inst in self.instances:
            for port in inst.interface.inputs():
                if not port.driven():
                    msg = f"Input port {inst.name}.{port.name} not driven"
                    _logger.error(msg, debug_info=inst.debug_info)

    @property
    def is_definition(self):
        return self._is_definition or self.verilog or self.verilogFile

    @property
    def instances(self):
        return self._context_.placer.instances()

    def place(cls, inst):
        """Place a circuit instance in this definition"""
        cls._context_.placer.place(inst)

    def bind(cls, monitor, *args):
        cls.bind_modules[monitor] = args


@six.add_metaclass(DefineCircuitKind)
class Circuit(CircuitType):
    pass


@deprecated(
    msg="DefineCircuit factory method is deprecated, subclass Circuit instead")
def DefineCircuit(name, *decl, **args):
    """DefineCircuit Factory"""
    debug_info = None
    if get_debug_mode():
        debug_info = get_callee_frame_info()
    metacls = DefineCircuitKind
    bases = (Circuit,)
    dct = metacls.__prepare__(name, bases)
    dct.update(dict(IO=decl,
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
                    kratos=args.get("kratos", None)))
    defn = metacls(name, bases, dct)
    _definition_context_stack.push(defn._context_)
    return defn


def EndDefine():
    try:
        context = _definition_context_stack.pop()
    except IndexError:
        raise Exception("EndDefine not matched to DefineCircuit")
    placer = context.placer
    placer._defn.check_unconnected()
    debug_info = get_callee_frame_info()
    placer._defn.end_circuit_filename = debug_info[0]
    placer._defn.end_circuit_lineno = debug_info[1]


EndCircuit = EndDefine


def CopyInstance(instance):
    circuit = type(instance)
    new_instance = circuit()
    new_instance.kwargs = instance.kwargs
    return new_instance


_GeneratorArguments = namedtuple('GeneratorArguments', ['args', 'kwargs'])


@deprecated(msg="circuit_generator decorator is deprecated, subclass Generator "
            "instead")
def circuit_generator(func):
    @cache_definition
    @wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        # Store arguments to generate the circuit.
        result._generator_arguments = _GeneratorArguments(args, kwargs)
        return result
    return wrapped


coreir_port_mapping = {
    "I": "in",
    "I0": "in0",
    "I1": "in1",
    "O": "out",
    "S": "sel",
    "CLK": "clk",
}


def DeclareCoreirCircuit(*args, **kwargs):
    return DeclareCircuit(*args, **kwargs,
                          renamed_ports=coreir_port_mapping)


class _CircuitBuilderMeta(type):
    pass


def builder_method(func):

    @wraps(func)
    def _wrapped(this, *args, **kwargs):
        with _DefinitionContextManager(this._context):
            result = func(this, *args, **kwargs)
        return result

    return _wrapped


class CircuitBuilder(metaclass=_CircuitBuilderMeta):
    _RESERVED_NAMESPACE_KEYS = {"io", "_context_", "name"}

    def __init__(self, name):
        try:
            context = _definition_context_stack.peek()
            context.add_builder(self)
        except IndexError:
            raise Exception("Can not instance a circuit builder outside a "
                            "definition")
        self._name = name
        self._io = SingletonInstanceIO()
        self._finalized = False
        self._dct = {}
        self._context = DefinitionContext(StagedPlacer(self._name))

    def _port(self, name):
        return self._io.ports[name]

    def _add_port(self, name, typ):
        self._io.add(name, typ)
        setattr(self, name, self._io.inst_ports[name])

    def _set_namespace_key(self, key, value):
        if key in CircuitBuilder._RESERVED_NAMESPACE_KEYS:
            raise Exception(f"Can not set reserved namespace key '{key}'")
        self._dct[key] = value

    def _finalize(self):
        pass

    def finalize(self):
        if self._finalized:
            raise Exception("Can only call finalize on a CircuitBuilder once")
        self._finalize()
        bases = (AnonymousCircuitType,)
        dct = {"io": self._io, "_context_": self._context, "name": self._name}
        dct.update(self._dct)
        DefineCircuitKind.__prepare__(self._name, bases)
        t = DefineCircuitKind(self._name, bases, dct)
        self._finalized = True
        return t(name=self._name)
