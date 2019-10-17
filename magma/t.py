import warnings
import enum
from abc import abstractclassmethod
from .ref import Ref, AnonRef, DefnRef, InstRef
from .port import INOUT, INPUT, OUTPUT
from .compatibility import IntegerTypes, StringTypes


# From http://code.activestate.com/recipes/391367-deprecated/
def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    def newFunc(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc


class Direction(enum.Enum):
    In = 0
    Out = 1
    InOut = 2
    Flip = 3


class Type(object):
    def __init__(self, **kwargs):
        name = kwargs.get('name', None)
        if name is None or isinstance(name, str):
            name = AnonRef(name=name)
        self.name = name

    # subclasses only need to implement one of these methods
    def __eq__(self, rhs):
        return not (self != rhs)

    def __ne__(self, rhs):
        return not (self == rhs)

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
        if self.is_input():
            self.wire(other)
        else:
            raise TypeError(f"Cannot use <= to assign to output: {self.debug_name} (trying to assign {other.debug_name})")


class Kind(type):
    # subclasses only need to implement one of these methods
    def __eq__(cls, rhs):
        raise NotImplementedError()

    __hash__ = type.__hash__

    def __repr__(cls):
        return cls.__name__

    def __str__(cls):
        return cls.__name__

#     @abstractclassmethod
#     def qualify(cls):
#         pass

    def flip(cls):
        return cls.qualify(Direction.Flip)


def In(T):
    return T.qualify(Direction.In)


def Out(T):
    return T.qualify(Direction.Out)


def InOut(T):
    return T.qualify(Direction.InOut)


def Flip(T):
    return T.qualify(Direction.Flip)
