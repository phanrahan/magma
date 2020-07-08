"""
Defines a subtype of m.Array called m.Bits

m.Bits[N] is roughly equivalent ot m.Array[N, T]
"""
import operator
from functools import lru_cache, wraps
import typing as tp
import hwtypes as ht
from hwtypes import BitVector
from hwtypes import AbstractBitVector, AbstractBitVectorMeta, AbstractBit, \
    InconsistentSizeError
from .compatibility import IntegerTypes
from .ref import AnonRef
from .bit import Bit
from .array import Array, ArrayMeta
from .debug import debug_wire
from .t import Type, Direction, In, Out
from magma.circuit import Circuit, coreir_port_mapping, IO
from magma.family import get_family
from magma.interface import IO
from magma.language_utils import primitive_to_python
from magma.logging import root_logger


_logger = root_logger()


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
        try:
            other = _coerce(type(self), other)
        except TypeError:
            return NotImplemented
        return fn(self, other)
    return wrapped


class BitsMeta(AbstractBitVectorMeta, ArrayMeta):
    def __new__(mcs, name, bases, namespace, info=(None, None, None), **kwargs):
        return ArrayMeta.__new__(mcs, name, bases, namespace, info, **kwargs)

    def __call__(cls, *args, **kwargs):
        result = super().__call__(*args, **kwargs)
        if all(x.is_output() for x in result.ts) and not cls.is_output():
            if cls.is_input() or cls.is_inout():
                raise TypeError("Can't construct output with input/inout")
            # Make it an output
            return cls.qualify(Direction.Out)(*args, **kwargs)
        return result

    def __getitem__(cls, index):
        if isinstance(index, int):
            index = (index, Bit)
        return ArrayMeta.__getitem__(cls, index)

    def __repr__(cls):
        return str(cls)

    def __str__(cls):
        name = getattr(cls, "orig_name", cls.__name__)
        if not cls.is_concrete:
            return name
        # Handle qualified, unsized e.g. In(Bits)
        if isinstance(cls.T, Direction):
            assert cls.N is None
            return f"{cls.T.name}({name})"

        name += f"[{cls.N}]"
        if cls.is_input():
            name = f"In({name})"
        elif cls.is_output():
            name = f"Out({name})"
        elif cls.is_output():
            name = f"InOut({name})"
        return name


