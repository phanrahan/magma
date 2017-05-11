from .ref import Ref, AnonRef
from .port import INOUT, INPUT, OUTPUT
from .compatibility import IntegerTypes, StringTypes

__all__  = ['Type', 'Kind']
__all__ += ['In', 'Out', 'InOut', 'Flip']




#def qualifiedname(self, sep='.'):
#    instname = str(self.inst) if self.inst else None
#    
#    if isinstance(self.addr, IntegerTypes):
#        assert instname
#        return instname + '[%d]' % self.addr
#    else:
#        name = self.name()
#        return instname + sep+ name if instname else name


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

    def __eq__(self, rhs):
        return not (self != rhs)
    def __ne__(self, rhs):
        return not (self == rhs)

    __hash__ = object.__hash__

    def __repr__(self):
        return self.name.qualifiedname()

    def __str__(self):
        return self.name.qualifiedname()

    #def name(self):
    #    # Bit or Array
    #    if isinstance(self.addr, StringTypes):
    #        return self.addr
    #
    #    # Array[i] or Tuple.i
    #    elif isinstance(self.addr, tuple):
    #        i = self.addr[1]
    #        if   isinstance(i, IntegerTypes):
    #            return self.addr[0].name() + '[%d]' % i
    #        elif isinstance(i, StringTypes):
    #            return self.addr[0].name() + '.' + i
    #
    #    # positional argument
    #    elif isinstance(self.addr, IntegerTypes):
    #        return str(self.addr)
    #
    #    return ""

    def isoriented(self, direction):
        return type(self)._isoriented(direction)

    def isinput(self):
        return self.isoriented(INPUT) 

    def isoutput(self):
        return self.isoriented(OUTPUT)

    def isinout(self):
        return self.isoriented(INOUT)

    def isbidir(self):
        return False

    # an anonymous type has an anon name
    def anon(self):
        return self.name.anon()


class Kind(type):
    def __init__(cls, name, bases, dct):
        type.__init__( cls, name, bases, dct)

    def __eq__(cls, rhs):
        return not (cls != rhs)

    def __ne__(cls, rhs):
        return not (cls == rhs)

    __hash__ = type.__hash__

    def __repr__(cls):
        return cls.__name__

    def _isinput(cls):
        return cls._isoriented(INPUT)

    def _isoutput(cls):
        return cls._isoriented(OUTPUT)

    def _isinout(cls):
        return cls._isoriented(INOUT)

    def _isbidir(cls):
        return False

def In(t):
    return t.qualify(direction=INPUT)

def Out(t):
    return t.qualify(direction=OUTPUT)

def InOut(t):
    return t.qualify(direction=INOUT)

def Flip(t):
    return t.flip()




