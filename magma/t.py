import abc
import enum
from magma.common import deprecated
from magma.compatibility import IntegerTypes, StringTypes
from magma.ref import AnonRef, NamedRef, DefnRef, InstRef
from magma.protocol_type import magma_value
from magma.wire import wire


class Direction(enum.Enum):
    In = 0
    Out = 1
    InOut = 2
    Undirected = 3


class Type(object):
    def __init__(self, name=None):
        if name is None:
            name = AnonRef()
        elif isinstance(name, str):
            name = NamedRef(name=name, value=self)
        self.name = name

    __hash__ = object.__hash__

    def __repr__(self):
        if self.name.anon():
            return f"{type(self)}()"
        has_name = (isinstance(self.name, NamedRef) and
                    not isinstance(self.name, (InstRef, DefnRef)))
        if has_name:
            return f"{type(self)}(name=\"{repr(self.name)}\")"
        return repr(self.name)

    def __str__(self):
        if self.name.anon():
            # Anon names aren't very useful, so just return a repr instead so
            # it's easier to find the value
            return repr(self)
        return str(self.name)

    # An instance has an anon name.
    def anon(self):
        return self.name.anon()

    # Abstract method to be implemented by subclasses.
    @classmethod
    def is_oriented(cls, direction):
        raise NotImplementedError()

    @classmethod
    def is_clock(cls):
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
        if self.is_output():
            raise TypeError(f"Cannot use <= to assign to output: "
                            f"{self.debug_name} (trying to assign "
                            f"{other.debug_name})")
        wire(other, self)

    def __imatmul__(self, other):
        other = magma_value(other)
        if self.is_output():
            raise TypeError(f"Cannot use @= to assign to output: {self} "
                            f"(trying to assign {other})")
        wire(other, self)
        return self

    @abc.abstractmethod
    def unused(self):
        # Mark value is unused by calling unused on the underlying magma
        # elements. For example, m.Bit is wired up to a coreir term primitive A
        # general m.Array and m.Tuple will recursively call `unused` on its
        # members.
        raise NotImplementedError()

    @abc.abstractmethod
    def undriven(self):
        # Mark value is undriven by calling undriven on the underlying magma
        # elements. For example, m.Bit is wired up to a coreir undriven
        # primitive A general m.Array and m.Tuple will recursively call
        # `undriven` on its members.
        raise NotImplementedError()

    def is_driven_anon_temporary(self):
        """
        Returns true if this is an anonymous temporary value (not an output)
        that is driven
        """
        return self.name.anon() and not self.is_output() and self.driven()


class Kind(type):
    # Subclasses only need to implement one of these methods.
    def __eq__(cls, rhs):
        return cls is rhs

    __hash__ = type.__hash__

    def __repr__(cls):
        return cls.__name__

    def __str__(cls):
        return cls.__name__

    @abc.abstractmethod
    def qualify(cls, direction):
        raise NotImplementedError()

    def flip(cls):
        if cls.direction == Direction.In:
            return cls[Direction.Out]
        if cls.direction == Direction.Out:
            return cls[Direction.In]
        # Flip of inout is inout, and flip of undirected is undirected.
        return cls

    @property
    def undirected_t(cls):
        return cls.qualify(Direction.Undirected)

    @property
    def is_directed(cls):
        return cls is not cls.qualify(Direction.Undirected)


def In(T):
    return T.qualify(Direction.In)


def Out(T):
    return T.qualify(Direction.Out)


def InOut(T):
    return T.qualify(Direction.InOut)


def Flip(T):
    return T.flip()
