from abc import ABC, abstractmethod
from collections import OrderedDict
from itertools import chain
from .common import deprecated, setattrs
from .compatibility import IntegerTypes, StringTypes
from .protocol_type import MagmaProtocolMeta
from .ref import InstRef, DefnRef, LazyDefnRef, LazyInstRef, NamedRef
from .t import Type, Kind, Direction


__all__  = ['make_interface']
__all__ += ['InterfaceKind', 'Interface', 'AnonymousInterface']
__all__ += ['IO', 'SingletonInstanceIO']


def _flatten(l):
    """Flatten an iterable of iterables to list."""
    return list(chain(*l))


def _make_interface_name(decl):
    return f"Interface({', '.join([str(d) for d in decl])})"


def _is_valid_port(port):
    return isinstance(port, (Kind, Type, MagmaProtocolMeta))


def _parse_decl(decl):
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


def _make_ref(name, inst, defn):
    assert not (inst is not None and defn is not None)
    if inst:
        return InstRef(inst, name)
    if defn:
        return DefnRef(defn, name)
    return NamedRef(name)


def _make_port(typ, ref, flip):
    if flip:
        typ = typ.flip()
    if isinstance(typ, MagmaProtocolMeta):
        return typ._from_magma_value_(typ._to_magma_()(name=ref))
    return typ(name=ref)


def _rename_ports(ports, renamed_ports):
    for name, port in ports.items():
        if name not in renamed_ports:
            continue
        port.name.name = renamed_ports[name]


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
    if driver.iswhole():
        iname = value.name.qualifiedname()
        oname = driver.name.qualifiedname()
        return f"wire({oname}, {iname})\n"
    return "".join(_make_wire_str(d, v, wired)
                   for d, v in zip(driver, value))


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
    if value.is_output():
        return ""
    if value.is_mixed():
        return "".join(_make_wires(v, wired) for v in value)
    driver = value.value()
    if driver is None:
        return ""
    if not driver.iswhole():
        return "".join(_make_wires(v, wired) for v in value)
    while driver is not None and driver.is_driven_anon_temporary():
        driver = driver.value()
    s = ""
    while driver is not None:
        if (driver, value) in wired:
            break
        s += _make_wire_str(driver, value, wired)
        if driver.is_output():
            break
        value = driver
        driver = driver.value()
    return s


class InterfaceKind(Kind):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        args = zip(cls._decl[::2], cls._decl[1::2])
        cls.ports = OrderedDict(args)

    def items(cls):
        return cls.ports.items()

    def __iter__(cls):
        return iter(cls.ports)

    def __str__(cls):
        args = [f"\"{arg}\"" if i % 2 == 0 else str(arg)
                for i, arg in enumerate(cls._decl)]
        return ", ".join(args)

    def __eq__(cls, rhs):
        return cls._decl == rhs._decl

    def __ne__(cls, rhs):
        return super().__ne__(rhs)

    def __hash__(cls):
        return super().__hash__()


class _InterfaceBase(Type):
    """Abstract Base Class for Interface types"""
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
            return [self[i] for i in range(*key.indices(len(self)))]
        raise ValueError(f"Expected key as str, int, or slice, got {key} "
                         f"({type(key)})")

    def arguments(self):
        """Return all the argument ports."""
        return list(self.ports.values())

    def is_input(self, port, include_clocks=False):
        return (port.is_input() and
                (not port.is_clock() or include_clocks))

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
        return _flatten([name, port]
                        for name, port in self.ports.items()
                        if port.is_input() and not port.is_clock())

    def outputargs(self):
        """Return all the output arguments as name, port."""
        return _flatten([name, port]
                        for name, port in self.ports.items()
                        if port.is_output())

    def clockargs(self):
        """Return all the clock arguments as name, port."""
        return _flatten([name, port]
                        for name, port in self.ports.items()
                        if port.is_clock())

    def clockargnames(self):
        """Return all the clock argument names."""
        return [name for name, port in self.ports.items()
                if port.is_clock()]

    def isclocked(self):
        """Return True if this interface has a Clock."""
        return any(port.is_clock()
                   for port in self.ports.values())


