import abc
import dataclasses
import inspect
import operator
from typing import Any, Callable, Optional, Union

from magma.bit import Bit
from magma.bits import Bits, BitsMeta, SInt, reduce as bits_reduce
from magma.conversions import uint, bits, sint
from magma.conversions import concat as bits_concat
from magma.debug import debug_wire
from magma.protocol_type import MagmaProtocolMeta, MagmaProtocol
from magma.ref import AnonRef


class SmartExprMeta(MagmaProtocolMeta):
    pass


class SmartExpr(MagmaProtocol, metaclass=SmartExprMeta):
    __hash__ = object.__hash__

    def __init__(self):
        self._name = AnonRef()
        self._value = None

    @property
    def name(self):
        if self._value is None:
            return self._name
        return self._value.name

    @name.setter
    def name(self, value):
        if self._value is None:
            self._name = value
        else:
            self._value.name = value

    @property
    @abc.abstractmethod
    def args(self):
        raise NotImplementedError()

    # Binary arithmetic operators.
    def __add__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.add, self, other)

    def __sub__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.sub, self, other)

    def __mul__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.mul, self, other)

    def __floordiv__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.floordiv, self, other)

    def __truediv__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.truediv, self, other)

    def __mod__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.mod, self, other)

    # Binary logic operators.
    def __and__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.and_, self, other)

    def __or__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.or_, self, other)

    def __xor__(self, other: 'SmartExpr') -> 'SmartBinaryOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.xor, self, other)

    # Comparison operators.
    def __eq__(self, other: 'SmartExpr') -> 'SmartComparisonOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.eq, self, other)

    def __ne__(self, other: 'SmartExpr') -> 'SmartComparisonOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.ne, self, other)

    def __ge__(self, other: 'SmartExpr') -> 'SmartComparisonOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.ge, self, other)

    def __gt__(self, other: 'SmartExpr') -> 'SmartComparisonOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.gt, self, other)

    def __le__(self, other: 'SmartExpr') -> 'SmartComparisonOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.le, self, other)

    def __lt__(self, other: 'SmartExpr') -> 'SmartComparisonOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.lt, self, other)

    # Shift operators.
    def __lshift__(self, other: 'SmartExpr') -> 'SmartShiftOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartShiftOp(operator.lshift, self, other)

    def __rshift__(self, other: 'SmartExpr') -> 'SmartShiftOp':
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartShiftOp(operator.rshift, self, other)

    # Unary operators.
    def __invert__(self) -> 'SmartUnaryOp':
        return SmartUnaryOp(operator.invert, self)

    def __neg__(self) -> 'SmartUnaryOp':
        return SmartUnaryOp(operator.neg, self)

    # Reduction operators.
    def reduce(self, op) -> 'SmartReductionOp':
        return SmartReductionOp(op, self)

    def reduce_and(self) -> 'SmartReductionOp':
        return self.reduce(operator.and_)

    def reduce_or(self) -> 'SmartReductionOp':
        return self.reduce(operator.or_)

    def reduce_xor(self) -> 'SmartReductionOp':
        return self.reduce(operator.xor)

    # Extension operators.
    def zext(self, width) -> 'SmartExtendOp':
        return SmartExtendOp(width, False, self)

    def sext(self, width) -> 'SmartExtendOp':
        return SmartExtendOp(width, True, self)

    def const(self) -> bool:
        return False


class SmartOp(SmartExpr, metaclass=SmartExprMeta):
    def __init__(self, op, *args):
        super().__init__()
        self._op = op
        self._args = args

    @property
    def op(self):
        return self._op

    @property
    def args(self):
        return self._args

    def __str__(self):
        op = self.op.__name__ if inspect.isbuiltin(self.op) else str(self.op)
        args = ", ".join(str(arg) for arg in self.args)
        return f"{op}({args})"


class SmartExtendOp(SmartOp):

    @dataclasses.dataclass(frozen=True)
    class Op:
        width: int
        signed: bool

        def __call__(self, operand: Bits) -> Bits:
            if self.signed:
                return sint(operand).sext(self.width)
            return uint(operand).zext(self.width)

        def __str__(self):
            func = "Sext" if self.signed else "Zext"
            return f"{func}[{self.width}]"

    def __init__(self, width, signed, operand):
        super().__init__(SmartExtendOp.Op(width, signed), operand)


