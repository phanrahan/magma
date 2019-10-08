import enum
from abc import abstractclassmethod
from .ref import Ref, AnonRef, DefnRef, InstRef
from .port import INOUT, INPUT, OUTPUT
from .compatibility import IntegerTypes, StringTypes

__all__  = ['Type', 'Kind']
__all__ += ['In', 'Out', 'InOut', 'Flip']


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
        pass

    @classmethod
    def is_input(cls):
        return cls.is_oriented(INPUT)

    @classmethod
    def is_output(self):
        return self.is_oriented(OUTPUT)

    @classmethod
    def is_inout(self):
        return self.is_oriented(INOUT)

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
        if self.isinput():
            self.wire(other)
        else:
            raise TypeError(f"Cannot use <= to assign to output: {self.debug_name} (trying to assign {other.debug_name})")


class Kind(type):
    # subclasses only need to implement one of these methods
    def __eq__(cls, rhs):
        return cls is rhs

    def __ne__(cls, rhs):
        return cls is not rhs

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
    return T.qualify(direction=INPUT)

def Out(T):
    return T.qualify(direction=OUTPUT)

def InOut(T):
    return T.qualify(direction=INOUT)

def Flip(T):
    return T.flip()