class Interface(_InterfaceBase):
    """Interface class"""
    def __init__(self, decl, renamed_ports={}):
        """
        Assumes the port instances are provided:
            e.g. Interface('I0', In(Bit)(), 'I1', In(Bit)(), 'O', Out(Bit)())
        """

        def _map_name(name):
            if name in renamed_ports:
                raise NotImplementedError("Port renaming not implemented")
            # Convert integer to str, e.g. 0 to "0".
            if isinstance(name, IntegerTypes):
                return str(name)
            return name

        names, types = _parse_decl(decl)
        names = map(_map_name, names)
        self.ports = OrderedDict(zip(names, types))

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

        def _is_output(port):
            return (port.is_output() or port.trace() is None and
                    not port.wired() and not port.is_input() and
                    not port.is_inout())

        return list(filter(_is_output, self.ports.values()))

    def is_input(self, port, include_clocks=False):
        return (port.is_input() or port.trace() is None and
                port.wired() and not port.is_output() and not port.is_inout() and
                (not port.is_clock() or include_clocks))


class _DeclareInterface(_InterfaceBase):
    """
    _DeclareInterface class.

    First, an Interface is declared:
        Interface = DeclareInterface('I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))

    Then, the interface is instanced:
        interface = Interface()
    """
    def __init__(self, renamed_ports={}, *, inst=None, defn=None):
        assert not (inst is not None and defn is not None)
        cls = type(self)
        names, types = _parse_decl(cls._decl)
        refs = (_make_ref(name, inst, defn) for name in names)
        args = zip(names, zip(types, refs))
        flip = defn is not None
        self.ports = {n: _make_port(t, r, flip) for n, (t, r) in args}
        _rename_ports(self.ports, renamed_ports)


class _DeclareSingletonInterface(_DeclareInterface):
    """_DeclareSingletonInterface class"""
    def __init__(self, renamed_ports={}, *, inst=None, defn=None):
        assert not (inst is not None and defn is not None)
        # This interface declaration has singleton semantics for its module
        # definition (not instances or further definition instancing).
        cls = type(self)
        if cls._initialized:
            super().__init__(renamed_ports, inst=inst, defn=defn)
            return
        assert defn is not None
        cls._io.bind(defn)  # bind IO to @defn
        self.ports = OrderedDict(cls._io.ports.items())
        _rename_ports(self.ports, renamed_ports)  # rename ports
        cls._initialized = True


class _DeclareSingletonInstanceInterface(_DeclareInterface):
    """_DeclareSingletonInterface class"""
    def __init__(self, renamed_ports={}, *, inst=None, defn=None):
        assert not (inst is not None and defn is not None)
        # This interface declaration has singleton semantics for its module
        # definition (not instances or further definition instancing).
        cls = type(self)

        if defn:
            if cls._initialized:
                super().__init__(renamed_ports, inst=inst, defn=defn)
                return
            cls._io.bind(defn)  # bind IO to @defn
            self.ports = OrderedDict(cls._io.ports.items())
            _rename_ports(self.ports, renamed_ports)  # rename ports
            cls._initialized = True
            return
        if inst:
            if cls._initialized_inst:
                super().__init__(renamed_ports, inst=inst, defn=defn)
                return
            cls._io.bind_inst(inst)  # bind IO to @inst
            self.ports = OrderedDict(cls._io.inst_ports.items())
            _rename_ports(self.ports, renamed_ports)  # rename ports
            cls._initialized_inst = True
            return
        super().__init__(renamed_ports, inst=inst, defn=defn)


def make_interface(*decl):
    """Interface factory function."""
    name = _make_interface_name(decl)
    dct = dict(_decl=decl)
    return InterfaceKind(name, (_DeclareInterface,), dct)


@deprecated(msg="DeclareInterface() is deprecated, use make_interface() "
            "instead")
def DeclareInterface(*decl):
    return make_interface(*decl)


