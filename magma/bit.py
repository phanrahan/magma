from abc import abstractmethod
from .logging import error
from .port import Port, INPUT, OUTPUT, INOUT
from .t import Type, Kind
from .compatibility import IntegerTypes
from .debug import debug_wire, get_callee_frame_info
from .port import report_wiring_error

__all__ = ['_BitType', '_BitKind']
__all__ += ['BitType', 'BitKind']
__all__ += ['Bit', 'BitIn', 'BitOut', 'BitInOut']
__all__ += ['VCC', 'GND', 'HIGH', 'LOW']


class _BitType(Type):
    """
    Each bit is associated with a Port. The Port keeps track of how bits are
    wired together.
    """

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
        # promote integer types to LOW/HIGH
        if isinstance(o, IntegerTypes):
            o = HIGH if o else LOW

        if not isinstance(o, _BitType):
            report_wiring_error(f'Cannot wire {i.debug_name} (type={type(i)}) to {o} (type={type(o)}) because {o.debug_name} is not a _Bit', debug_info)
            return

        i.port.wire(o.port, debug_info)
        i.debug_info = debug_info
        o.debug_info = debug_info

    def driven(self):
        return self.port.driven()

    def wired(self):
        return self.port.wired()

    # return the input or output _Bit connected to this _Bit
    def trace(self):
        t = self.port.trace()
        if t:
            t = t.bit
        return t

    # return the output _Bit connected to this input _Bit
    def value(self):
        t = self.port.value()
        if t:
            t = t.bit
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
        if self is VCC:
            return '1'
        if self is GND:
            return '0'

        return self.name.qualifiedname(sep='.')

    def flatten(self):
        return [self]


class _BitKind(Kind):
    def __init__(cls, name, bases, dct):
        super(_BitKind, cls).__init__(name, bases, dct)

        if not hasattr(cls, 'direction'):
            cls.direction = None

    def __call__(cls, value=None, *args, **kwargs):
        if value is not None:
            if isinstance(value, (bool, IntegerTypes)):
                return VCC if value else GND
        result = super().__call__(*args, **kwargs)
        if value is not None:
            assert isinstance(value, BitType), type(value)
            result(value)
        return result

    def __eq__(cls, rhs):
        if not isinstance(rhs, _BitKind):
            return False

        return cls.direction == rhs.direction

    __ne__ = Kind.__ne__
    __hash__ = Kind.__hash__

    def __str__(cls):
        if cls.isinput():
            return 'In(_Bit)'
        if cls.isoutput():
            return 'Out(_Bit)'
        if cls.isinout():
            return 'InOut(_Bit)'
        return '_Bit'

    def size(self):
        return 1

    @abstractmethod
    def qualify(cls, direction):
        pass

    @abstractmethod
    def flip(cls):
        pass

    def get_family(cls):
        import magma as m
        return m.get_family()


class BitType(_BitType):
    __hash__ = Type.__hash__


class BitKind(_BitKind):
    def __eq__(cls, rhs):
        if not isinstance(rhs, BitKind):
            return False

        return cls.direction == rhs.direction

    __ne__ = _BitKind.__ne__
    __hash__ = _BitKind.__hash__

    def __str__(cls):
        if cls.isinput():
            return 'In(Bit)'
        if cls.isoutput():
            return 'Out(Bit)'
        if cls.isinout():
            return 'InOut(Bit)'
        return 'Bit'

    def qualify(cls, direction):
        if direction is None:
            return Bit
        elif direction == INPUT:
            return BitIn
        elif direction == OUTPUT:
            return BitOut
        elif direction == INOUT:
            return BitInOut
        return cls

    def flip(cls):
        if cls.isoriented(INPUT):
            return BitOut
        elif cls.isoriented(OUTPUT):
            return BitIn
        return cls


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

