import abc
import copy
import dataclasses
import inspect
import operator
from typing import Callable, List, Optional

from magma.bits import Bits, BitsMeta, SInt, reduce
from magma.conversions import uint, bits, sint
from magma.conversions import concat as bits_concat
from magma.debug import debug_wire
from magma.protocol_type import MagmaProtocolMeta, MagmaProtocol
from magma.t import Direction
from magma.type_utils import TypeTransformer, issint
from magma.value_utils import ValueTransformer, make_selector


def _is_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        return False
    return True


@dataclasses.dataclass(frozen=True)
class Context:
    assignee: '_SmartBitsExpr'
    root: '_SmartExpr'

    @staticmethod
    def _max_width(node):
        if hasattr(node, "_width_"):
            return node._width_
        if isinstance(node, _SmartBitsExpr):
            return len(node.bits)
        return max(Context._max_width(arg) for arg in node.args)

    def max_width(self):
        max_width = Context._max_width(self.root)
        if self.assignee is not None:
            max_width = max(max_width, len(self.assignee.bits))
        return max_width

    def __str__(self):
        return f"Context(lhs={repr(self.assignee)}, rhs={repr(self.root)})"


@dataclasses.dataclass
class Resolution:
    width: Optional[int] = None
    signed: Optional[bool] = None


class Resolutions:
    def __init__(self):
        self._resolutions = {}

    def _get_or_set(self, key):
        return self._resolutions.setdefault(key, Resolution())

    def set(self, key, width: int, signed: bool):
        resolution = self._get_or_set(key)
        resolution.width = width
        resolution.signed = signed

    def set_width(self, key, width: int):
        resolution = self._get_or_set(key)
        resolution.width = width

    def set_signed(self, key, signed: bool):
        resolution = self._get_or_set(key)
        resolution.signed = signed

    def get(self, key) -> Resolution:
        return self._resolutions[key]


class _SmartExprMeta(MagmaProtocolMeta):
    pass


class _SmartExpr(MagmaProtocol, metaclass=_SmartExprMeta):
    @property
    @abc.abstractmethod
    def args(self) -> List['_SmartExpr']:
        raise NotImplementedError()

    @abc.abstractmethod
    def resolve(self, context: Context, resolutions: Resolutions):
        raise NotImplementedError()

    @abc.abstractmethod
    def eval(self, resolutions: Resolutions) -> Bits:
        raise NotImplementedError()

    # Convenience functions on top of resolve() and eval().
    def _resolve_args(self, context: Context, resolutions: Resolutions):
        for arg in self.args:
            arg.resolve(context)

    def _eval_args(self) -> List[Bits]:
        return [arg.eval() for arg in self.args]

    # Binary arithmetic operators.
    def __add__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.add, self, other)

    def __sub__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.sub, self, other)

    def __mul__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.mul, self, other)

    def __floordiv__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.floordiv, self, other)

    def __truediv__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.truediv, self, other)

    def __mod__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.mod, self, other)

    # Binary logic operators.
    def __and__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.and_, self, other)

    def __or__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.or_, self, other)

    def __xor__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartBinaryOp(operator.xor_, self, other)

    # Comparison operators.
    def __eq__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartComparisonOp(operator.eq, self, other)

    def __ne__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartComparisonOp(operator.ne, self, other)

    def __ge__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartComparisonOp(operator.ge, self, other)

    def __gt__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartComparisonOp(operator.gt, self, other)

    def __le__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartComparisonOp(operator.le, self, other)

    def __lt__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartComparisonOp(operator.lt, self, other)

    # Shift operators.
    def __lshift__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartShiftOp(operator.lshift, self, other)

    def __rshift__(self, other: '_SmartExpr'):
        if not isinstance(other, _SmartExpr):
            return NotImplemented
        return _SmartShiftOp(operator.rshift, self, other)

    # Unary operators.
    def __invert__(self):
        return _SmartUnaryOp(operator.invert, self)

    def __neg__(self):
        return _SmartUnaryOp(operator.neg, self)

    # Reduction operators.
    def reduce(self, op):
        return _SmartReductionOp(op, self)

    # Extension operators.
    def zext(self, width):
        return _SmartExtendOp(width, False, self, resolved=False)

    def sext(self, width):
        return _SmartExtendOp(width, True, self, resolved=False)


