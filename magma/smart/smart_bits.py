import abc
import copy
import enum
import inspect
import operator
from typing import Dict

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


class Type(enum.Enum):
    UNSIGNED = enum.auto()
    SIGNED = enum.auto()

    @staticmethod
    def make(signed: bool) -> 'Type':
        return Type.SIGNED if signed else Type.UNSIGNED

    @property
    def signed(self) -> bool:
        return self is Type.SIGNED


class Context:
    def __init__(self, assignee, root):
        self.assignee = assignee
        self.root = root

    def max_width(self):

        def _visit(node):
            if hasattr(node, "_width_"):
                return node._width_
            if isinstance(node, _SmartBitsExpr):
                return len(node.bits)
            return max(_visit(arg) for arg in node.args)

        max_width = _visit(self.root)
        if self.assignee is not None:
            max_width = max(max_width, len(self.assignee.bits))
        return max_width

    def __str__(self):
        return f"Context(lhs={repr(self.assignee)}, rhs={repr(self.root)})"


class _SmartExprMeta(MagmaProtocolMeta):
    pass


class _SmartExpr(MagmaProtocol, metaclass=_SmartExprMeta):
    __hash__ = object.__hash__

    @property
    @abc.abstractmethod
    def args(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def resolve(self, context):
        raise NotImplementedError()

    @abc.abstractmethod
    def eval(self):
        raise NotImplementedError()

    #@abc.abstractmethod
    def result_size(self, *sizes) -> int:
        raise NotImplementedError()

    #@abc.abstractmethod
    def result_type(self, *types) -> Type:
        raise NotImplementedError()

    #@abc.abstractmethod
    def propagate_size(self, lhs, expr, sizes):
        raise NotImplementedError()

    #@abc.abstractmethod
    def eval2(self, sizes, types) -> Bits:
        raise NotImplementedError()

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

    def _update(self, *args):
        self._args = args

    def _resolve_args(self, context):
        for arg in self._args:
            arg.resolve(context)

    def _eval_args(self):
        return [arg.eval() for arg in self._args]

    def __str__(self):
        if inspect.isbuiltin(self._op):
            op_str = self._op.__name__
        else:
            op_str = str(self._op)
        args = ", ".join(str(arg) for arg in self._args)
        return f"{op_str}({args})"


class _SmartExtendOp(_SmartOp):

    class _ExtendOp:
        def __init__(self, width, signed):
            self._width = width
            self._signed = signed

        def __call__(self, operand):
            if self._signed:
                return sint(operand).sext(self._width)
            return uint(operand).zext(self._width)

        def __str__(self):
            return f"Extend[width={self._width}, signed={self._signed}]"

    def __init__(self, width, signed, operand, resolved=True):
        extend = _SmartExtendOp._ExtendOp(width, signed)
        super().__init__(extend, operand)
        self._resolved = resolved

    def resolve(self, context):
        if self._resolved:
            return
        context = Context(None, self)
        self._resolve_args(context)
        self._width_ = self._args[0]._width_ + self.op._width
        self._signed_ = self.op._signed

    def eval(self):
        args = self._eval_args()
        return self.op(*args)


def _extend_if_needed(expr, to_width, signed):
    diff = expr._width_ - to_width
    assert diff <= 0
    if diff == 0:
        return expr
    expr = _SmartExtendOp(-diff, signed, expr)
    expr._width_ = to_width
    expr._signed_ = signed
    return expr


class _SmartReductionOp(_SmartOp):

    class _ReductionOp:
        _OP_TO_NAME = {
            operator.and_: "And",
            operator.or_: "Or",
            operator.xor: "Xor",
        }

        def __init__(self, op):
            cls = _SmartReductionOp._ReductionOp
            if op not in cls._OP_TO_NAME:
                raise ValueError(f"Reduction operator {op} not supported")
            self._op = op

        def __call__(self, operand):
            return reduce(self._op, operand)

        def __str__(self):
            cls = _SmartReductionOp._ReductionOp
            op_name = cls._OP_TO_NAME[self._op]
            return f"{op_name}Reduce"

    def __init__(self, op, operand):
        reduction = _SmartReductionOp._ReductionOp(op)
        super().__init__(reduction, operand)

    def resolve(self, context):
        context = Context(None, self)
        self._resolve_args(context)
        self._width_ = 1
        self._signed_ = all(arg._signed_ for arg in self._args)

    def eval(self):
        args = self._eval_args()
        fn = sint if self._signed_ else uint
        return fn(self.op(*args))

    def result_size(self, *sizes) -> int:
        return 1

    def result_type(self, *types) -> Type:
        return Type.make(False)

    def propagate_size(self, lhs, expr, sizes):
        self.args[0].propagate_size(None, None, sizes)

    def eval2(self, sizes, types):
        args = (arg.eval2(sizes, types) for arg in self.args)
        args = list(args)
        print ("@", args, list(map(type, args)))
        cons = sint if types[self].signed else uint
        return cons(self.op(*args))


class _SmartNAryContextualOp(_SmartOp):
    def __init__(self, op, *args):
        super().__init__(op, *args)

    def resolve(self, context):
        self._resolve_args(context)
        self._signed_ = all(arg._signed_ for arg in self._args)
        to_width = context.max_width()
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

    def result_size(self, *sizes) -> int:
        return max(sizes)

    def result_type(self, *types) -> Type:
        return Type.make(all(type.signed for type in types))

    def propagate_size(self, lhs, expr, sizes):
        size = sizes[self]
        if lhs is not None:
            size = max(len(lhs), size)
        if expr is not None:
            size = max(sizes[expr], size)
        sizes[self] = size
        for arg in self.args:
            arg.propagate_size(lhs, self, sizes)

    def eval2(self, sizes, types):
        args = (arg.eval2(sizes, types) for arg in self.args)
        args = (
            (
                arg.ext(sizes[self] - len(arg))
                if sizes[self] > len(arg)
                else arg
            )
            for arg in args
        )
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

    def result_size(self, *sizes) -> int:
        return 1

    def result_type(self, *types) -> Type:
        return Type.make(False)

    def propagate_size(self, lhs, expr, sizes):
        sizes[self] = max(sizes[arg] for arg in self.args)
        for arg in self.args:
            arg.propagate_size(None, self, sizes)

    def eval2(self, sizes, types):
        args = (arg.eval2(sizes, types) for arg in self.args)
        args = list(args)
        return bits(self.op(*args))


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

    def result_size(self, *sizes) -> int:
        return sizes[0]

    def result_type(self, *types) -> Type:
        return Type.make(all(type.signed for type in types))

    def propagate_size(self, lhs, expr, sizes):
        size = max(sizes[arg] for arg in self.args)
        if lhs is not None:
            size = max(size, len(lhs))
        sizes[self] = size
        self.args[0].propagate_size(lhs, self, sizes)
        self.args[1].propagate_size(None, self, sizes)

    def eval2(self, sizes, types):
        larg, rarg = (arg.eval2(sizes, types) for arg in self.args)
        diff = len(larg) - len(rarg)
        assert diff >= 0
        if diff > 0:
            rarg = rarg.ext(diff)
        return self.op(larg, rarg)


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

    def result_size(self, *sizes) -> int:
        return sum(sizes)

    def result_type(self, *types) -> Type:
        return Type.make(False)

    def propagate_size(self, lhs, expr, sizes):
        for arg in self.args:
            arg.propagate_size(None, None, sizes)

    def eval2(self, sizes, types):
        args = (arg.eval2(sizes, types) for arg in self.args)
        return self.op(*args)


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

    def result_size(self, *sizes) -> int:
        return sizes[0]

    def result_type(self, *types) -> Type:
        return Type.make(self._op.signed)

    def propagate_size(self, lhs, expr, sizes):
        self.args[0].propagate_size(lhs, expr, sizes)

    def eval2(self, sizes, types):
        cons = sint if self._op.signed else uint
        return cons(self.args[0].eval2(sizes, types))


def signed(expr):
    return _SmartSignedOp(True, expr)


def unsigned(expr):
    return _SmartSignedOp(False, expr)


class _SmartBitsExpr(_SmartExpr, metaclass=_SmartExprMeta):
    def __init__(self, bits):
        self._bits = bits

    @property
    def args(self):
        return []

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

    def result_size(self) -> int:
        return len(self._bits)

    def result_type(self) -> Type:
        return Type.make(type(self._bits)._signed)

    def propagate_size(self, lhs, expr, sizes):
        size = sizes[self]
        if lhs is not None:
            size = max(len(lhs), size)
        if expr is not None:
            size = max(sizes[expr], size)
        sizes[self] = size

    def eval2(self, sizes, types):
        diff = sizes[self] - len(self)
        assert diff >= 0
        evaluation = self._bits.typed_value()
        if diff > 0:
            evaluation = evaluation.ext(diff)
        return evaluation


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
        result = _evaluate_assignment(self, other)
        result = result.force_width(len(self))
        MagmaProtocol.wire(self, result)

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


def _result_types(expr: _SmartExpr, types: Dict[_SmartExpr, int]):
    for arg in expr.args:
        _result_types(arg, types)
    types[expr] = expr.result_type(*(types[arg] for arg in expr.args))


def result_types(expr: _SmartExpr) -> Dict[_SmartExpr, int]:
    types = {}
    _result_types(expr, types)
    return types


def _result_sizes(expr: _SmartExpr, sizes: Dict[_SmartExpr, int]):
    for arg in expr.args:
        _result_sizes(arg, sizes)
    sizes[expr] = expr.result_size(*(sizes[arg] for arg in expr.args))


def result_sizes(expr: _SmartExpr) -> Dict[_SmartExpr, int]:
    sizes = {}
    _result_sizes(expr, sizes)
    return sizes


def _evaluate_assignment(lhs: SmartBits, rhs: _SmartExpr) -> SmartBits:
    sizes = result_sizes(rhs)
    types = result_types(rhs)
    rhs.propagate_size(lhs, None, sizes)
    result = rhs.eval2(sizes, types)
    return SmartBits.from_bits(result)


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
