import functools
from collections.abc import Sequence
from .compatibility import IntegerTypes
from .t import In, Out, InOut, Direction
from .digital import Digital
from .bit import Bit, VCC, GND
from .digital import DigitalMeta
from .clock import Clock, Reset, AsyncReset, AsyncResetN, Enable
from .array import Array
from .bits import Bits, UInt, SInt
from .bfloat import BFloat
from .digital import Digital
from .tuple import Tuple, tuple_ as tuple_imported, namedtuple
from .bitutils import int2seq
import magma as m
import hwtypes

__all__ = ['bit']
__all__ += ['clock', 'reset', 'enable', 'asyncreset', 'asyncresetn']

__all__ += ['array']
__all__ += ['bits', 'uint', 'sint']

__all__ += ['tuple_', 'namedtuple']

__all__ += ['concat', 'repeat']
__all__ += ['sext', 'zext']

def can_convert_to_bit(value):
    return isinstance(value, (Digital, Array, Tuple, IntegerTypes))


def can_convert_to_bit_type(value):
    return issubclass(value, (Digital, Array, Tuple))


def convertbit(value, totype):
    if isinstance(value, totype):
        return value

    if not can_convert_to_bit(value):
        raise ValueError(
            "bit can only be used on a Bit, an Array, or an int"
            f"; not {type(value)}")

    if isinstance(value, (Array, Tuple)):
        if len(value) != 1:
            raise ValueError(
                "bit can only be used on arrays and tuples of length 1"
                f"; not {type(value)}")
        value = value[0]
        if not isinstance(value, Digital):
            raise ValueError(
                "bit can only be used on arrays and tuples of bits"
                f"; not {type(value)}")

    assert isinstance(value, (IntegerTypes, Digital))

    if isinstance(value, IntegerTypes):
        value = VCC if value else GND

    if value.is_input():
        b = In(totype)(name=value.name)
    elif value.is_output():
        b = Out(totype)(name=value.name)
    else:
        b = totype()
    b.port = value.port
    return b


def bit(value):
    return convertbit(value, Bit)


def clock(value):
    return convertbit(value, Clock)


def reset(value):
    return convertbit(value, Reset)


def asyncreset(value):
    return convertbit(value, AsyncReset)


def asyncresetn(value):
    return convertbit(value, AsyncResetN)


def enable(value):
    return convertbit(value, Enable)


def convertbits(value, n, totype, checkbit):
    if isinstance(value, totype):
        if n is not None and n != len(value):
            raise ValueError("converting a value should not change the size, use concat, zext, or sext instead.")
        return value

    convertible_types = (Digital, Tuple, Array, IntegerTypes,
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
    elif isinstance(value, Digital):
        if n is None:
            ts = [value]
        elif issubclass(totype, SInt):
            # sext
            ts = n * [value]
        else:
            # zext
            ts = [GND for _ in range(n - 1)] + [value]
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
            if not isinstance(t, DigitalMeta):
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
            Direction.In: In,
            Direction.Out: Out,
            Direction.InOut: InOut
        }[T.direction](Bit)

    return totype[len(Ts), T](*ts)


def array(value, n=None):
    return convertbits(value, n, Array, False)


def bits(value, n=None):
    return convertbits(value, n, Bits, True)


def uint(value, n=None):
    return convertbits(value, n, UInt, True)


def sint(value, n=None):
    return convertbits(value, n, SInt, True)


def bfloat(value, n=None):
    return convertbits(value, n, BFloat, True)


def concat(*arrays):
    ts = []
    for a in arrays:
        if isinstance(a, hwtypes.BitVector):
            ts.extend(a.bits())
        else:
            ts.extend(a.ts)
    return array(ts)


def repeat(value, n):
    if isinstance(value, Bit):
        repeats = bits(n * [value])
    else:
        repeats = array(n * [value])
    return repeats


def check_value_is_not_input(fn):
    @functools.wraps(fn)
    def wrapped(value, n):
        if isinstance(value, m.Type) and not value.is_output():
            raise Exception(f"{fn.__name__} only works with non input values")
        return fn(value, n)
    return wrapped


# @check_value_is_not_input
def zext(value, n):
    assert isinstance(value, (UInt, SInt, Bits)) or \
        isinstance(value, Array) and isinstance(value.T, Digital)
    if isinstance(value, UInt):
        zeros = uint(0, n)
    elif isinstance(value, SInt):
        zeros = sint(0, n)
    elif isinstance(value, Bits):
        zeros = bits(0, n)
    elif isinstance(value, Array):
        zeros = array(0, n)
    result = concat(value, zeros)
    if isinstance(value, UInt):
        return uint(result)
    elif isinstance(value, SInt):
        return sint(result)
    elif isinstance(value, Bits):
        return bits(result)
    return result


# @check_value_is_not_input
def sext(value, n):
    assert isinstance(value, SInt)
    return sint(concat(array(value), array([value[-1]] * n)))


def tuple_(value, n=None):
    return tuple_imported(value, n)