class _SmartOp(_SmartExpr, metaclass=_SmartExprMeta):
    def __init__(self, op, *args):
        self._op = op
        self._args = args

    @property
    def args(self):
        return self._args

    @property
    def op(self):
        return self._op

    def __str__(self):
        op = self.op.__name__ if inspect.isbuiltin(self.op) else str(self.op)
        args = ", ".join(str(arg) for arg in self.args)
        return f"{op}({args})"


class _SmartExtendOp(_SmartOp):

    @dataclasses.dataclass(frozen=True)
    class _ExtendOp:
        width: int
        signed: bool

        def __call__(self, arg):
            if self._signed:
                return sint(arg).sext(self.width)
            return uint(arg).zext(self.width)

        def __str__(self):
            name = "Sext" if self.signed else "Zext"
            return f"{name}[{self.width}]"

    def __init__(self, width: int, signed: bool, arg: _SmartExpr):
        op = _SmartExtendOp._ExtendOp(width, signed)
        super().__init__(op, arg)

    def resolve(self, context: Context, resolutions: Resolutions):
        context = Context(None, self)
        self._resolve_args(context, resolutions)
        resolution = resolutions.get(self.args[0])
        width = resolution.width + self.op.width
        resolutions.set(self, width, resolution.signed)

    def eval(self, resolutions: Resolutions):
        arg = self.args[0].eval(resolutions)
        return self.op(arg)


class _SmartReductionOp(_SmartOp):
    _OP_TO_NAME = {
        operator.and_: "And",
        operator.or_: "Or",
        operator.xor: "Xor",
    }

    @dataclasses.dataclass(frozen=True)
    class _ReductionOp:
        op: Callable

        def __post_init__(self):
            if self.op not in _SmartReductionOp._OP_TO_NAME:
                raise ValueError(f"Reduction operator {self.op} not supported")

        def __call__(self, arg):
            return reduce(self.op, arg)

        def __str__(self):
            name = _SmartReductionOp._OP_TO_NAME[self.op]
            return f"{name}Reduce"

    def __init__(self, op: Callable, arg: _SmartExpr):
        op = _SmartReductionOp._ReductionOp(op)
        super().__init__(op, arg)

    def resolve(self, context: Context, resolutions: Resolutions):
        context = Context(None, self)
        self._resolve_args(context, resolutions)
        resolution = resolutions.get(self.args[0])
        resolutions.set(self, 1, resolution.signed)

    def eval(self, resolutions: Resolutions):
        resolution = resolutions.get(self)
        cons = sint if resolution.signed else uint
        arg = self.args[0].eval(resolutions)
        return cons(self.op(arg))


class _SmartNAryContextualOp(_SmartOp):
    def resolve(self, context: Context, resolutions: Resolutions):
        self._resolve_args(context, resolutions)
        resolutions = list(map(resolutions.get, self.args))
        width = context.max_width()
        signed = all(resolution.signed for resolution in resolutions)
        resolutions.set(self, width, signed)

    def eval(self, resolutions: Resolutions):
        args = self._eval_args(resolutions)
        resolution = resolutions.get(self)
        if self._signed_:
            args = (sint(arg) for arg in args)
        else:
            args = (uint(arg) for arg in args)
        return self.op(*args)


class _SmartBinaryOp(_SmartNAryContextualOp):
    def __init__(self, op, loperand, roperand):
        super().__init__(op, loperand, roperand)


class _SmartUnaryOp(_SmartNAryContextualOp):
    def __init__(self, op, operand):
        super().__init__(op, operand)