class SmartReductionOp(SmartOp):
    OP_TO_NAME = {
        operator.and_: "And",
        operator.or_: "Or",
        operator.xor: "Xor",
    }

    @dataclasses.dataclass(frozen=True)
    class Op:
        op: Callable

        def __post_init__(self):
            if self.op not in SmartReductionOp.OP_TO_NAME:
                raise ValueError(f"Reduction operator {op} not supported")

        def __call__(self, operand: Bits) -> Bits:
            return bits(bits_reduce(self.op, operand))

        def __str__(self):
            func = SmartReductionOp.OP_TO_NAME[self.op]
            return f"{func}Reduce"

    def __init__(self, op, operand):
        super().__init__(SmartReductionOp.Op(op), operand)


class SmartNAryContextualOp(SmartOp):
    pass


class SmartBinaryOp(SmartNAryContextualOp):
    def __init__(self, op, loperand, roperand):
        super().__init__(op, loperand, roperand)


class SmartUnaryOp(SmartNAryContextualOp):
    def __init__(self, op, operand):
        super().__init__(op, operand)


class SmartComparisonOp(SmartOp):

    @dataclasses.dataclass(frozen=True)
    class Op:
        op: Callable

        def __call__(self, *args) -> Bits:
            return bits(self.op(*args))

        def __str__(self) -> str:
            return self.op.__name__

    def __init__(self, op, loperand, roperand):
        super().__init__(SmartComparisonOp.Op(op), loperand, roperand)


class SmartShiftOp(SmartOp):
    def __init__(self, op, loperand, roperand):
        super().__init__(op, loperand, roperand)


class SmartConcatOp(SmartOp):

    class Op:
        def __call__(self, *args) -> Bits:
            return bits_concat(*args)

        def __str__(self) -> str:
            return "Concat"

    def __init__(self, *args):
        super().__init__(SmartConcatOp.Op(), *args)


class SmartMuxOp(SmartOp):

    class Op:
        def __call__(self, *args) -> Bits:
            import magma as m
            values, select = args[:-1], args[-1]
            return m.mux(values, select)

        def __str__(self) -> str:
            return "Mux"

    def __init__(self, *args):
        super().__init__(SmartMuxOp.Op(), *args)


def concat(*args) -> SmartExpr:
    if not all(isinstance(arg, SmartExpr) for arg in args):
        types = ", ".join(str(type(arg)) for arg in args)
        raise NotImplementedError(f"Concat not supported for [{types}]")
    return SmartConcatOp(*args)


def repeat(value, num) -> SmartExpr:
    """Repeats @value @num number of times flat. Note that for single bit values
    (e.g. x[0]) this is the same as m.repeat, but for bits this function retruns
    a flattened type, whereas m.repeat constructs a higher-dimensional
    array. This function is equivalent to m.smart.concat(*(value for _ in
    range(num))).
    """
    return concat(*(value for _ in range(num)))


def mux(values, select) -> SmartExpr:
    if not all(isinstance(value, SmartExpr) for value in values):
        types = ", ".join(str(type(value)) for value in values)
        raise NotImplementedError(f"Mux not supported for [{types}]")
    return SmartMuxOp(*values, select)


class SmartSignedOp(SmartOp):

    @dataclasses.dataclass
    class Op:
        signed: bool

        def __call__(self, operand: Bits) -> Bits:
            cons = sint if self.signed else uint
            return cons(operand)

        def __str__(self):
            return "Signed" if self.signed else "Unsigned"

    def __init__(self, signed, operand):
        super().__init__(SmartSignedOp.Op(signed), operand)


def signed(expr):
    return SmartSignedOp(True, expr)


def unsigned(expr):
    return SmartSignedOp(False, expr)


@dataclasses.dataclass(frozen=True)
class SmartBitsExpr(SmartExpr, metaclass=SmartExprMeta):
    bits: 'SmartBits'

    @property
    def args(self):
        return []

    def __str__(self):
        return str(self.bits)


