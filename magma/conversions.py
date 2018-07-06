from collections import Sequence, Mapping, OrderedDict
from .compatibility import IntegerTypes
from .t import In, Out
from .bit import _BitKind, _BitType, Bit, BitKind, BitType, VCC, GND
from .clock import ClockType, Clock, \
    Reset, ResetType, \
    Enable, EnableType
from .array import ArrayType, Array
from .bits import BitsType, Bits, UIntType, UInt, SIntType, SInt
from .tuple import TupleType, Tuple, tuple_ as tuple_imported
from .bitutils import int2seq

__all__  = ['bit']
__all__ += ['clock', 'reset', 'enable']

__all__ += ['array']
__all__ += ['bits', 'uint', 'sint']

__all__ += ['tuple_']

__all__ += ['concat', 'repeat']
__all__ += ['sext', 'zext']

def convertbit(value, totype, T):
    if isinstance(value, totype):
        return value

    if not isinstance(value, (_BitType, ArrayType, TupleType, IntegerTypes)):
        raise ValueError(
            "bit can only be used on a Bit, an Array, or an int; not {}".format(type(value)))

    if isinstance(value, (ArrayType, TupleType)):
        if len(value) != 1:
            raise ValueError(
            "bit can only be used on arrays and tuples of length 1; not {}".format(len(value)))
        value = value[0]
        if not isinstance(value, _BitType):
            raise ValueError(
                "bit can only be used on arrays and tuples of bits; not {}".format(type(value)))

    assert isinstance(value, (IntegerTypes, _BitType))

    if isinstance(value, IntegerTypes):
        value = VCC if value else GND

    if   value.isinput():  b = In(T)()
    elif value.isoutput(): b = Out(T)()
    else: b = T()
    b.port = value.port
    return b


def bit(value):
    return convertbit(value, BitType, Bit)

def clock(value):
    return convertbit(value, ClockType, Clock)

def reset(value):
    return convertbit(value, ResetType, Reset)

def enable(value):
    return convertbit(value, EnableType, Enable)



def convertbits(value, n, totype, totypeconstructor, checkbit):
    if isinstance(value, totype):
        return value

    if not isinstance(value, (_BitType, TupleType, ArrayType, IntegerTypes, Sequence)):
        raise ValueError(
            "bits can only be used on a Bit, an Array, a Tuple, an int, or a Sequence; not : {}".format(type(value)))

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(),1)
        ts = int2seq(value, n)
    elif isinstance(value, Sequence):
        ts =  list(value)
    elif isinstance(value, _BitType):
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
       # this should be converted to error()
       if checkbit:
            if not isinstance(t, _BitKind):
                raise ValueError(
                    "bits can only be used on Arrays or Tuples containing bits, not : {}".format(type(value)))
       if t != T:
           raise ValueError("All fields in a Array or a Tuple must be the same type : {}".format(Ts))

    assert len(Ts)

    return totypeconstructor(len(Ts), T)(*ts)

def array(value, n=None):
    return convertbits(value, n, ArrayType, Array, False)

def bits(value, n=None):
    return convertbits(value, n, BitsType, Bits, True)

def uint(value, n=None):
    if isinstance(value, SIntType):
        raise ValueError( "uint cannot convert SInt" )
    return convertbits(value, n, UIntType, UInt, True)

def sint(value, n=None):
    if isinstance(value, UIntType):
        raise ValueError( "uint cannot convert SInt" )
    return convertbits(value, n, SIntType, SInt, True)



def concat(*arrays):
    ts = [t for a in arrays for t in a.ts] # flatten
    return array(ts)

def repeat(value, n):
    if isinstance(value, BitType):
        repeats = bits(n*[value])
    else:
        repeats = array(n*[value])
    return repeats

def zext(value, n):
    assert isinstance(value, (UIntType, SIntType, BitsType))
    if isinstance(value, UIntType):
        zeros = uint(0,n)
    elif isinstance(value, SIntType):
        zeros = sint(0,n)
    elif isinstance(value, BitsType):
        zeros = bits(0,n)
    return concat(zeros,value)

def sext(value, n):
    assert isinstance(value, SIntType)
    return sint(concat(array(value[-1], n), array(value)))

def tuple_(value, n=None):
    return tuple_imported(value, n)