class _SmartComparisonOp(_SmartOp):
    def __init__(self, op, loperand, roperand):
        super().__init__(op, loperand, roperand)

    def resolve(self, context):
        context = Context(None, self)
        self._resolve_args(context)
        signed_args = all(arg._signed_ for arg in self._args)
        to_width = max(arg._width_ for arg in self._args)
        args = (_extend_if_needed(arg, to_width, signed_args)
                for arg in self._args)
        self._update(*args)
        self._width_ = 1
        self._signed_ = False

    def eval(self):
        args = self._eval_args()
        signed_args = all(arg._signed_ for arg in self._args)
        fn = sint if signed_args else uint
        args = (fn(arg) for arg in args)
        return uint(self.op(*args))


class _SmartShiftOp(_SmartOp):
    def __init__(self, op, loperand, roperand):
        super().__init__(op, loperand, roperand)

    def resolve(self, context):
        loperand, roperand = self._args
        loperand.resolve(context)
        self_context = Context(None, self)
        roperand.resolve(self_context)
        to_width = max(arg._width_ for arg in self._args)
        self._signed_ = all(arg._signed_ for arg in self._args)
        args = (_extend_if_needed(arg, to_width, self._signed_)
                for arg in self._args)
        self._update(*args)
        self._width_ = to_width

    def eval(self):
        args = self._eval_args()
        if self._signed_:
            args = (sint(arg) for arg in args)
        else:
            args = (uint(arg) for arg in args)
        return self.op(*args)


class _SmartConcatOp(_SmartOp):

    class _ConcatOp:
        def __call__(self, *args):
            return bits_concat(*args)

        def __str__(self):
            return "Concat"

    def __init__(self, *args):
        concat = _SmartConcatOp._ConcatOp()
        super().__init__(concat, *args)

    def resolve(self, context):
        for arg in self._args:
            context = Context(None, arg)
            arg.resolve(context)
        self._width_ = sum(arg._width_ for arg in self._args)
        self._signed_ = False

    def eval(self):
        args = self._eval_args()
        args = [uint(arg) for arg in args]
        return uint(self.op(*args))


def concat(*args):
    if not all(isinstance(arg, _SmartExpr) for arg in args):
        types = ", ".join(str(type(arg)) for arg in args)
        raise NotImplementedError(f"Concat not supported for {types}")
    return _SmartConcatOp(*args)


class _SmartSignedOp(_SmartOp):

    class _SignedOp:
        def __init__(self, signed):
            self._signed = signed

        @property
        def signed(self):
            return self._signed

        def __str__(self):
            return "Signed" if self._signed else "Unsigned"

    def __init__(self, signed, operand):
        signed = _SmartSignedOp._SignedOp(signed)
        super().__init__(signed, operand)

    def resolve(self, context):
        self._resolve_args(context)
        self._width_ = self._args[0]._width_
        self._signed_ = self._op.signed

    def eval(self):
        args = self._eval_args()
        fn = sint if self._signed_ else uint
        return fn(args[0])


def signed(expr):
    return _SmartSignedOp(True, expr)


def unsigned(expr):
    return _SmartSignedOp(False, expr)


class _SmartBitsExpr(_SmartExpr, metaclass=_SmartExprMeta):
    def __init__(self, bits):
        self._bits = bits

    @property
    def bits(self):
        return self._bits

    def __str__(self):
        return str(self._bits)

    def resolve(self, context):
        self._width_ = len(self._bits)
        self._signed_ = type(self._bits)._signed

    def eval(self):
        return self._bits.typed_value()


