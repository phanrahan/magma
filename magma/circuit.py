import ast
import enum
import textwrap
import inspect
import itertools
from functools import wraps
import functools
import operator
from collections import namedtuple, Counter, UserDict
import os
from typing import Callable, Dict, List, Union

from . import cache_definition
from .common import deprecated, setattrs, OrderedIdentitySet
from .interface import *
from .wire import *
from .config import get_debug_mode, set_debug_mode
from .debug import get_debug_info, debug_info
from .is_definition import isdefinition
from .placer import Placer, StagedPlacer
from magma.syntax.combinational import combinational
try:
    import kratos
    from magma.syntax.verilog import combinational_to_verilog, \
        sequential_to_verilog
except ImportError:
    pass

from magma.clock import is_clock_or_nested_clock, Clock, ClockTypes
from magma.common import (
    only,
    IterableException,
    EmptyIterableException,
    NonSingletonIterableException,
)
from magma.config import get_debug_mode, set_debug_mode, config, RuntimeConfig
from magma.definition_context import (
    DefinitionContext,
    definition_context_manager,
    push_definition_context,
    pop_definition_context,
    get_definition_context,
)
from magma.find_unconnected_ports import find_and_log_unconnected_ports
from magma.logging import root_logger, capture_logs
from magma.protocol_type import MagmaProtocol
from magma.ref import TempNamedRef, AnonRef
from magma.t import In, Type
from magma.wire_container import WiringLog, AggregateWireable


__all__ = ['AnonymousCircuitType']
__all__ += ['AnonymousCircuit']

__all__ += ['CircuitType']
__all__ += ['Circuit', 'DebugCircuit']
__all__ += ['DeclareCircuit']
__all__ += ['DefineCircuit', 'EndDefine', 'EndCircuit']
__all__ += ['DefineCircuitKind']

__all__ += ['CopyInstance']
__all__ += ['circuit_type_method']
__all__ += ['circuit_generator']
__all__ += ['CircuitBuilder', 'builder_method']
__all__ += ['register_instance_callback', 'get_instance_callback']

circuit_type_method = namedtuple('circuit_type_method', ['name', 'definition'])

_logger = root_logger()

config.register(use_namer_dict=RuntimeConfig(False))


class _SyntaxStyle(enum.Enum):
    NONE = enum.auto()
    OLD = enum.auto()
    NEW = enum.auto()


def _has_definition(cls, port=None):
    if cls.instances:
        return True
    if port is None:
        interface = getattr(cls, "interface", None)
        if not interface:
            return False
        return any(_has_definition(cls, p) for p in interface.ports.values())
    if port.is_output():
        return False
    if port.is_mixed():
        # mixed direction
        return any(_has_definition(cls, p) for p in port)
    return port.driven()


def _maybe_add_default_clock(cls):
    """
    If circuit @cls needs a default input clock (requires that both (a) @cls has
    an instance that has an undriven clock port and (b) @cls *doesn't* already
    have a default clock input), then we add one with the name "CLK". If a port
    with name "CLK" already exists then we do not add any port.
    """
    # Check if @cls already has a default clock.
    for port in cls.io.ports.values():
        if is_clock_or_nested_clock(type(port), (Clock,)):
            return

    # Check all instances in @cls for an undriven clock port.
    inst_ports = itertools.chain(
        *(instance.interface.ports.values() for instance in cls.instances
          if getattr(instance, "stateful", True)))
    for port in inst_ports:
        T = type(port)
        if is_clock_or_nested_clock(T, (Clock,)) and not port.driven():
            break  # undriven clock found
    else:  # no undriven clock found
        return
    if "CLK" in cls.io.ports.keys():
        # What should we do in the case that the CLK name is taken, but isn't a
        # clock type? Seems odd, but we shouldn't cause an error. For now, we
        # can assume that the user might be using some custom "Clock" type and
        # not introduce a default.  Alternatively we could add a different name.
        return

    cls.io.add("CLK", In(Clock))


def _get_interface_type(cls, add_default_clock):
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
        # Assume circuit is stateful, but if it's set stateful=False, then we
        # don't need to add clock (useful for performance to avoid the
        # traversal)
        if add_default_clock and getattr(cls, "stateful", True):
            _maybe_add_default_clock(cls)
        return cls.io.make_interface()
    return None