class IOInterface(ABC):
    """Abstract base class for IO-like classes"""
    @property
    @abstractmethod
    def ports(self):
        raise NotImplementedError()

    @abstractmethod
    def bind(self, defn):
        raise NotImplementedError()

    @abstractmethod
    def decl(self):
        raise NotImplementedError()

    @abstractmethod
    def make_interface(self):
        raise NotImplementedError()

    @abstractmethod
    def __add__(self, other):
        raise NotImplementedError()

    def __iadd__(self, other):
        # __iadd__ is explicitly overriden to enforce that it is non-mutating.
        return self + other


class IO(IOInterface):
    """
    Class for creating an interface bundle.

    @kwargs: ordered dict of {name: type}, ala decl.
    """
    # Note that because we require kwargs to be ordered, we have a strong
    # requirement here for >= python version 3.6. See
    # https://www.python.org/dev/peps/pep-0468/.
    def __init__(self, **kwargs):
        self._ports = {}
        self._decl = []
        names = kwargs.keys()
        types = kwargs.values()
        refs = (LazyDefnRef(name=name) for name in kwargs)
        args = zip(kwargs.keys(), zip(kwargs.values(), refs))
        self._ports = {n: _make_port(t, r, flip=True) for n, (t, r) in args}
        setattrs(self, self._ports)
        self._decl = _flatten(zip(names, types))
        self._bound = False

    @property
    def ports(self):
        return self._ports.copy()

    def bind(self, defn):
        if self._bound:
            raise Exception("Can not bind IO multiple times")
        for port in self._ports.values():
            port.name.set_defn(defn)
        self._bound = True

    def decl(self):
        return self._decl

    def make_interface(self):
        decl = self.decl()
        name = _make_interface_name(decl)
        dct = dict(_io=self, _decl=decl, _initialized=False)
        return InterfaceKind(name, (_DeclareSingletonInterface,), dct)

    def __add__(self, other):
        """
        Attempts to combine this IO and @other. Returns a new IO object with the
        combined ports, unless:
          * @other is not of type IOInterface, in which case a TypeError is
            raised
          * this or @other has already been bound, in which case an Exception is
            raised
          * this and @other have common port names, in which case an Exception
            is raised
        """
        if not isinstance(other, IOInterface):
            raise TypeError(f"unsupported operand type(s) for +: 'IO' and "
                            f"'{type(other).__name__}'")
        if self._bound or other._bound:
            raise Exception("Adding bound IO not allowed")
        if self._ports.keys() & other._ports.keys():
            raise Exception("Adding IO with duplicate port names not allowed")
        decl = self._decl + other._decl
        return IO(**dict(zip(decl[::2], decl[1::2])))


class SingletonInstanceIO(IO):
    """
    Class for creating an interface bundle for a singleton instance.

    @kwargs: ordered dict of {name: type}, ala decl.
    """
    def __init__(self):
        super().__init__()
        self._inst_ports = {}
        self._bound_inst = False

    def bind_inst(self, inst):
        if self._bound_inst:
            raise Exception("Can not bind IO multiple times")
        for port in self._inst_ports.values():
            port.name.set_inst(inst)
        self._bound = True

    @property
    def inst_ports(self):
        return self._inst_ports.copy()

    def make_interface(self):
        decl = self.decl()
        name = _make_interface_name(decl)
        dct = dict(_io=self, _decl=decl, _initialized=False,
                   _initialized_inst=False)
        return InterfaceKind(name, (_DeclareSingletonInstanceInterface,), dct)

    def add(self, name, typ):
        # Definition port.
        ref = LazyDefnRef(name=name)
        port = _make_port(typ, ref, flip=True)
        self._ports[name] = port
        setattr(self, name, port)
        # Instance port.
        inst_ref = LazyInstRef(name=name)
        inst_port = _make_port(typ, inst_ref, flip=False)
        self._inst_ports[name] = inst_port

    def __add__(self, other):
        raise NotImplementedError(f"Addition operator disallowed on "
                                  f"{cls.__name__}")
