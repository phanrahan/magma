import functools
from collections import Sequence
from .compatibility import IntegerTypes
from .t import In, Out, InOut, INPUT, OUTPUT, INOUT
from .bit import _BitKind, _BitType, Bit, BitType, VCC, GND
from .clock import ClockType, Clock, \
    Reset, ResetType, \
    AsyncReset, AsyncResetType, \
    Enable, EnableType
from .array import ArrayType, Array, ArrayKind
from .bits import BitsType, Bits, UIntType, UInt, SIntType, SInt, UIntKind, \
    SIntKind, BFloat
from .tuple import TupleType, tuple_ as tuple_imported, TupleKind, namedtuple
from .bitutils import int2seq
import magma as m

__all__ = ['bit']
__all__ += ['clock', 'reset', 'enable', 'asyncreset']

__all__ += ['array']
__all__ += ['bits', 'uint', 'sint']

__all__ += ['tuple_', 'namedtuple']

__all__ += ['concat', 'repeat']
__all__ += ['sext', 'zext']


def can_convert_to_bit(value):
    return isinstance(value, (_BitType, ArrayType, TupleType, IntegerTypes))


def can_convert_to_bit_type(value):
    return isinstance(value, (_BitKind, ArrayKind, TupleKind))


def convertbit(value, totype, T):
    if isinstance(value, totype):
        return value

    if not can_convert_to_bit(value):
        raise ValueError(
            "bit can only be used on a Bit, an Array, or an int"
            f"; not {type(value)}")

    if isinstance(value, (ArrayType, TupleType)):
        if len(value) != 1:
            raise ValueError(
                "bit can only be used on arrays and tuples of length 1"
                f"; not {type(value)}")
        value = value[0]
        if not isinstance(value, _BitType):
            raise ValueError(
                "bit can only be used on arrays and tuples of bits"
                f"; not {type(value)}")

    assert isinstance(value, (IntegerTypes, _BitType))

    if isinstance(value, IntegerTypes):
        value = VCC if value else GND

    if value.isinput():
        b = In(T)(name=value.name)
    elif value.isoutput():
        b = Out(T)(name=value.name)
    else:
        b = T()
    b.port = value.port
    return b


def bit(value):
    return convertbit(value, BitType, Bit)


def clock(value):
    return convertbit(value, ClockType, Clock)


def reset(value):
    return convertbit(value, ResetType, Reset)


def asyncreset(value):
    return convertbit(value, AsyncResetType, AsyncReset)


def enable(value):
    return convertbit(value, EnableType, Enable)


def convertbits(value, n, totype, totypeconstructor, checkbit):
    if isinstance(value, totype):
        if n is not None and n != len(value):
            raise ValueError("converting a value should not change the size, use concat, zext, or sext instead.")
        return value

    convertible_types = (_BitType, TupleType, ArrayType, IntegerTypes,
                         Sequence)
    if not isinstance(value, convertible_types):
        raise ValueError(
            "bits can only be used on a Bit, an Array, a Tuple, an int, or a"
            f" Sequence; not : {type(value)}"
        )

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(), 1)
        ts = int2seq(value, n)
    elif isinstance(value, Sequence):
        ts = list(value)
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

    convert_to_bit = False
    # check that they are all the same
    for t in Ts:
        if checkbit:
            if not isinstance(t, _BitKind):
                raise ValueError(
                    "bits can only be used on Arrays or Tuples containing bits"
                    f", not : {t}")
        if t != T:
            if can_convert_to_bit_type(t) and can_convert_to_bit_type(T):
                # If they can all be converted to Bit, then that's okay
                convert_to_bit = True
            else:
                raise ValueError(
                    "All fields in a Array or a Tuple must be the same type"
                    f"got {t} expected {T}")

    assert len(Ts)

    if convert_to_bit is True:
        ts = [bit(t) for t in ts]
        T = {
            INPUT: In,
            OUTPUT: Out,
            INOUT: InOut
        }[T.direction](Bit)

    return totypeconstructor[len(Ts), T](*ts)


def array(value, n=None):
    return convertbits(value, n, ArrayType, Array, False)


def bits(value, n=None):
    return convertbits(value, n, BitsType, Bits, True)


def uint(value, n=None):
    if isinstance(value, SIntType):
        raise ValueError("uint cannot convert SInt")
    return convertbits(value, n, UIntType, UInt, True)


def sint(value, n=None):
    if isinstance(value, UIntType):
        raise ValueError("uint cannot convert SInt")
    return convertbits(value, n, SIntType, SInt, True)


def bfloat(value, n=None):
    return convertbits(value, n, BFloat, BFloat, True)


def concat(*arrays):
    ts = [t for a in arrays for t in a.ts]  # flatten
    return array(ts)


def repeat(value, n):
    if isinstance(value, BitType):
        repeats = bits(n * [value])
    else:
        repeats = array(n * [value])
    return repeats


def check_value_is_not_input(fn):
    @functools.wraps(fn)
    def wrapped(value, n):
        if isinstance(value, m.Type) and not value.isoutput():
            raise Exception(f"{fn.__name__} only works with non input values")
        return fn(value, n)
    return wrapped


# @check_value_is_not_input
def zext(value, n):
    assert isinstance(value, (UIntType, SIntType, BitsType)) or \
        isinstance(value, ArrayType) and isinstance(value.T, _BitKind)
    if isinstance(value, UIntType):
        zeros = uint(0, n)
    elif isinstance(value, SIntType):
        zeros = sint(0, n)
    elif isinstance(value, BitsType):
        zeros = bits(0, n)
    elif isinstance(value, ArrayType):
        zeros = array(0, n)
    result = concat(value, zeros)
    if isinstance(value, UIntType):
        return uint(result)
    elif isinstance(value, SIntType):
        return sint(result)
    elif isinstance(value, BitsType):
        return bits(result)
    return result


# @check_value_is_not_input
def sext(value, n):
    assert isinstance(value, SIntType)
    return sint(concat(array(value), array(value[-1], n)))


def tuple_(value, n=None):
    return tuple_imported(value, n)
