from itertools import chain
from collections import OrderedDict
from .conversions import array
from .ref import InstRef, DefnRef, LazyDefnRef, NamedRef
from .t import Type, Kind, MagmaProtocolMeta, Direction
from .clock import Clock, ClockTypes
from .array import Array
from .tuple import Tuple
from .compatibility import IntegerTypes, StringTypes


__all__  = ['DeclareInterface']
__all__ += ['Interface']
__all__ += ['AnonymousInterface']
__all__ += ['InterfaceKind']
__all__ += ['DeclareLazyInterface']
__all__ += ['IO']


def _flatten(l):
    """
    Flat an iterable of iterables to list.
    """
    return list(chain(*l))


def _make_interface_name(decl):
    return f"Interface({', '.join([str(d) for d in decl])})"


def _is_valid_port(port):
    return isinstance(port, (Kind, Type, MagmaProtocolMeta))


def _parse(decl):
    """
    Parse argument declaration of the form:

        (name0, type0, name1, type1, ..., namen, typen)
    """
    if len(decl) % 2:
        raise ValueError(f"Expected even number of arguments, got {len(decl)}")

    names = decl[::2]
    ports = decl[1::2]
    # If name is empty, convert to the index.
    names = [name if name else i for i, name in enumerate(names)]
    # Check that all ports are given as instances of Kind or Type.
    if not all(_is_valid_port(port) for port in ports):
        raise ValueError(f"Expected kinds or types, got {ports}")

    return names, ports


def _make_interface_args(decl, renamed_ports, inst, defn):
    names, ports = _parse(decl)  # parse the class Interface declaration
    args = OrderedDict()
    for name, port in zip(names, ports):
        if   inst: ref = InstRef(inst, name)
        elif defn: ref = DefnRef(defn, name)
        else:      ref = NamedRef(name)

        if name in renamed_ports:
            ref.name = renamed_ports[name]
        if defn:
           port = port.flip()
        if isinstance(port, MagmaProtocolMeta):
            args[name] = port._from_magma_value_(port._to_magma_()(name=ref))
        else:
            args[name] = port(name=ref)

    return args


def _make_wire_str(driver, value, wired):
    """
    Emit the wiring string for `driver` and `value` for the `__repr__` of an
    interface.

    Used by `_make_wires`, `wired` is a set of previously wired values, so in
    cases of fan-out wires are not done more than once.

    Handles non-whole values (e.g. arrays/tuple constructed with values coming
    from multiple sources) by emitting the wiring of the child values.
    """
    if (value, driver) in wired:
        return ""
    wired.add((value, driver))
    if isinstance(driver, (Array, Tuple)) and \
            not driver.iswhole(driver.ts):
        return "".join(_make_wire_str(d, v, wired)
                       for d, v in zip(driver, value))
    iname = value.name.qualifiedname()
    oname = driver.name.qualifiedname()
    return f"wire({oname}, {iname})\n"


def _make_wires(value, wired):
    """
    Make the wires used in the `__repr__` of an interface.

    Handles the recursive types with mixed direction (e.g. Tuples containing
    inputs and outputs)

    Handles anonymous values by skipping them (we don't include anonymous
    temporaries in the representation)

    Handles non-whole values (e.g. arrays/tuple constructed with values coming
    from multiple sources)

    Traces from `value` to the source driver, emitting the wiring of the
    temporaries along the way.
    """
    s = ""
    if value.is_output():
        return s
    if isinstance(value, (Array, Tuple)) and \
            not value.is_input() and \
            not value.is_output() and \
            not value.is_inout():
        # Mixed
        for v in value:
            s += _make_wires(v, wired)
        return s
    driver = value.value()
    if driver is None:
        return s
    if isinstance(value, (Array, Tuple)) and \
            not driver.iswhole(driver.ts):
        for elem in value:
            s += _make_wires(elem, wired)
        return s
    while driver is not None and driver.name.anon():
        # Skip anon values
        driver = driver.value()
    while driver is not None:
        if (driver, value) in wired:
            break
        s += _make_wire_str(driver, value, wired)
        if not driver.is_output():
            value = driver
            driver = driver.value()
        else:
            driver = None
    return s


class _Interface(Type):
    """
    Abstract Base Class for an Interface.
    """
    def __str__(self):
        return str(type(self))

    def __repr__(self):
        s = ""
        wired = set()
        for name, value in self.ports.items():
            if value.is_output():
                continue
            s += _make_wires(value, wired)
        return s

    @classmethod
    def items(cls):
        return cls.ports.items()

    def __iter__(self):
        return iter(self.ports)

    def __len__(self):
        return len(self.ports.keys())

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.ports[key]
        if isinstance(key, int):
            return self.arguments()[key]
        if isinstance(key, slice):
            return array([self[i] for i in range(*key.indices(len(self)))])
        raise ValueError(f"Expected key as str, int, or slice, got {key} "
                         f"({type(key)})")

    def arguments(self):
        """Return all the argument ports."""
        return list(self.ports.values())

    def is_input(self, port, include_clocks=False):
        return port.is_input() and \
            (not isinstance(port, ClockTypes) or include_clocks)

    def inputs(self, include_clocks=False):
        """Return all the argument input ports."""
        return list(filter(lambda x: self.is_input(x, include_clocks),
                           self.ports.values()))

    def inputs_by_name(self, include_clocks=False):
        inputs = []
        for name, port in self.ports.items():
            if self.is_input(port):
                inputs.append(name)
        return inputs

    def outputs(self):
        """Return all the argument output ports."""
        return list(filter(lambda port: port.is_output(), self.ports.values()))

    def args(self):
        """Return all the arguments as name, port."""
        return _flatten(self.ports.items())

    def decl(self):
        """
        Return all the arguments as name, flip(port) (same as the declaration).
        """
        return _flatten([name, type(port).flip()]
                        for name, port in self.ports.items())

    def inputargs(self):
        """Return all the input arguments as name, port."""
        return _flatten([name, port] for name, port in self.ports.items()
                        if port.is_input() and not isinstance(port, ClockTypes))

    def outputargs(self):
        """Return all the output arguments as name, port."""
        return _flatten([name, port] for name, port in self.ports.items()
                        if port.is_output())

    def clockargs(self):
        """Return all the clock arguments as name, port."""
        return _flatten([name, port] for name, port in self.ports.items()
                        if isinstance(port, ClockTypes))

    def clockargnames(self):
        """Return all the clock argument names."""
        return [name for name, port in self.ports.items()
                if isinstance(port, ClockTypes)]

    def isclocked(self):
        """Return True if this interface has a Clock."""
        return any(isinstance(port, ClockType) for
                   port in self.ports.values())