def _setup_interface(cls):
    IO = _get_interface_type(cls, add_default_clock=True)
    if not hasattr(cls, "IO") and not hasattr(cls, "io"):
        return
    if IO is not None:
        cls.IO = IO
    cls.interface = cls.IO(defn=cls, renamed_ports=cls._renamed_ports_)
    setattrs(cls, cls.interface.ports, lambda k, v: isinstance(k, str))


def _add_intermediate_value(value):
    """
    Add an intermediate value `value` to `values`, handling members of
    recursive types.  Used by `_get_intermediate_values` as part of
    `CircuitKind.__repr__`.
    """
    root = value.name.root()
    # If it is a TempNamedRef which doesn't refer to a constant, then we seed
    # the set with the root value. Otherwise, we can proceed with the empty
    # set.
    if isinstance(root, TempNamedRef) and not root.value().const():
        return OrderedIdentitySet((root.value(),))
    return OrderedIdentitySet()


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
    if (
            isinstance(driver, AggregateWireable) and
            driver.name.anon() and
            driver.has_elaborated_children()
    ):
        return functools.reduce(
            operator.or_, (_get_intermediate_values(v) for v, _ in
                           value.connection_iter()),
            OrderedIdentitySet())
    values = OrderedIdentitySet()
    while driver is not None:
        values |= _add_intermediate_value(driver)
        if not driver.driven():
            break
        value = driver
        driver = driver.value()
    return values


class NamerDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._inferred_names = {}

    def _set_name(self, key, value):
        if isinstance(value, (Type, MagmaProtocol)):
            key = TempNamedRef(key, value)
        value.name = key

    def _check_unique_name(
        self,
        key: str,
        value: Union[Type, 'Circuit'],
    ):
        """If key has been seen more than once, "uniquify" the names by append
           _{i} to them."""
        values = self._inferred_names.setdefault(key, [])
        if len(values) == 0:
            self._set_name(key, value)
        elif any(value is x for x in values):
            return  # already uniquified
        else:
            if len(values) == 1:
                # Make the first value consistent by appending _0.
                self._set_name(f"{key}_0", values[0])
            self._set_name(f"{key}_{len(values)}", value)
        values.append(value)

    def _set_value_name(self, key: str, value: Type):
        if not hasattr(value, "name"):
            return  # interface object is a Type without a name
        if isinstance(value.name, AnonRef):
            self._check_unique_name(key, value)
        elif isinstance(value.name, TempNamedRef):
            self._check_unique_name(value.name.name, value)

    def _set_inst_name(self, key: str, value: 'Circuit'):
        if not value.name:
            self._check_unique_name(key, value)
        else:
            self._check_unique_name(value.name, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if isinstance(value, (Type, MagmaProtocol)):
            self._set_value_name(key, value)
        elif isinstance(type(value), CircuitKind):
            # NOTE(leonardt): we check type(value) because this code is run in
            # the Circuit class creation pipeline (so Circuit may not be defined
            # yet).
            self._set_inst_name(key, value)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class CircuitKind(type):
    def __prepare__(name, bases, **kwargs):
        ctx = DefinitionContext(StagedPlacer(name))
        push_definition_context(ctx, use_staged_logger=True)
        if config.use_namer_dict:
            return NamerDict()
        return type.__prepare__(name, bases, **kwargs)

    """Metaclass for creating circuits."""
    def __new__(metacls, name, bases, dct):
        if isinstance(dct, NamerDict):
            dct = dict(dct)  # resolve to dict, no longer need name logic
        # Override class name if supplied (and save class name).
        cls_name = dct.get("_cls_name_", name)
        name = dct.setdefault('name', name)

        dct.setdefault("_circuit_base_", False)
        dct.setdefault('renamed_ports', {})
        dct.setdefault('primitive', False)
        dct.setdefault('coreir_lib', 'global')
        dct.setdefault("inline_verilog_strs", [])
        dct.setdefault("coreir_metadata", {})
        dct["inline_verilog_generated"] = False
        dct["bind_modules"] = {}
        dct["compiled_bind_modules"] = {}

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

        cls._syntax_style_ = _SyntaxStyle.NONE
        cls._renamed_ports_ = dct["renamed_ports"]
        # NOTE(rsetaluri): We first peek the definition context
        # (get_definition_context()) so that we can finalize it before popping
        # it. This is necessary because we want the unstaging of the logger to
        # happen (inside of pop) after finalization.
        try:
            context = get_definition_context()
        except IndexError:  # no staged placer
            cls._context_ = DefinitionContext(Placer(cls))
        else:
            assert context.placer.name == cls_name
            # Override staged context with '_context_' from namespace if
            # available.
            cls._context_ = dct.get("_context_", context)
            cls._context_.place_instances(cls)
            _setup_interface(cls)
            cls._context_.finalize(cls)
            pop_definition_context(use_staged_logger=True)

        return cls

    def __call__(cls, *largs, **kwargs):
        if "debug_info" not in kwargs:
            kwargs["debug_info"] = get_debug_info(3)
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
        args = cls.IO.args_to_str()

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
        # NOTE(rsetaluri): This is a hack to avoid a circular import.
        from magma.inline_verilog import inline_verilog as m_inline_verilog
        with definition_context_manager(cls._context_):
            m_inline_verilog(inline_str, **kwargs)


class AnonymousCircuitType(object, metaclass=CircuitKind):
    """Abstract base class for circuits"""

    _circuit_base_ = True

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
        name = self.name
        if not name:
            name = f"AnonymousCircuitInst{id(self)}"
        if type(self) is AnonymousCircuitType:
            interface = ", ".join(
                f"{name}: {type(value)}"
                for name, value in self.interface.ports.items()
            )
            name += f"<{interface}>"
        else:
            name += f"<{type(self)}>"
        return name

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
            inputs[i].wire(outputs[i], debug_info)

    def wire(self, output, debug_info):
        """Wire a single output to the circuit's inputs"""
        if hasattr(output, 'interface'):
            # Wire the circuit's outputs to this circuit's inputs.
            self.wireoutputs(output.interface.outputs(), debug_info)
            return
        # Wire the output to this circuit's input (should only have 1 input).
        inputs = []
        for inp in self.interface.inputs():
            inputs.append(inp)
        ni = len(inputs)
        if ni == 0:
            msg = ("Wiring an output to a circuit with no input arguments, "
                   "skipping")
            _logger.warning(msg, debug_info=debug_info)
            return
        if ni != 1:
            _logger.warning(
                WiringLog("Wiring an output to a circuit with more than one "
                          "input argument, using the first input {}",
                          inputs[0]),
                debug_info=debug_info
            )
        inputs[0].wire(output, debug_info)

    @property
    def debug_name(self):
        defn_str = ""
        if hasattr(self, 'defn') and self.defn is not None:
            defn_str = str(self.defn.name)
        return f"{defn_str}.{self.name}"

    def __call__(input, *outputs, **kw):
        debug_info = get_debug_info(3)

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
                _logger.warning(
                    WiringLog(f"Instance {{}} does not have input {key}",
                              input),
                    debug_info=debug_info
                )

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
        return definition_context_manager(cls._context_)


def AnonymousCircuit(*decl):
    """
    AnonymousCircuits are like macros - the circuit instances are not placed
    """
    if len(decl) == 1:
        decl = decl[0]
    return AnonymousCircuitType().setinterface(AnonymousInterface(decl))


class CircuitType(AnonymousCircuitType):
    _circuit_base_ = True

    """Placed circuit - instances placed in a definition"""
    def __init__(self, *largs, **kwargs):
        super(CircuitType, self).__init__(*largs, **kwargs)
        try:
            context = get_definition_context()
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
    debug_info = get_debug_info(4)
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


def _get_name(name, bases, dct):
    try:
        return dct["name"]
    except KeyError:
        pass
    # Take name of the first base class which is not a base circuit type, if one
    # exists.
    for base in bases:
        if base._circuit_base_:
            continue
        if not issubclass(base, AnonymousCircuitType):
            raise Exception(f"Must subclass from AnonymousCircuitType or a "
                            f"subclass of AnonymousCircuitType ({base})")
        return base.name
    return name


class DefineCircuitKind(CircuitKind):
    def __new__(metacls, name, bases, dct):
        dct["_cls_name_"] = name  # save original name for debugging purposes
        name = _get_name(name, bases, dct.copy())
        dct["name"] = name
        dct["renamed_ports"] = dct.get("renamed_ports", {})

        self = CircuitKind.__new__(metacls, name, bases, dct)

        self.verilog = dct.get("verilog", None)
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
                # NOTE(leonardt): We can call setup here before placing
                # instances because old style IO syntax doesn't support the
                # automatic clock lifting anyways
                _setup_interface(self)
                with definition_context_manager(self._context_):
                    self.definition()
                self._context_.place_instances(self)
                self._context_.finalize(self)
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
            with capture_logs(self._context_):
                find_and_log_unconnected_ports(self)

        return self

    def __getattr__(self, attr):
        error = None
        try:
            return object.__getattribute__(self, attr)
        except AttributeError as e:
            # NOTE(rsetaluri): The scope of `e` is only within this `except`
            # block. Therefore we have to stash it in a local variable to be
            # able to raise it later.
            error = e
        # NOTE(rsetaluri): We need to use object.__getattribute__ to avoid
        # potential infinite loops. See
        # https://github.com/phanrahan/magma/pull/1263.
        instances = object.__getattribute__(self, "instances")
        try:
            return only(filter(lambda i: i.name == attr, instances))
        except IterableException:
            pass
        raise error from None

    @property
    def is_definition(self):
        return self._is_definition or self.verilog or self.verilogFile

    @property
    def instances(self):
        # NOTE(rsetaluri): We need to use object.__getattribute__ here because
        # the instances() property might get called in the __getattr__ pipeline
        # resulting in an infinite loop. See
        # https://github.com/phanrahan/magma/pull/1263.
        context = object.__getattribute__(self, "_context_")
        return context.placer.instances()

    def get_instance(self, name: str) -> 'AnonymousCircuitType':
        instances = self.instances
        try:
            return only(filter(lambda i: i.name == name, instances))
        except EmptyIterableException:
            raise KeyError(name) from None
        except NonSingletonIterableException:
            raise KeyError(f"Found multiple instances with name '{name}'")

    @property
    def logs(self):
        return self._context_.logs

    def place(cls, inst):
        """Place a circuit instance in this definition"""
        cls._context_.placer.place(inst)

    def bind(cls, monitor, *args, compile_guard=None):
        cls.bind_modules[monitor] = (args, compile_guard)


class Circuit(CircuitType, metaclass=DefineCircuitKind):
    _circuit_base_ = True


@deprecated(
    msg="DefineCircuit factory method is deprecated, subclass Circuit instead")
def DefineCircuit(name, *decl, **args):
    """DefineCircuit Factory"""
    debug_info = get_debug_info(4)
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
    push_definition_context(defn._context_)
    return defn


def EndDefine():
    # NOTE(rsetaluri): We first peek the definition context
    # (get_definition_context()) so that we avoid pushing on a log capturer for
    # the find_and_log_unconnected_ports() call.
    try:
        context = get_definition_context()
    except IndexError:
        raise Exception("EndDefine not matched to DefineCircuit")
    placer = context.placer
    find_and_log_unconnected_ports(placer._defn)
    debug_info = get_debug_info(3)
    placer._defn.end_circuit_filename = debug_info.filename
    placer._defn.end_circuit_lineno = debug_info.lineno
    pop_definition_context()


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


@deprecated
def DeclareCoreirCircuit(*args, **kwargs):
    return DeclareCircuit(*args, **kwargs,
                          renamed_ports=coreir_port_mapping)


def declare_coreir_circuit(name_: str, ports: dict, coreir_name_: str,
                           coreir_genargs_: dict, coreir_lib_: str):
    """
    parameter names are suffixed with `_` otherwise we get a NameError inside
    the class definition
    """
    class CoreIRCircuit(Circuit):
        name = name_
        renamed_ports = coreir_port_mapping
        io = IO(**ports)
        coreir_name = coreir_name_
        coreir_genargs = coreir_genargs_
        coreir_lib = coreir_lib_

    return CoreIRCircuit


class _CircuitBuilderMeta(type):
    pass


def builder_method(func):

    @wraps(func)
    def _wrapped(this, *args, **kwargs):
        with definition_context_manager(this.context):
            result = func(this, *args, **kwargs)
        return result

    return _wrapped


class CircuitBuilder(metaclass=_CircuitBuilderMeta):
    _RESERVED_NAMESPACE_KEYS = {"io", "_context_", "name"}

    def __init__(self, name):
        # Try to add this builder to a context if one exists currently. A
        # builder can still be constructed outside of a context, but (a) the
        # builder will not be automatically finalized, and (b) instantation
        # might fail.
        try:
            context = get_definition_context()
        except IndexError:
            pass
        else:
            context.add_builder(self)
        self._name = name
        self._io = SingletonInstanceIO()
        self._finalized = False
        self._dct = {}
        self._inst_attrs = {}
        self._context = DefinitionContext(StagedPlacer(self._name))
        self._instance_name = None
        self.debug_info = get_debug_info(4)

    def _port(self, name):
        return self._io.ports[name]

    def _add_port(self, name, typ):
        self._io.add(name, typ)
        setattr(self, name, self._io.inst_ports[name])
        return self._port(name)

    def _add_ports(self, **kwargs):
        return list(self._add_port(name, typ) for name, typ in kwargs.items())

    @property
    def _instances(self):
        return self._context.placer.instances.copy()

    def _set_definition_attr(self, key, value):
        if key in CircuitBuilder._RESERVED_NAMESPACE_KEYS:
            raise Exception(f"Can not set reserved attr '{key}'")
        self._dct[key] = value

    def _set_inst_attr(self, key, value):
        self._inst_attrs[key] = value

    def _open(self):
        return definition_context_manager(self._context)

    def _finalize(self):
        pass

    def set_instance_name(self, name):
        self._instance_name = name

    @property
    def context(self):
        return self._context

    @property
    def instance_name(self):
        if self._instance_name is None:
            return self._name
        return self._instance_name

    @property
    def defn(self):
        if not self._finalized:
            return None
        return self._defn

    def finalize(self, dont_instantiate: bool = False):
        if self._finalized:
            raise Exception("Can only call finalize on a CircuitBuilder once")
        self._finalize()
        bases = (AnonymousCircuitType,)
        dct = {"io": self._io, "_context_": self._context, "name": self._name}
        dct.update(self._dct)
        dct.setdefault("debug_info", self.debug_info)
        DefineCircuitKind.__prepare__(self._name, bases)
        self._defn = DefineCircuitKind(self._name, bases, dct)
        self._context.finalize(self._defn)
        self._finalized = True
        if dont_instantiate:
            return None
        inst = self._defn(name=self.instance_name)
        inst.debug_info = self.debug_info
        for k, v in self._inst_attrs.items():
            setattr(inst, k, v)
        return inst


class DebugDefineCircuitKind(DefineCircuitKind):
    def __prepare__(name, bases, **kwargs):
        prev_debug_mode = get_debug_mode()
        set_debug_mode(True)
        # NOTE(leonardt): Using super() here doesn't work:
        #   cls = super().__prepare__(name, bases, **kwargs)
        #   TypeError: super(type, obj): obj must be an instance or subtype of
        #   type
        cls = DefineCircuitKind.__prepare__(name, bases, **kwargs)
        ctx = get_definition_context()
        ctx.set_metadata("prev_debug_mode", prev_debug_mode)
        return cls

    def __new__(metacls, name, bases, dct):
        ctx = get_definition_context()
        set_debug_mode(ctx.get_metadata("prev_debug_mode"))
        return DefineCircuitKind.__new__(metacls, name, bases, dct)


class DebugCircuit(Circuit, metaclass=DebugDefineCircuitKind):
    pass


InstanceCallback = Callable[[List[CircuitType], Dict], None]


def register_instance_callback(
        instance: CircuitType,
        callback: InstanceCallback,
):
    if hasattr(instance, "_callback_"):
        raise AttributeError(
            f"Instance {instance} already has callback registered"
        )
    instance._callback_ = callback


def get_instance_callback(instance: CircuitType) -> InstanceCallback:
    try:
        return instance._callback_
    except AttributeError:
        msg = (
            f"Instance {instance} has no callback registered. Did you call "
            f"m.register_instance_callback()?"
        )
        raise AttributeError(msg) from None
