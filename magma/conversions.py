from collections import Sequence
from .compatibility import IntegerTypes
from .bit import BitKind, BitType, BitOut, VCC, GND
from .array import ArrayType, Array, BitsType, Bits, UIntType, UInt, SIntType, SInt
from .tuple import Tuple
from .bits import int2seq

__all__  = ['bit']
__all__ += ['array']
__all__ += ['bits', 'uint', 'sint']
__all__ += ['tuple_']

def bit(value):
    if not isinstance(value, (BitType, ArrayType, BitsType, UIntType, SIntType, IntegerTypes)):
        raise ValueError(
            "bit can only be used with a Bit, Array, Bits, UInt, SInt, or int, not : {}".format(type(value)))

    if isinstance(value, (ArrayType, BitsType, UIntType, SIntType)):
        assert len(value) == 1
        value = value[0]

    if isinstance(value, IntegerTypes):
        value = VCC if value else GND

    assert isinstance(value, BitType)

    return value


def convertbits(value, n, totype, checkbit):
    if not isinstance(value, (BitType, ArrayType, BitsType, UIntType, SIntType, IntegerTypes, Sequence)):
        raise ValueError(
            "bits can only be used with a Bit, Array, Bits, UInt, SInt, int, or Sequence, not : {}".format(type(value)))

    if not isinstance(value, (IntegerTypes, BitType)):
        assert n is None

    if isinstance(value, int):
        if n is None:
            n = value.bit_length()
        ts = int2seq(value, n)
    elif isinstance(value, Sequence):
        ts =  list(value)
    elif isinstance(value, BitType):
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
            T = BitOut
        Ts.append(T)

    # check that they are all the same
    for t in Ts:
       # make this test optional ...
       if checkbit:
           assert isinstance(t, BitKind)
       assert t == T

    return totype(len(Ts), T)(*ts)

# not exported because it has a different interface than array.array
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
    return convertbits(value, n, UInt, True)

def sint(value, n=None):
    if isinstance(value, SIntType):
        return value
    return convertbits(value, n, SInt, True)


def tuple_(*larg, **kwargs):
    decl = []
    args = []
    n = len(larg)
    if n > 0:
        assert n % 2 == 0
        for i in range(0, n, 2):
            K = larg[i]
            t = larg[i+1]
            T = type(t)
            if T in IntegerTypes:
                T = BitOut
            decl.append(K)
            decl.append(T)
            args.append(t)
    else:
        for K, t in kwargs.items():
            T = type(t)
            if T in IntegerTypes:
                T = BitOut
            decl.append(K)
            decl.append(T)
            args.append(t)
    return Tuple(*decl)(*args)

