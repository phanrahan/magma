import functools
import warnings
import enum
from abc import abstractmethod, ABCMeta
from .common import deprecated
from .ref import Ref, AnonRef, DefnRef, InstRef
from .compatibility import IntegerTypes, StringTypes


class Direction(enum.Enum):
    In = 0
    Out = 1
    InOut = 2
    Undirected = 3


class Type(object):
    def __init__(self, **kwargs):
        name = kwargs.get('name', None)
        if name is None or isinstance(name, str):
            name = AnonRef(name=name)
        self.name = name

    __hash__ = object.__hash__

    def __repr__(self):
        return repr(self.name)

    def __str__(self):
        return str(self.name)

    # an instance has an anon name
    def anon(self):
        return self.name.anon()

    # abstract method - must be implemented by subclasses
    @classmethod
    def is_oriented(cls, direction):
        raise NotImplementedError()

    @classmethod
    def is_input(cls):
        return cls.is_oriented(Direction.In)

    @classmethod
    def is_output(cls):
        return cls.is_oriented(Direction.Out)

    @classmethod
    def is_inout(cls):
        return cls.is_oriented(Direction.InOut)

    @classmethod
    @deprecated
    def isoriented(cls, direction):
        return cls.is_oriented(direction)

    @classmethod
    @deprecated
    def isinput(cls):
        return cls.is_input()

    @classmethod
    @deprecated
    def isoutput(cls):
        return cls.is_output()

    @classmethod
    @deprecated
    def isinout(cls):
        return cls.is_inout()

    @property
    def debug_name(self):
        defn_str = ""
        inst_str = ""
        if isinstance(self.name, DefnRef):
            defn_str = str(self.name.defn.name) + "."
        elif isinstance(self.name, InstRef):
            inst_str = str(self.name.inst.name) + "."
            defn_str = str(self.name.inst.defn.name) + "."
        return f"{defn_str}{inst_str}{str(self)}"

    def __le__(self, other):
        if not self.is_output():
            self.wire(other)
        else:
            raise TypeError(f"Cannot use <= to assign to output: {self.debug_name} (trying to assign {other.debug_name})")

    def __imatmul__(self, other):
        if not self.is_output():
            self.wire(other)
        else:
            raise TypeError(f"Cannot use @= to assign to output: {self.debug_name} (trying to assign {other.debug_name})")
        return self

    @abstractmethod
    def unused(self):
        # Mark value is unused by calling unused on the underlying magma
        # elements
        # For example, m.Bit is wired up to a coreir term primitive
        # A general m.Array and m.Tuple will recursively call `unused` on its
        # members
        raise NotImplementedError()

    @abstractmethod
    def undriven(self):
        # Mark value is undriven by calling undriven on the underlying magma
        # elements
        # For example, m.Bit is wired up to a coreir undriven primitive
        # A general m.Array and m.Tuple will recursively call `undriven` on its
        # members
        raise NotImplementedError()



class Kind(type):
    # subclasses only need to implement one of these methods
    def __eq__(cls, rhs):
        return cls is rhs

    __hash__ = type.__hash__

    def __repr__(cls):
        return cls.__name__

    def __str__(cls):
        return cls.__name__

    @abstractmethod
    def qualify(cls, direction):
        raise NotImplementedError()

    def flip(cls):
        if cls.direction == Direction.In:
            return cls[Direction.Out]
        elif cls.direction == Direction.Out:
            return cls[Direction.In]
        else:
            # Flip of inout is inout
            # Flip of undirected is undirected
            return cls


def dispatch_magma_protocol(func):
    @functools.wraps(func)
    def wrapper(T):
        if issubclass(T, MagmaProtocol):
            return T._from_magma_(func(T._to_magma_()))
        return func(T)
    return wrapper


@dispatch_magma_protocol
def In(T):
    return T.qualify(Direction.In)


@dispatch_magma_protocol
def Out(T):
    return T.qualify(Direction.Out)


@dispatch_magma_protocol
def InOut(T):
    return T.qualify(Direction.InOut)


@dispatch_magma_protocol
def Flip(T):
    return T.flip()


class MagmaProtocolMeta(ABCMeta):
    @abstractmethod
    def _to_magma_(cls):
        # Need way to retrieve underlying magma type
        raise NotImplementedError()

    @abstractmethod
    def _from_magma_(cls, T: Kind):
        # Need way to create a new version (e.g. give me a Foo with the
        # underlying type qualified to be an input)
        raise NotImplementedError()

    @abstractmethod
    def _from_magma_value_(cls, val: Type):
        # Need a way to create an instance from a value
        raise NotImplementedError()

    def flip(cls):
        return cls._from_magma_(cls._to_magma_().flip())


class MagmaProtocol(metaclass=MagmaProtocolMeta):
    @abstractmethod
    def _get_magma_value_(self):
        # Need way to access underlying magma value
        raise NotImplementedError()

    @classmethod
    def is_input(cls):
        return cls._to_magma_().is_input()

    @classmethod
    def is_output(cls):
        return cls._to_magma_().is_output()

    def value(cls):
        return cls._get_magma_value_().value()

    def driven(cls):
        return cls._get_magma_value_().driven()

    @property
    def name(cls):
        return cls._get_magma_value_().name
