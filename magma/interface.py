from itertools import chain
from collections import OrderedDict
from .conversions import array
from .ref import AnonRef, InstRef, DefnRef
from .t import Type, Kind, MagmaProtocolMeta
from .port import INPUT, OUTPUT, INOUT
from .clock import Clock, ClockTypes
from .array import Array
from .tuple import Tuple
from .compatibility import IntegerTypes, StringTypes


__all__  = ['DeclareInterface']
__all__ += ['Interface']
__all__ += ['InterfaceKind']


def _flatten(l):
    """
    Flat an iterable of iterables to list.
    """
    return list(chain(*l))


def is_valid_port(port):
    return isinstance(port, (Kind, Type, MagmaProtocolMeta))


def parse(decl):
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
    if not all(is_valid_port(port) for port in ports):
        raise ValueError(f"Expected kinds or types, got {ports}")

    return names, ports


class _Interface(Type):
    """
    Abstract Base Class for an Interface.
    """
    def __str__(self):
        return str(type(self))

    def __repr__(self):
        s = ""
        for name, input in self.ports.items():
            if not input.is_input():
                continue
            output = input.value()
            if isinstance(output, (Array, Tuple)):
                if not output.iswhole(output.ts):
                    for i in range(len(input)):
                        iname = repr(input[i])
                        oname = repr(output[i])
                        s += f"wire({oname}, {iname})\n"
                    continue
            iname = repr(input)
            oname = repr(output)
            s += f"wire({oname}, {iname})\n"
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

    def inputs(self, include_clocks=False):
        """Return all the argument input ports."""
        fn = lambda port: port.is_input() and \
            (not isinstance(port, ClockTypes) or include_clocks)
        return list(filter(fn, self.ports.values()))

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
        names, ports = parse(decl)
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


class _DeclareInterface(_Interface):
    """
    _DeclareInterface class.

    First, an Interface is declared:
        Interface = DeclareInterface('I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))

    Then, the interface is instanced:
        interface = Interface()
    """
    def __init__(self, renamed_ports={}, inst=None, defn=None):
        # Parse the class Interface declaration.
        names, ports = parse(self.Decl)

        args = OrderedDict()
        for name, port in zip(names, ports):
            if   inst: ref = InstRef(inst, name)
            elif defn: ref = DefnRef(defn, name)
            else:      ref = AnonRef(name)

            if name in renamed_ports:
                ref.name = renamed_ports[name]
            if defn:
               port = port.flip()
            if isinstance(port, MagmaProtocolMeta):
                args[name] = port._from_magma_value_(port._to_magma_()(name=ref))
            else:
                args[name] = port(name=ref)

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
    name = f"Interface({', '.join([str(a) for a in decl])})"
    dct = dict(Decl=decl, **kwargs)
    return InterfaceKind(name, (_DeclareInterface,), dct)
