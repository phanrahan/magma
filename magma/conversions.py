import functools
from collections import OrderedDict
from collections.abc import Sequence, Mapping
from .compatibility import IntegerTypes
from .t import Type, In, Out, InOut, Direction
from .digital import Digital
from .bit import Bit
from .bits import Bits
from .digital import DigitalMeta
from .clock import Clock, Reset, AsyncReset, AsyncResetN, Enable
from .array import Array
from .bits import Bits, UInt, SInt
from .bfloat import BFloat
from .digital import Digital
from .tuple import Tuple, Product
from .protocol_type import magma_type, magma_value
from .bitutils import int2seq
import hwtypes as ht

__all__ = ['bit']
__all__ += ['clock', 'reset', 'enable', 'asyncreset', 'asyncresetn']

__all__ += ['array']
__all__ += ['bits', 'uint', 'sint']

__all__ += ['tuple_', 'namedtuple']

__all__ += ['concat', 'repeat']
__all__ += ['sext', 'zext', 'sext_to', 'sext_by', 'zext_to', 'zext_by']
__all__ += ['replace']
__all__ += ['as_bits', 'from_bits']

def can_convert_to_bit(value):
    return isinstance(magma_value(value), (Digital, Array, Tuple, IntegerTypes))


def can_convert_to_bit_type(value):
    return issubclass(magma_type(value), (Digital, Array, Tuple))


def convertbit(value, totype):
    value = magma_value(value)
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
        # Just return VCC or GND here, otherwise we lose VCC/GND singleton
        # invariant
        return totype(1) if value else totype(0)

    if value.is_input():
        b = In(totype)(name=value.name)
    elif value.is_output():
        b = Out(totype)(name=value.name)
    else:
        b = totype()
    b._wire = value._wire
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

    value = magma_value(value)
    convertible_types = (Digital, Tuple, Array, IntegerTypes,
                         Sequence, ht.BitVector)
    if not isinstance(value, convertible_types):
        raise ValueError(
            "bits can only be used on a Bit, an Array, a Tuple, an int, or a"
            f" Sequence; not : {type(value)}"
        )

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(), 1)
        ts = int2seq(value, n)
    elif isinstance(value, ht.BitVector):
        ts = value.bits()
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
            ts = [value] + [Bit(0) for _ in range(n - 1)]
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
            if not isinstance(magma_type(t), DigitalMeta):
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

    value = totype[len(Ts), T](ts)
    if n is not None and len(value) < n:
        value = value.ext_to(n)
    return value


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
        if isinstance(a, ht.BitVector):
            ts.extend(a.bits())
        elif isinstance(magma_value(a), Bit):
            ts.extend([a])
        elif isinstance(a, (bool, ht.Bit)):
            ts.extend([Bit(a)])
        else:
            if not isinstance(a, Array):
                raise TypeError(
                    "concat expects values of type Array, BitVector, Bit, or "
                    f"bool, not {a} with type {type(a)}"
                )
            ts.extend(a.ts)
    return array(ts)


def repeat(value, n):
    if isinstance(magma_value(value), Bit):
        repeats = bits(n * [value])
    else:
        repeats = array(n * [value])
    return repeats


def check_value_is_not_input(fn):
    @functools.wraps(fn)
    def wrapped(value, n):
        if isinstance(value, Type) and not value.is_output():
            raise Exception(f"{fn.__name__} only works with non input values")
        return fn(value, n)
    return wrapped


# @check_value_is_not_input
def zext(value, n):
    """Extend `value` by `n` zeros"""
    assert isinstance(value, (UInt, SInt, Bits)) or \
        isinstance(value, Array) and issubclass(value.T, Digital)
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


def zext_by(value, n):
    """Extend `value` by `n` zeros"""
    return zext(value, n)


def zext_to(value, n):
    """Extend `value` to length `n` with zeros"""
    return zext(value, n - len(value))


# @check_value_is_not_input
def sext(value, n):
    """Extend `value` by `n` replications of the msb (`value[-1]`)"""
    assert isinstance(value, SInt)
    return sint(concat(array(value), array([value[-1]] * n)))


def sext_by(value, n):
    """Extend `value` by `n` replications of the msb (`value[-1]`)"""
    return sext(value, n)


def sext_to(value, n):
    """Extend `value` to length `n` by replicating the msb (`value[-1]`)"""
    return sext(value, n - len(value))


from .bitutils import int2seq
from .array import Array
from .bit import Digital, Bit


#
# convert value to a tuple
#   *value = tuple from positional arguments
#   **kwargs = tuple from keyword arguments
#
def _tuple(value, n=None, t=Tuple):
    if isinstance(value, t):
        return value

    if not isinstance(magma_value(value),
                      (Digital, Array, IntegerTypes, Sequence, Mapping)):
        raise ValueError(
            "bit can only be used on a Bit, an Array, or an int; not {}".format(type(value)))

    decl = OrderedDict()
    args = []

    if isinstance(value, IntegerTypes):
        if n is None:
            n = max(value.bit_length(),1)
        value = int2seq(value, n)
    elif isinstance(magma_value(value), Digital):
        value = [value]
    elif isinstance(value, Array):
        value = [value[i] for i in range(len(value))]

    if isinstance(value, Sequence):
        ts = list(value)
        for i in range(len(ts)):
            args.append(ts[i])
            decl[i] = type(ts[i])
    elif isinstance(value, Mapping):
        for k, v in value.items():
            args.append(v)
            decl[k] = type(v)
    for a, d in zip(args, decl):
        # bool types to Bit
        if issubclass(decl[d], (bool, ht.Bit)):
            decl[d] = Digital
        # Promote integer types to Bits
        elif decl[d] in IntegerTypes:
            decl[d] = Bits[max(a.bit_length(), 1)]
        elif issubclass(decl[d], ht.BitVector):
            decl[d] = Bits[len(decl[d])]

    if t == Tuple:
        return t[tuple(decl.values())](*args)
    assert t == Product
    return t.from_fields("anon", decl)(*args)


def namedtuple(**kwargs):
    return _tuple(kwargs, t=Product)


def product(**kwargs):
    return _tuple(kwargs, t=Product)


def tuple_(value, n=None):
    return _tuple(value, n)


def replace(value, others: dict):
    value = magma_value(value)
    if isinstance(value, Product):
        d = dict(value.items())
        d.update(others)
        return namedtuple(**d)
    elif isinstance(value, Tuple):
        a = value.values()
        for idx, v in others.items():
            a[int(idx)] = v
        return tuple_(a)
    elif isinstance(value, Array):
        l = value.as_list()
        for idx, v in others.items():
            l[int(idx)] = v
        return array(l)
    else:
        raise ValueError("replace can only be used with an Array, a Tuple, or Product")


def _dispatch(cls, dispatch, *args, **kwargs):
    mro = cls.mro()
    for dispatch_cls in mro:
        fn = dispatch.registry.get(dispatch_cls, None)
        if fn is not None:
            return fn(*args, **kwargs)
    raise NotImplementedError()


def as_bits(value):
    return bits(value.flatten())


def from_bits(cls, value):
    ts = value.ts
    return cls.unflatten(ts)