class Interface(_Interface):
    """Interface class."""
    def __init__(self, decl, renamed_ports={}):
        """
        This function assumes the port instances are provided:
            e.g. Interface('I0', In(Bit)(), 'I1', In(Bit)(), 'O', Out(Bit)())
        """
        names, ports = _parse(decl)
        args = OrderedDict()
        for name, port in zip(names, ports):
            if isinstance(name, IntegerTypes):
                name = str(name)  # convert integer to str, e.g. 0 to "0"
            if name in renamed_ports:
                raise NotImplementedError("Port renaming not implemented")
            args[name] = port
        self.ports = args

    def __str__(self):
        s = ", ".join(f"{k}: {v}" for k, v in self.ports.items())
        return f"Interface({s})"


class AnonymousInterface(Interface):
    """
    Anonymous interfaces can have ports that are not inputs/output, so we need
    ot see if they trace to an input or if they are wired to inputs

    TODO: Need tests for all these cases
    """
    def outputs(self):
        return list(filter(
            lambda port: port.is_output() or port.trace() is None and
            not port.wired() and not port.is_input() and not port.is_inout(),
            self.ports.values()))

    def is_input(self, port, include_clocks=False):
        return port.is_input() or port.trace() is None and \
            port.wired() and not port.is_output() and not port.is_inout() and \
            (not isinstance(port, ClockTypes) or include_clocks)


class _DeclareInterface(_Interface):
    """
    _DeclareInterface class.

    First, an Interface is declared:
        Interface = DeclareInterface('I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))

    Then, the interface is instanced:
        interface = Interface()
    """
    def __init__(self, renamed_ports={}, inst=None, defn=None):
        self.ports = _make_interface_args(self.Decl, renamed_ports, inst, defn)

class _DeclareLazyInterface(_Interface):
    """_DeclareLazyInterface class"""
    def __init__(self, renamed_ports={}, inst=None, defn=None):
        # This interface declaration is only lazy for module definitions (not
        # instances). If @defn is not supplied, then we use the standard
        # (non-lazy) interface construction logic.
        if not defn:
            self.ports = _make_interface_args(self.Decl, renamed_ports, inst,
                                              defn)
            return
        args = OrderedDict()
        for name, port in self.io.ports.items():
            ref = port.name
            ref.set_defn(defn)
            if name in renamed_ports:
                ref.name = renamed_ports[name]
            args[name] = port

        self.ports = args


class InterfaceKind(Kind):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ports = []
        key = None
        for i, arg in enumerate(cls.Decl):
            if i % 2 == 0:
                key = arg
            else:
                ports.append((key, arg))
        cls.ports = OrderedDict(ports)

    def items(cls):
        return cls.ports.items()

    def __iter__(cls):
        return iter(cls.ports)

    def __str__(cls):
        args = []
        for i, arg in enumerate(cls.Decl):
            if i % 2 == 0:
                args.append(f"\"{arg}\"")
            else:
                args.append(str(arg))
        return ", ".join(args)

    def __eq__(cls, rhs):
        return cls.Decl == rhs.Decl

    __ne__=Kind.__ne__
    __hash__=Kind.__hash__


def DeclareInterface(*decl, **kwargs):
    """Interface factory function."""
    name = _make_interface_name(decl)
    dct = dict(Decl=decl, **kwargs)
    return InterfaceKind(name, (_DeclareInterface,), dct)


def DeclareLazyInterface(io, **kwargs):
    """LazyInterface factory function"""
    decl = io.decl()
    name = _make_interface_name(decl)
    dct = dict(io=io, Decl=io.decl(), **kwargs)
    return InterfaceKind(name, (_DeclareLazyInterface,), dct)


class IO:
    """
    Class for creating an interface bundle.

    @kwargs: ordered dict of {name: type}, ala decl.
    """
    # Note that because we require kwargs to be ordered, we have a strong
    # requirement here for >= python version 3.6. See
    # https://www.python.org/dev/peps/pep-0468/.
    def __init__(self, **kwargs):
        self.ports = {}
        self.__decl = []
        for name, typ in kwargs.items():
            ref = LazyDefnRef(name=name)
            if isinstance(typ, MagmaProtocolMeta):
                port = typ.flip()
                port = port._from_magma_value_(port._to_magma_()(name=ref))
            else:
                port = typ.flip()(name=ref)
            self.ports[name] = port
            self.__decl += [name, typ]
            setattr(self, name, port)

    def decl(self):
        return self.__decl
