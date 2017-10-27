import inspect
from .logging import error
from .port import Port, INPUT, OUTPUT, INOUT
from .t import Type, Kind, In, Out
from .compatibility import IntegerTypes
from .debug import debug_wire, get_callee_frame_info

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

__all__  = ['_BitType', '_BitKind']
__all__ += ['BitType', 'BitKind']
__all__ += ['Bit', 'BitIn', 'BitOut', 'BitInOut']
__all__ += ['VCC', 'GND', 'HIGH', 'LOW']

#
# Each bit is associated with a Port. The Port keeps track of
# how bits are wired together.
#
class _BitType(Type):
    def __init__(self, *largs, **kwargs):
        super(_BitType, self).__init__(*largs, **kwargs)

        self.port = Port(self)

    __ne__ = Type.__ne__
    __hash__ = Type.__hash__

    def __call__(self, output):
        return self.wire(output, get_callee_frame_info())

    @classmethod
    def isoriented(cls, direction):
        return cls.direction == direction

    @debug_wire
    def wire(i, o, debug_info):

        #print('_Bit.wire(', str(i), ', ', str(o), ')')

        # promote integer types to LOW/HIGH
        if isinstance(o, IntegerTypes):
            o = HIGH if o else LOW

        if not isinstance(o, _BitType):
            error('Wiring Error: wiring {} to {} (not a _Bit)'.format(o, i))
            return

        i.port.wire(o.port)
        i.debug_info = debug_info
        o.debug_info = debug_info

    def driven(self):
        return self.port.driven()

    def wired(self):
        return self.port.wired()

    # return the input or output _Bit connected to this _Bit
    def trace(self):
        t = self.port.trace()
        if t: t = t.bit
        return t

    # return the output _Bit connected to this input _Bit
    def value(self):
        t = self.port.value()
        if t: t = t.bit
        return t

    def const(self):
        return self is VCC or self is GND

    def getinst(self):
        t = self.trace()
        return t.name.inst if t else None

    def getgpio(self):
        return self.getinst()

    # return the bits driven by this bit
    def dependencies(self):
        assert self.isoutput(), "Trying to get dependencies from output bit"
        deps = map(lambda i: i.bit, self.port.wires.inputs)
        return deps

    def __repr__(self):
        if self is VCC: return '1'
        if self is GND: return '0'

        #assert not t.anon()
        return self.name.qualifiedname(sep='.')

    def flatten(self):
        return [self]


class _BitKind(Kind):
    def __init__(cls, name, bases, dct):
        super(_BitKind, cls).__init__(name, bases, dct)

        if not hasattr(cls, 'direction'):
            cls.direction = None

    def __eq__(cls, rhs):
        if not isinstance(rhs, _BitKind):
            return False

        #if cls.direction is None or rhs.direction is None:
        #    return True

        return cls.direction == rhs.direction

    __ne__ = Kind.__ne__
    __hash__ = Kind.__hash__

    def __str__(cls):
        if cls.isinput():  return 'In(_Bit)'
        if cls.isoutput(): return 'Out(_Bit)'
        if cls.isinout():  return 'InOut(_Bit)'
        return '_Bit'

    def qualify(cls, direction): 
        if   direction is None:   return _Bit
        elif direction == INPUT:  return _BitIn
        elif direction == OUTPUT: return _BitOut
        return cls

    def flip(cls):
        if   cls.isoriented(INPUT):  return _BitOut
        elif cls.isoriented(OUTPUT): return _BitIn
        return cls

class BitType(_BitType):
    __ne__ = Type.__ne__
    __hash__ = Type.__hash__

class BitKind(_BitKind):
    def __eq__(cls, rhs):
        if not isinstance(rhs, BitKind):
            return False

        #if cls.direction is None or rhs.direction is None:
        #    return True

        return cls.direction == rhs.direction

    __ne__ = _BitKind.__ne__
    __hash__ = _BitKind.__hash__

    def __str__(cls):
        if cls.isinput():  return 'In(Bit)'
        if cls.isoutput(): return 'Out(Bit)'
        if cls.isinout():  return 'InOut(Bit)'
        return 'Bit'

    def qualify(cls, direction): 
        if   direction is None:   return Bit
        elif direction == INPUT:  return BitIn
        elif direction == OUTPUT: return BitOut
        return cls

    def flip(cls):
        if   cls.isoriented(INPUT):  return BitOut
        elif cls.isoriented(OUTPUT): return BitIn
        return cls

@lru_cache(maxsize=None)
def MakeBit(**kwargs):
    return BitKind('Bit', (BitType,), kwargs)

Bit = MakeBit()
BitIn = MakeBit(direction=INPUT)
BitOut = MakeBit(direction=OUTPUT)
BitInOut = MakeBit(direction=INOUT)

VCC = BitOut(name="VCC")
GND = BitOut(name="GND")

HIGH = VCC
LOW = GND