class _SmartBitsMeta(_SmartExprMeta):
    def __eq__(cls, other):
        return (
            isinstance(other, _SmartExprMeta) and
            cls._to_magma_() == other._to_magma_()
        )

    __hash__ = type.__hash__

    def __getitem__(cls, key):
        if issubclass(cls, SmartBits) and (hasattr(cls, "_T") or
                                           hasattr(cls, "_signed")):
            raise TypeError("Can not doubly qualify SmartBits, i.e. "
                            "SmartBits[n][m] not allowed")
        signed = False
        if isinstance(key, tuple):
            if len(key) == 1:
                pass
            elif len(key) == 2:
                key, signed = key
            else:
                raise ValueError(f"{key} unsupported")
        if _is_int(key):
            T = Bits[key]
        else:
            assert isinstance(key, BitsMeta)
            T = key
        name = f"SmartBits[{len(T)}, {signed}]"
        dct = {"_T": T, "_signed": signed}
        return type(cls)(name, (cls,), dct)

    def _to_magma_(cls):
        return cls._T

    def _qualify_magma_(cls, d):
        return SmartBits[cls._T.qualify(d), cls._signed]

    def _flip_magma_(cls):
        return SmartBits[cls._T.flip(), cls._signed]

    def _from_magma_value_(cls, value):
        return cls(value)

    def __repr__(cls):
        has_T = hasattr(cls, "_T")
        has_signed = hasattr(cls, "_signed")
        if not (has_T or has_signed):
            return "SmartBits"
        assert has_T and has_signed
        return f"SmartBits[{len(cls._T)}, {cls._signed}]"


class SmartBits(_SmartBitsExpr, metaclass=_SmartBitsMeta):
    def __init__(self, value=None):
        super().__init__(self)
        if value is None:
            value = type(self)._to_magma_()()
        self._value = value

    def typed_value(self):
        if type(self)._signed:
            return sint(self._value)
        return uint(self._value)

    def untyped_value(self):
        return self._value

    def __hash__(self):
        return hash(self._value)

    def _get_magma_value_(self):
        return self.untyped_value()

    def __deepcopy__(self, memo):
        return type(self)(self._value)

    @debug_wire
    def wire(self, other, debug_info):
        if isinstance(other, Bits):
            super().wire(other, debug_info)
            return
        if not isinstance(other, _SmartExpr):
            raise ValueError(f"Can not wire {type(self)} to {type(other)}")
        evaluated, resolved = _eval(self, other)
        evaluated = evaluated.force_width(len(self))
        MagmaProtocol.wire(self, evaluated)
        self._smart_expr_ = resolved  # attach debug info

    def __len__(self):
        return len(type(self)._T)

    def force_width(self, width):
        diff = len(self) - width
        if diff == 0:
            return copy.deepcopy(self)
        value = self.typed_value()
        value = value.ext(-diff) if diff < 0 else value[:-diff]
        return SmartBits.from_bits(value)

    @staticmethod
    def from_bits(value):
        assert isinstance(value, Bits), type(value)
        signed = isinstance(value, SInt)
        return SmartBits[len(value), signed](value)

    def __str__(self):
        signed = type(self)._signed
        return f"SmartBits[{len(self)}, {signed}]({str(self._value)})"

    def connection_iter(self):
        yield from zip(self, self.trace())


SmartBit = SmartBits[1]


def _eval(lhs: SmartBits, rhs: _SmartExpr) -> (SmartBits, _SmartExpr):
    rhs = copy.deepcopy(rhs)
    rhs.resolve(Context(lhs, rhs))
    res = rhs.eval()
    return SmartBits.from_bits(res), rhs


def eval(expr: _SmartExpr, width: int, signed: bool = False):
    lhs = SmartBits[width, signed]()
    lhs @= expr
    return lhs


class _SmartifyTypeTransformer(TypeTransformer):
    def visit_Bits(self, T):
        signed = issint(T)
        return SmartBits[len(T), signed]


class _InitializeSmartValueTransformer(ValueTransformer):
    def __init__(self, value):
        self._value = value

    def visit_Bits(self, value):
        sel = make_selector(value)
        init = sel.select(self._value)
        signed = issint(type(value))
        return SmartBits[len(value), signed](init)


def make_smart(value):
    Tsmart = _SmartifyTypeTransformer().visit(type(value))
    Tsmart = Tsmart.qualify(Direction.Undirected)
    smart_value = Tsmart()
    return _InitializeSmartValueTransformer(value).visit(smart_value)