class SmartBitsMeta(SmartExprMeta):
    def _parse_key(cls, key):
        qualified = (
            issubclass(cls, SmartBits) and
            (
                hasattr(cls, "_T_") or
                hasattr(cls, "_signed_")
            )
        )
        if qualified:
            raise TypeError("Can not doubly qualify SmartBits")
        width_or_type = key
        signed = False
        if isinstance(key, tuple):
            if len(key) == 1:
                width_or_type = key[0]
            elif len(key) == 2:
                width_or_type, signed = key
            else:
                raise ValueError(f"{key} unsupported")
        try:
            int(width_or_type)
        except (ValueError, TypeError):
            assert isinstance(width_or_type, BitsMeta)
            T = width_or_type
        else:
            T = Bits[width_or_type]
        return T, signed

    def __eq__(cls, other):
        return (
            isinstance(other, SmartExprMeta) and
            cls._to_magma_() == other._to_magma_()
        )

    __hash__ = type.__hash__

    def __getitem__(cls, key):
        T, signed = SmartBitsMeta._parse_key(cls, key)
        name = f"SmartBits[{len(T)}, {signed}]"
        dct = {"_T_": T, "_signed_": signed}
        return type(cls)(name, (cls,), dct)

    def _to_magma_(cls):
        return cls._T_

    def _qualify_magma_(cls, d):
        return SmartBits[cls._T_.qualify(d), cls._signed_]

    def _flip_magma_(cls):
        return SmartBits[cls._T_.flip(), cls._signed_]

    def _from_magma_value_(cls, value):
        return cls(value)

    def __repr__(cls):
        has_T = hasattr(cls, "_T_")
        has_signed = hasattr(cls, "_signed_")
        if not (has_T or has_signed):
            return "SmartBits"
        assert has_T and has_signed
        return f"SmartBits[{len(cls._T_)}, {cls._signed_}]"


def _make_initializer(
        value: Optional[Any],
        T: SmartBitsMeta,
        name: Optional[str]
) -> Bits:
    if value is None:
        return T._to_magma_()(name=name)
    size = len(T._T_)
    if isinstance(value, Bits[size]):
        return value
    return Bits[size](value)


class SmartBits(SmartBitsExpr, metaclass=SmartBitsMeta):
    def __init__(self, value=None, name=None):
        super().__init__(self)
        self._value = _make_initializer(value, type(self), name)

    def __len__(self):
        return len(type(self)._T_)

    def typed_value(self):
        if type(self)._signed_:
            return sint(self._value)
        return uint(self._value)

    def untyped_value(self):
        return self._value

    def __hash__(self):
        return hash(self._value)

    def _get_magma_value_(self):
        return self.untyped_value()

    # Slice operators.
    def __getitem__(self, key_or_slice) -> 'SmartBits':
        return SmartBits.from_bits(self._value[key_or_slice])

    @debug_wire
    def wire(self, other, debug_info):
        if isinstance(other, Bits):
            MagmaProtocol.wire(self, other, debug_info)
            return
        if not isinstance(other, SmartExpr):
            raise ValueError(f"Can not wire {type(self)} to {type(other)}")
        # NOTE(rsetaluri): We delay the import of the evaluation method to avoid
        # a circular import, since the evaluation depends on the implementation
        # of SmartBits.
        from magma.smart.eval import evaluate_assignment
        other = evaluate_assignment(self, other)
        MagmaProtocol.wire(self, other, debug_info)

    @staticmethod
    def from_bits(value):
        if isinstance(value, Bit):
            value = bits(value)
        if not isinstance(value, Bits):
            raise TypeError(value)
        signed = isinstance(value, SInt)
        return SmartBits[len(value), signed](value)

    def __str__(self):
        signed = type(self)._signed_
        return f"SmartBits[{len(self)}, {signed}]({str(self._value)})"

    def connection_iter(self):
        yield from zip(self, self.trace())


SmartBit = SmartBits[1]


def issigned(value_or_type: Union[SmartBits, SmartBitsMeta]) -> bool:
    if isinstance(value_or_type, SmartBits):
        return type(value_or_type)._signed_
    if isinstance(value_or_type, SmartBitsMeta):
        return value_or_type._signed_
    raise TypeError(value_or_type)


def eval(expr: SmartExpr, width: int, signed: bool = False):
    lhs = SmartBits[width, signed]()
    lhs @= expr
    return lhs