class Bits(Array, AbstractBitVector, metaclass=BitsMeta):
    __hash__ = Array.__hash__
    hwtypes_T = ht.BitVector

    def __init__(self, *args, **kwargs):
        if args and len(args) == 1 and isinstance(args[0], Array) and \
                len(self) > 1 and len(args[0]) <= len(self):
            self.ts = args[0].ts[:]
            # zext for promoting width
            for i in range(len(self) - len(args[0])):
                self.ts.append(Bit(0))
            Type.__init__(self, **kwargs)
        else:
            Array.__init__(self, *args, **kwargs)

    def __repr__(self):
        if not self.name.anon():
            return super().__repr__()
        ts = [repr(t) for t in self.ts]
        return 'bits([{}])'.format(', '.join(ts))

    def bits(self):
        if not self.const():
            raise Exception("Not a constant")

        def _convert(x):
            if x is type(x).VCC:
                return True
            assert x is type(x).GND
            return False

        return [_convert(x) for x in self.ts]

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

    @classmethod
    @lru_cache(maxsize=None)
    def declare_unary_op(cls, op):
        N = len(cls)
        python_op_name = primitive_to_python(op)

        class _MagmBitsOp(Circuit):
            name = f"magma_Bits_{N}_{op}"
            coreir_name = op
            coreir_lib = "coreir"
            coreir_genargs = {"width": N}
            renamed_ports = coreir_port_mapping
            primitive = True
            stateful = False

            io = IO(I=In(cls), O=Out(cls))

            def simulate(self, value_store, state_store):
                I = cls.hwtypes_T[N](value_store.get_value(self.I))
                O = int(getattr(operator, python_op_name)(I))
                value_store.set_value(self.O, O)

        return _MagmBitsOp

    @classmethod
    @lru_cache(maxsize=None)
    def declare_binary_op(cls, op):
        N = len(cls)
        python_op_name = primitive_to_python(op)
        python_op = getattr(operator, python_op_name)

        class _MagmBitsOp(Circuit):
            name = f"magma_Bits_{N}_{op}"
            coreir_name = op
            coreir_lib = "coreir"
            coreir_genargs = {"width": N}
            renamed_ports = coreir_port_mapping
            primitive = True
            stateful = False

            io = IO(I0=In(cls), I1=In(cls), O=Out(cls))

            def simulate(self, value_store, state_store):
                I0 = cls.hwtypes_T[N](value_store.get_value(self.I0))
                I1 = cls.hwtypes_T[N](value_store.get_value(self.I1))
                O = int(python_op(I0, I1))
                value_store.set_value(self.O, O)

        return _MagmBitsOp

    @classmethod
    @lru_cache(maxsize=None)
    def declare_compare_op(cls, op):
        N = len(cls)
        python_op_name = primitive_to_python(op)

        class _MagmBitsOp(Circuit):
            name = f"magma_Bits_{N}_{op}"
            coreir_name = op
            coreir_lib = "coreir"
            coreir_genargs = {"width": N}
            renamed_ports = coreir_port_mapping
            primitive = True
            stateful = False

            io = IO(I0=In(cls), I1=In(cls), O=Out(Bit))

            def simulate(self, value_store, state_store):
                I0 = cls.hwtypes_T[N](value_store.get_value(self.I0))
                I1 = cls.hwtypes_T[N](value_store.get_value(self.I1))
                O = int(getattr(operator, python_op_name)(I0, I1))
                value_store.set_value(self.O, O)

        return _MagmBitsOp

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

        class _MagmBitsOp(Circuit):
            name = f"magma_Bits_{N}_ite_{t_str}"
            coreir_name = "mux"
            coreir_lib = "coreir"
            coreir_genargs = {"width": len(T)}
            renamed_ports = coreir_port_mapping
            primitive = True
            stateful = False

            io = IO(I0=In(T), I1=In(T), S=In(Bit), O=Out(T))

            def simulate(self, value_store, state_store):
                I0 = cls.hwtypes_T[N](value_store.get_value(self.I0))
                I1 = cls.hwtypes_T[N](value_store.get_value(self.I1))
                S = ht.Bit(value_store.get_value(self.S))
                O = I1 if S else I0
                value_store.set_value(self.O, O)

        return _MagmBitsOp

    def bvnot(self) -> 'AbstractBitVector':
        return self.declare_unary_op("not")()(self)

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
        return Bits[1](self == other)

    def bveq(self, other) -> AbstractBit:
        return self.declare_compare_op("eq")()(self, other)

    def bvult(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvule(self, other) -> AbstractBit:
        # For wiring
        if not self.is_output():
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
        r = int(other)
        if r <= 0:
            raise ValueError()

        return type(self).unsized_t[r * self.size](r * self.ts)

    def sext(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def ext(self, other) -> 'AbstractBitVector':
        return self.zext(other)

    def zext(self, other) -> 'AbstractBitVector':
        ext = int(other)
        if ext < 0:
            raise ValueError()

        T = type(self).unsized_t
        return self.concat(T[ext](0))

    def __invert__(self):
        return self.bvnot()

    def __and__(self, other):
        try:
            return self.bvand(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __or__(self, other):
        try:
            return self.bvor(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __xor__(self, other):
        try:
            return self.bvxor(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __lshift__(self, other):
        try:
            return self.bvshl(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __rshift__(self, other):
        try:
            return self.bvlshr(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __neg__(self):
        return self.bvneg()

    def __add__(self, other):
        try:
            return self.bvadd(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __sub__(self, other):
        try:
            return self.bvsub(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __mul__(self, other):
        try:
            return self.bvmul(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __floordiv__(self, other):
        try:
            return self.bvudiv(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __truediv__(self, other):
        try:
            return self.bvudiv(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __mod__(self, other):
        try:
            return self.bvurem(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __eq__(self, other):
        try:
            return self.bveq(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __ne__(self, other):
        try:
            return self.bvne(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.bvuge(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.bvugt(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __le__(self, other):
        try:
            return self.bvule(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.bvult(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    @classmethod
    def get_family(cls):
        return get_family()

    @classmethod
    def unflatten(cls, value):
        size = len(value)
        if cls.N != size:
            _logger.warning(f"Using {repr(cls)} to unflatten {size} elements")
        return Bits[size](value)

    def unused(self):
        if self.is_input() or self.is_inout():
            raise TypeError("unused cannot be used with input/inout")
        if not getattr(self, "_magma_unused_", False):
            DefineUnused(len(self))().I.wire(self)
            # "Cache" unused calls so only one is produced
            self._magma_unused_ = True

    def undriven(self):
        if self.is_output() or self.is_inout():
            raise TypeError("undriven cannot be used with output/inout")
        self.wire(DefineUndriven(len(self))().O)

    def __getitem__(self, index):
        if isinstance(index, Bits):
            if len(index) > len(self):
                raise TypeError(f"Unexpected index width: {len(index)}")
            if len(index) < len(self):
                index = index.zext(len(self) - len(index))
            return (self >> index)[0]
        return super().__getitem__(index)


def make_Define(_name, port, direction):
    @lru_cache(maxsize=None)
    def Define(width):
        class _Circuit(Circuit):
            renamed_ports = coreir_port_mapping
            name = _name
            io = IO(**{port: direction(Bits[width])})
            coreir_name = _name
            coreir_lib = "coreir"
            coreir_genargs = {"width": width}
            def simulate(self, value_store, state_store):
                pass

        return _Circuit
    return Define


DefineUndriven = make_Define("undriven", "O", Out)
DefineUnused = make_Define("term", "I", In)


BitsType = Bits


class UInt(Bits):
    hwtypes_T = ht.UIntVector

    def bvneg(self) -> 'AbstractBitVector':
        return self.declare_unary_op("neg")()(self)

    @bits_cast
    def bvult(self, other) -> AbstractBit:
        return self.declare_compare_op("ult")()(self, other)

    @bits_cast
    def bvule(self, other) -> AbstractBit:
        # For wiring
        if self.is_input():
            return Type.__le__(self, other)
        return self.declare_compare_op("ule")()(self, other)

    @bits_cast
    def bvugt(self, other) -> AbstractBit:
        return self.declare_compare_op("ugt")()(self, other)

    @bits_cast
    def bvuge(self, other) -> AbstractBit:
        return self.declare_compare_op("uge")()(self, other)

    @bits_cast
    def bvadd(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("add")()(self, other)

    @bits_cast
    def bvsub(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("sub")()(self, other)

    @bits_cast
    def bvmul(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("mul")()(self, other)

    @bits_cast
    def bvudiv(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("udiv")()(self, other)

    @bits_cast
    def bvurem(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("urem")()(self, other)

    def adc(self, other: 'Bits', carry: Bit) -> tp.Tuple['Bits', Bit]:
        """
        add with carry
        returns a two element tuple of the form (result, carry)
        """
        T = type(self)
        other = _coerce(T, other)
        carry = _coerce(T.unsized_t[1], carry)

        a = self.zext(1)
        b = other.zext(1)
        c = carry.zext(T.size)

        res = a + b + c
        return res[0:-1], res[-1]


class SInt(Bits):
    hwtypes_T = ht.SIntVector

    def __init__(self, *args, **kwargs):
        if args and len(args) == 1 and isinstance(args[0], Array) and \
                len(self) > 1 and len(args[0]) <= len(self):
            self.ts = args[0].ts[:]
            # zext for promoting width
            for i in range(len(self) - len(args[0])):
                self.ts.append(args[0].ts[-1])
            Type.__init__(self, **kwargs)
        else:
            Array.__init__(self, *args, **kwargs)

    @bits_cast
    def bvslt(self, other) -> AbstractBit:
        return self.declare_compare_op("slt")()(self, other)

    @bits_cast
    def bvsle(self, other) -> AbstractBit:
        # For wiring
        if self.is_input():
            return Type.__le__(self, other)
        return self.declare_compare_op("sle")()(self, other)

    @bits_cast
    def bvsgt(self, other) -> AbstractBit:
        return self.declare_compare_op("sgt")()(self, other)

    @bits_cast
    def bvsge(self, other) -> AbstractBit:
        return self.declare_compare_op("sge")()(self, other)

    @bits_cast
    def bvadd(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("add")()(self, other)

    @bits_cast
    def bvsub(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("sub")()(self, other)

    @bits_cast
    def bvmul(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("mul")()(self, other)

    @bits_cast
    def bvsdiv(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("sdiv")()(self, other)

    @bits_cast
    def bvsrem(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("srem")()(self, other)

    def bvneg(self) -> 'AbstractBitVector':
        return self.declare_unary_op("neg")()(self)

    @bits_cast
    def bvashr(self, other) -> 'AbstractBitVector':
        return self.declare_binary_op("ashr")()(self, other)

    def __mod__(self, other):
        try:
            return self.bvsrem(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __floordiv__(self, other):
        try:
            return self.bvsdiv(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __truediv__(self, other):
        try:
            return self.bvsdiv(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.bvsge(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.bvsgt(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __le__(self, other):
        try:
            return self.bvsle(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.bvslt(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def __rshift__(self, other):
        try:
            return self.bvashr(other)
        except InconsistentSizeError as e:
            raise e from None
        except TypeError:
            return NotImplemented

    def adc(self, other: 'Bits', carry: Bit) -> tp.Tuple['Bits', Bit]:
        """
        add with carry
        returns a two element tuple of the form (result, carry)
        """
        T = type(self)
        other = _coerce(T, other)
        carry = _coerce(T.unsized_t[1], carry)

        a = self.sext(1)
        b = other.sext(1)
        c = carry.zext(T.size)

        res = a + b + c
        return res[0:-1], res[-1]

    def ext(self, other):
        return self.sext(other)

    def sext(self, other) -> 'AbstractBitVector':
        ext = int(other)
        if ext < 0:
            raise ValueError()

        T = type(self).unsized_t
        return self.concat(T[ext]([self[-1] for _ in range(ext)]))
