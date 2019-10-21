"""
Defines a subtype of m.Array called m.Bits

m.Bits[N] is roughly equivalent ot m.Array[N, T]
"""
from functools import lru_cache, wraps
import typing as tp
from hwtypes import BitVector
from hwtypes import AbstractBitVector, AbstractBitVectorMeta, AbstractBit, \
    InconsistentSizeError

import magma as m
from .compatibility import IntegerTypes
from .ref import AnonRef
from .bit import Bit, VCC, GND
from .array import Array, ArrayMeta
from .debug import debug_wire
from .t import Type


def _coerce(T: tp.Type['Bits'], val: tp.Any) -> 'Bits':
    if not isinstance(val, Bits):
        return T(val)
    elif len(val) != len(T):
        raise InconsistentSizeError('Inconsistent size')
    else:
        return val


def bits_cast(fn: tp.Callable[['Bits', 'Bits'], tp.Any]) -> \
        tp.Callable[['Bits', tp.Any], tp.Any]:
    @wraps(fn)
    def wrapped(self: 'Bits', other: tp.Any) -> tp.Any:
        other = _coerce(type(self), other)
        return fn(self, other)
    return wrapped


class BitsMeta(AbstractBitVectorMeta, ArrayMeta):
    def __new__(mcs, name, bases, namespace, info=(None, None, None), **kwargs):
        return ArrayMeta.__new__(mcs, name, bases, namespace, info, **kwargs)

    def __getitem__(cls, index):
        if isinstance(index, int):
            index = (index, Bit)
        return ArrayMeta.__getitem__(cls, index)

    def __repr__(cls):
        return str(cls)

    def __str__(cls):
        name = f"{cls.orig_name}[{cls.N}]"
        if cls.is_input():
            name = f"In({name})"
        elif cls.is_output():
            name = f"Out({name})"
        elif cls.is_output():
            name = f"InOut({name})"
        return name


class Bits(Array, AbstractBitVector, metaclass=BitsMeta):
    __hash__ = Array.__hash__

    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'bits([{}])'.format(', '.join(ts))

    def bits(self):
        if not self.const():
            raise Exception("Not a constant")

        def convert(x):
            if x is VCC:
                return True
            assert x is GND
            return False
        return [convert(x) for x in self.ts]

    def __int__(self):
        if not self.const():
            raise Exception("Can't call __int__ on a non-constant")
        return BitVector[len(self)](self.bits()).as_int()

    @debug_wire
    def wire(self, other, debug_info):
        if isinstance(other, IntegerTypes):
            if other.bit_length() > len(self):
                raise ValueError(
                    f"Cannot convert integer {other} "
                    f"(bit_length={other.bit_length()}) to Bits ({len(self)})")
            from .conversions import bits
            other = bits(other, len(self))
        super().wire(other, debug_info)

    @classmethod
    def make_constant(cls, value, num_bits: tp.Optional[int] = None) -> \
            'AbstractBitVector':
        if num_bits is None:
            return cls(value)
        return cls.unsized_t[num_bits](value)

    def __setitem__(self, index: int, value: AbstractBit):
        raise NotImplementedError()

    @classmethod
    @lru_cache(maxsize=None)
    def declare_unary_op(cls, op):
        N = len(cls)
        return m.circuit.DeclareCoreirCircuit(f"magma_Bits_{N}_{op}",
                                              "I", m.In(m.Bits[N]),
                                              "O", m.Out(m.Bits[N]),
                                              coreir_name=op,
                                              coreir_genargs={"width": N},
                                              coreir_lib="coreir")

    @classmethod
    @lru_cache(maxsize=None)
    def declare_binary_op(cls, op):
        N = len(cls)
        return m.circuit.DeclareCoreirCircuit(f"magma_Bits_{N}_{op}",
                                              "I0", m.In(m.Bits[N]),
                                              "I1", m.In(m.Bits[N]),
                                              "O", m.Out(m.Bits[N]),
                                              coreir_name=op,
                                              coreir_genargs={"width": N},
                                              coreir_lib="coreir")

    @classmethod
    @lru_cache(maxsize=None)
    def declare_compare_op(cls, op):
        N = len(cls)
        return m.circuit.DeclareCoreirCircuit(f"magma_Bits_{N}_{op}",
                                              "I0", m.In(m.Bits[N]),
                                              "I1", m.In(m.Bits[N]),
                                              "O", m.Out(m.Bit),
                                              coreir_name=op,
                                              coreir_genargs={"width": N},
                                              coreir_lib="coreir")

    @classmethod
    @lru_cache(maxsize=None)
    def declare_ite(cls, T):
        t_str = str(T)
        # Sanitize
        t_str = t_str.replace("(", "_")
        t_str = t_str.replace(")", "")
        t_str = t_str.replace("[", "_")
        t_str = t_str.replace("]", "")
        N = len(cls)
        return m.circuit.DeclareCoreirCircuit(f"magma_Bits_{N}_ite_{t_str}",
                                              "I0", m.In(T),
                                              "I1", m.In(T),
                                              "S", m.In(m.Bit),
                                              "O", m.Out(T),
                                              coreir_name="mux",
                                              coreir_genargs={"width": N},
                                              coreir_lib="coreir")

    def bvnot(self) -> 'AbstractBitVector':
        return self.declare_unary_op("invert")()(self)

    @bits_cast
    def bvand(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("and")()(self, other)

    @bits_cast
    def bvor(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("or")()(self, other)

    @bits_cast
    def bvxor(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("xor")()(self, other)

    @bits_cast
    def bvshl(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("shl")()(self, other)

    @bits_cast
    def bvlshr(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("lshr")()(self, other)

    def bvashr(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvrol(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvror(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvcomp(self, other) -> 'AbstractBitVector[1]':
        raise NotImplementedError()

    def bveq(self, other) -> AbstractBit:
        return self.declare_compare_op("eq")()(self, other)

    def bvult(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvule(self, other) -> AbstractBit:
        # For wiring
        if self.is_input():
            return Type.__le__(self, other)
        raise NotImplementedError()

    def bvugt(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvuge(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvslt(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvsle(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvsgt(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvsge(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvneg(self) -> 'AbstractBitVector':
        raise NotImplementedError()

    def adc(self, other, carry) -> tp.Tuple['AbstractBitVector', AbstractBit]:
        raise NotImplementedError()

    def ite(self, t_branch, f_branch) -> 'AbstractBitVector':
        type_ = type(t_branch)
        if type_ != type(f_branch):
            raise TypeError("ite expects same type for both branches")
        return self.declare_ite(type_)()(t_branch, f_branch,
                                         self != self.make_constant(0))

    def bvadd(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvsub(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvmul(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvudiv(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvurem(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvsdiv(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvsrem(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def repeat(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def sext(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def ext(self, other) -> 'AbstractBitVector':
        return self.zext(other)

    def zext(self, other) -> 'AbstractBitVector':
        return m.zext(self, other)

    __invert__ = bvnot
    __and__ = bvand
    __or__ = bvor
    __xor__ = bvxor

    __lshift__ = bvshl
    __rshift__ = bvlshr

    __neg__ = bvneg
    __add__ = bvadd
    __sub__ = bvsub
    __mul__ = bvmul
    __floordiv__ = bvudiv
    __mod__ = bvurem

    __eq__ = bveq
    __ne__ = AbstractBitVector.bvne
    __ge__ = bvuge
    __gt__ = bvugt
    __le__ = bvule
    __lt__ = bvult


BitsType = Bits


class UInt(Bits):
    pass


class SInt(Bits):
    pass


class BFloat(Bits):
    pass
