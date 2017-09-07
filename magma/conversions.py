from collections import Sequence, OrderedDict
from .compatibility import IntegerTypes
from .t import In, Out
from .bit import BitKind, BitType, Bit, VCC, GND, BitIn, BitOut, BitInOut
from .clock import ClockType, Clock, ClockIn, ClockOut, ResetType, EnableType
from .array import ArrayType, Array
from .bits import BitsType, Bits, UIntType, UInt, SIntType, SInt
from .tuple import TupleType, Tuple
from .bitutils import int2seq

__all__  = ['bit']
__all__ += ['clock']

__all__ += ['array']
__all__ += ['bits', 'uint', 'sint']

__all__ += ['tuple_']

def bit(value):
    if isinstance(value, BitType):
        return value

    if not isinstance(value, (ClockType, ResetType, EnableType, ArrayType, BitsType, UIntType, SIntType, IntegerTypes)):
        raise ValueError(
            "bit can only be used with a Clock, Array, Bits, UInt, SInt, or int, not : {}".format(type(value)))

    if isinstance(value, (ArrayType, BitsType, UIntType, SIntType)):
        assert len(value) == 1
        value = value[0]

    if isinstance(value, IntegerTypes):
        return VCC if value else GND

    if isinstance(value, (ClockType, ResetType, EnableType)):
        if   value.isinput():  b = BitIn()
        elif value.isoutput(): b = BitOut()
        else: b = Bit()
        b.port = value.port
        return b

    return value


def clock(value):
    if isinstance(value, ClockType):
        return value

    if not isinstance(value, (BitType, ArrayType, BitsType, UIntType, SIntType, IntegerTypes)):
        raise ValueError(
            "clock can only be used with a Bit, Array, Bits, UInt, SInt, or int, not : {}".format(type(value)))

    if isinstance(value, (ArrayType, BitsType, UIntType, SIntType)):
        assert len(value) == 1
        value = value[0]

    if isinstance(value, IntegerTypes):
        return VCC if value else GND

    if isinstance(value, (BitType, EnableType, ResetType)):
        if   value.isinput():  c = ClockIn()
        elif value.isoutput(): c = ClockOut()
        else: c = Clock()
        c.port = value.port
        return c

    return value

def convertbits(value, n, totype, checkbit):
    if not isinstance(value, (BitType, ClockType, ResetType, EnableType, TupleType, ArrayType, BitsType, UIntType, SIntType, IntegerTypes, Sequence)):
        raise ValueError(
            "bits can only be used with a Bit, Clock, Tuple, Array, Bits, UInt, SInt, int, or Sequence, not : {}".format(type(value)))

    if not isinstance(value, (IntegerTypes, BitType, ClockType)):
        assert n is None

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(),1)
        ts = int2seq(value, n)
    elif isinstance(value, Sequence):
        ts =  list(value)
    elif isinstance(value, (BitType, ClockType, ResetType, EnableType)):
        if n is None:
            ts = [value]
        else:
            ts = n*[value]
    else:
        ts = [value[i] for i in range(len(value))]

    # create list of types
    Ts = []
    for t in ts:
        T = type(t)
        if T in IntegerTypes:
            T = Out(Bit)
        Ts.append(T)

    # check that they are all the same
    for t in Ts:
       # make this test optional ...
       if checkbit:
           assert isinstance(t, BitKind)
       assert t == T

    return totype(len(Ts), T)(*ts)

def array(value, n=None):
    if isinstance(value, ArrayType):
        return value
    return convertbits(value, n, Array, False)

def bits(value, n=None):
    if isinstance(value, BitsType):
        return value
    return convertbits(value, n, Bits, True)

def uint(value, n=None):
    if isinstance(value, UIntType):
        return value
    if isinstance(value, SIntType):
        raise ValueError( "uint cannot convert SInt" ) 
    return convertbits(value, n, UInt, True)

def sint(value, n=None):
    if isinstance(value, SIntType):
        return value
    if isinstance(value, UIntType):
        raise ValueError( "uint cannot convert SInt" ) 
    return convertbits(value, n, SInt, True)

#
# convert value to a tuple
#   *value = tuple from positional arguments
#   **kwargs = tuple from keyword arguments
#
def tuple_(value):
    if isinstance(value, TupleType):
        return value

    decl = OrderedDict()
    args = []

    if isinstance(value, IntegerTypes):
        value = int2seq(value, max(value.bit_length(),1) )
    elif isinstance(value, (BitType, ClockType, ResetType, EnableType)):
        value = [value]
    elif isinstance(value, ArrayType):
        value = [value[i] for i in range(len(value))]

    if isinstance(value, Sequence):
        ts = list(value)
        for i in range(len(ts)):
            args.append(ts[i])
            decl[i] = type(ts[i])
    elif isinstance(value, (dict, OrderedDict)):
        for k, v in value.items():
            args.append(v)
            decl[k] = type(v)
    else:
        assert False

    return Tuple(decl)(*args)
