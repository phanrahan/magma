from .ref import Ref, AnonRef
from .port import INOUT, INPUT, OUTPUT
from .compatibility import IntegerTypes, StringTypes

__all__  = ['Type', 'Kind']
__all__ += ['In', 'Out', 'InOut', 'Flip']


class Type(object):
    def __init__(self, **kwargs):
        # ref is int, str or tuple
        name = kwargs.get('name', None)
        if name is None or isinstance(name, str):
            #print('creating name ref',name)
            name = AnonRef(name=name)
        #print('using',name)
        #assert isinstance(name, Ref)
        self.name = name

    # subclasses only need to implement one of these methods
    def __eq__(self, rhs):
        return not (self != rhs)
    def __ne__(self, rhs):
        return not (self == rhs)

    __hash__ = object.__hash__

    def __repr__(self):
        return self.name.qualifiedname()

    def __str__(self):
        return self.name.qualifiedname()

    # an instance has an anon name
    def anon(self):
        return self.name.anon()

    # abstract method - must be implemented by subclasses
    @classmethod
    def isoriented(cls, direction):
        pass

    @classmethod
    def isinput(cls):
        return cls.isoriented(INPUT) 

    @classmethod
    def isoutput(self):
        return self.isoriented(OUTPUT)

    @classmethod
    def isinout(self):
        return self.isoriented(INOUT)

    @classmethod
    def isbidir(self):
        return False


class Kind(type):
    def __init__(cls, name, bases, dct):
        type.__init__( cls, name, bases, dct)

    # subclasses only need to implement one of these methods
    def __eq__(cls, rhs):
        return not (cls != rhs)
    def __ne__(cls, rhs):
        return not (cls == rhs)

    __hash__ = type.__hash__

    def __repr__(cls):
        return cls.__name__

    # abstract method - must be implemented by subclasses
    def qualify(cls):
        pass

    # abstract method - must be implemented by subclasses
    def flip(cls):
        pass




def In(T):
    return T.qualify(direction=INPUT)

def Out(T):
    return T.qualify(direction=OUTPUT)

def InOut(T):
    return T.qualify(direction=INOUT)

def Flip(T):
    return T.flip()




