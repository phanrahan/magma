import abc
import copy
import dataclasses
import inspect
import operator
from typing import Tuple

from magma.bits import Bits, BitsMeta, SInt, reduce
from magma.common import MroVisitor
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


class Context:
    def __init__(self, assignee, root):
        self.assignee = assignee
        self.root = root

    def max_width(self):

        def _visit(node):
            if hasattr(node, "_width_"):
                return node._width_
            if isinstance(node, SmartBitsExpr):
                return len(node.bits)
            return max(_visit(arg) for arg in node.args)

        max_width = _visit(self.root)
        if self.assignee is not None:
            max_width = max(max_width, len(self.assignee.bits))
        return max_width

    def __str__(self):
        return f"Context(lhs={repr(self.assignee)}, rhs={repr(self.root)})"


class SmartExprMeta(MagmaProtocolMeta):
    pass


class SmartExpr(MagmaProtocol, metaclass=SmartExprMeta):
    __hash__ = object.__hash__

    @property
    @abc.abstractmethod
    def args(self):
        raise NotImplementedError()

    # Binary arithmetic operators.
    def __add__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.add, self, other)

    def __sub__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.sub, self, other)

    def __mul__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.mul, self, other)

    def __floordiv__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.floordiv, self, other)

    def __truediv__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.truediv, self, other)

    def __mod__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.mod, self, other)

    # Binary logic operators.
    def __and__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.and_, self, other)

    def __or__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.or_, self, other)

    def __xor__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartBinaryOp(operator.xor_, self, other)

    # Comparison operators.
    def __eq__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.eq, self, other)

    def __ne__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.ne, self, other)

    def __ge__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.ge, self, other)

    def __gt__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.gt, self, other)

    def __le__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.le, self, other)

    def __lt__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartComparisonOp(operator.lt, self, other)

    # Shift operators.
    def __lshift__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartShiftOp(operator.lshift, self, other)

    def __rshift__(self, other: 'SmartExpr'):
        if not isinstance(other, SmartExpr):
            return NotImplemented
        return SmartShiftOp(operator.rshift, self, other)

    # Unary operators.
    def __invert__(self):
        return SmartUnaryOp(operator.invert, self)

    def __neg__(self):
        return SmartUnaryOp(operator.neg, self)

    # Reduction operators.
    def reduce(self, op):
        return SmartReductionOp(op, self)

    # Extension operators.
    def zext(self, width):
        return SmartExtendOp(width, False, self, resolved=False)

    def sext(self, width):
        return SmartExtendOp(width, True, self, resolved=False)


class SmartOp(SmartExpr, metaclass=SmartExprMeta):
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

    def __str__(self):
        if inspect.isbuiltin(self._op):
            op_str = self._op.__name__
        else:
            op_str = str(self._op)
        args = ", ".join(str(arg) for arg in self.args)
        return f"{op_str}({args})"


class SmartExtendOp(SmartOp):

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
        extend = SmartExtendOp._ExtendOp(width, signed)
        super().__init__(extend, operand)
        self._resolved = resolved

    @property
    def resolved(self):
        return self._resolved


def _extend_if_needed(expr, to_width, signed):
    diff = expr._width_ - to_width
    assert diff <= 0
    if diff == 0:
        return expr
    expr = SmartExtendOp(-diff, signed, expr)
    expr._width_ = to_width
    expr._signed_ = signed
    return expr


class SmartReductionOp(SmartOp):

    class _ReductionOp:
        _OP_TO_NAME = {
            operator.and_: "And",
            operator.or_: "Or",
            operator.xor: "Xor",
        }

        def __init__(self, op):
            cls = SmartReductionOp._ReductionOp
            if op not in cls._OP_TO_NAME:
                raise ValueError(f"Reduction operator {op} not supported")
            self._op = op

        def __call__(self, operand):
            return reduce(self._op, operand)

        def __str__(self):
            cls = SmartReductionOp._ReductionOp
            op_name = cls._OP_TO_NAME[self._op]
            return f"{op_name}Reduce"

    def __init__(self, op, operand):
        reduction = SmartReductionOp._ReductionOp(op)
        super().__init__(reduction, operand)


class SmartNAryContextualOp(SmartOp):
    def __init__(self, op, *args):
        super().__init__(op, *args)


class SmartBinaryOp(SmartNAryContextualOp):
    def __init__(self, op, loperand, roperand):
        super().__init__(op, loperand, roperand)


class SmartUnaryOp(SmartNAryContextualOp):
    def __init__(self, op, operand):
        super().__init__(op, operand)


class SmartComparisonOp(SmartOp):
    def __init__(self, op, loperand, roperand):
        super().__init__(op, loperand, roperand)


class SmartShiftOp(SmartOp):
    def __init__(self, op, loperand, roperand):
        super().__init__(op, loperand, roperand)


class SmartConcatOp(SmartOp):

    class _ConcatOp:
        def __call__(self, *args):
            return bits_concat(*args)

        def __str__(self):
            return "Concat"

    def __init__(self, *args):
        concat = SmartConcatOp._ConcatOp()
        super().__init__(concat, *args)


def concat(*args):
    if not all(isinstance(arg, SmartExpr) for arg in args):
        types = ", ".join(str(type(arg)) for arg in args)
        raise NotImplementedError(f"Concat not supported for {types}")
    return SmartConcatOp(*args)


class SmartSignedOp(SmartOp):

    class _SignedOp:
        def __init__(self, signed):
            self._signed = signed

        @property
        def signed(self):
            return self._signed

        def __str__(self):
            return "Signed" if self._signed else "Unsigned"

    def __init__(self, signed, operand):
        signed = SmartSignedOp._SignedOp(signed)
        super().__init__(signed, operand)


def signed(expr):
    return SmartSignedOp(True, expr)


def unsigned(expr):
    return SmartSignedOp(False, expr)


class SmartBitsExpr(SmartExpr, metaclass=SmartExprMeta):
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


class SmartBitsMeta(SmartExprMeta):
    def __eq__(cls, other):
        return (
            isinstance(other, SmartExprMeta) and
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


class SmartBits(SmartBitsExpr, metaclass=SmartBitsMeta):
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
        if not isinstance(other, SmartExpr):
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


@dataclasses.dataclass(frozen=True)
class _SmartExprNode:
    expr: SmartExpr
    children: Tuple['_SmartExprNode']

    @staticmethod
    def make_tree(expr: SmartExpr):
        children = tuple(_SmartExprNode.make_tree(arg) for arg in expr.args)
        return _SmartExprNode(expr, children)


class _SmartExprNodeVisitor(MroVisitor):
    def _get_cls(self, node: _SmartExprNode) -> type:
        return super()._get_cls(node.expr)

    def generic_visit(self, node: _SmartExprNode, *args, **kwargs):
        return [self.visit(child, *args, **kwargs) for child in node.children]


class _Resolver(_SmartExprNodeVisitor):
    def visit_SmartExtendOp(self, node: SmartExtendOp, context: Context):
        if node.expr.resolved:
            return
        self.generic_visit(node, Context(None, expr))
        node.expr._width_ = node.expr.args[0]._width_ + node.expr.op._width
        node.expr._signed_ = node.expr.op._signed

    def visit_SmartReductionOp(self, node: SmartReductionOp, context: Context):
        self.generic_visit(node, Context(None, node.expr))
        node.expr._width_ = 1
        node.expr._signed_ = all(arg._signed_ for arg in node.expr.args)

    def visit_SmartNAryContextualOp(self, node: SmartNAryContextualOp, context: Context):
        self.generic_visit(node, context)
        node.expr._signed_ = all(arg._signed_ for arg in node.expr.args)
        to_width = context.max_width()
        args = (_extend_if_needed(arg, to_width, node.expr._signed_)
                for arg in node.expr.args)
        node.expr._update(*args)
        node.expr._width_ = to_width

    def visit_SmartComparisonOp(self, node: SmartComparisonOp, context: Context):
        self.generic_visit(node, Context(None, node.expr))
        signed_args = all(arg._signed_ for arg in node.expr.args)
        to_width = max(arg._width_ for arg in node.expr.args)
        args = (_extend_if_needed(arg, to_width, signed_args)
                for arg in node.expr.args)
        node.expr._update(*args)
        node.expr._width_ = 1
        node.expr._signed_ = False

    def visit_SmartShiftOp(self, node: SmartShiftOp, context: Context):
        loperand, roperand = node.children
        self.visit(loperand, context)
        self.visit(roperand, Context(None, node.expr))
        to_width = max(arg._width_ for arg in node.expr.args)
        node.expr._signed_ = all(arg._signed_ for arg in node.expr.args)
        args = (_extend_if_needed(arg, to_width, node.expr._signed_)
                for arg in node.expr.args)
        node.expr._update(*args)
        node.expr._width_ = to_width

    def visit_SmartConcatOp(self, node: SmartConcatOp, context: Context):
        for child in node.children:
            self.visit(child, Context(None, child.expr))
        node.expr._width_ = sum(arg._width_ for arg in node.expr.args)
        node.expr._signed_ = False

    def visit_SmartSignedOp(self, node: SmartSignedOp, context: Context):
        self.generic_visit(node, context)
        node.expr._width_ = node.expr.args[0]._width_
        node.expr._signed_ = node.expr._op.signed

    def visit_SmartBitsExpr(self, node: SmartBitsExpr, context: Context):
        node.expr._width_ = len(node.expr._bits)
        node.expr._signed_ = type(node.expr._bits)._signed


class _Evaluator(_SmartExprNodeVisitor):
    def visit_SmartExtendOp(self, node: SmartExtendOp) -> Bits:
        args = self.generic_visit(node)
        return node.expr.op(*args)

    def visit_SmartReductionOp(self, node: SmartReductionOp) -> Bits:
        args = self.generic_visit(node)
        fn = sint if node.expr._signed_ else uint
        return fn(node.expr.op(*args))

    def visit_SmartNAryContextualOp(self, node: SmartNAryContextualOp) -> Bits:
        args = self.generic_visit(node)
        if node.expr._signed_:
            args = (sint(arg) for arg in args)
        else:
            args = (uint(arg) for arg in args)
        return node.expr.op(*args)

    def visit_SmartComparisonOp(self, node: SmartComparisonOp) -> Bits:
        args = self.generic_visit(node)
        signed_args = all(arg._signed_ for arg in node.expr.args)
        fn = sint if signed_args else uint
        args = (fn(arg) for arg in args)
        return uint(node.expr.op(*args))

    def visit_SmartShiftOp(self, node: SmartShiftOp) -> Bits:
        args = self.generic_visit(node)
        if node.expr._signed_:
            args = (sint(arg) for arg in args)
        else:
            args = (uint(arg) for arg in args)
        return node.expr.op(*args)

    def visit_SmartConcatOp(self, node: SmartConcatOp) -> Bits:
        args = self.generic_visit(node)
        args = [uint(arg) for arg in args]
        return uint(node.expr.op(*args))

    def visit_SmartSignedOp(self, node: SmartSignedOp) -> Bits:
        args = self.generic_visit(node)
        fn = sint if node.expr._signed_ else uint
        return fn(args[0])

    def visit_SmartBitsExpr(self, node: SmartBitsExpr) -> Bits:
        return node.expr._bits.typed_value()


def _eval(lhs: SmartBits, rhs: SmartExpr) -> (SmartBits, SmartExpr):
    rhs = copy.deepcopy(rhs)
    root = _SmartExprNode.make_tree(rhs)
    _Resolver().visit(root, Context(lhs, rhs))
    # NOTE(rsetaluri): We need to re-construct the tree since args of expr's
    # might have changed during resolution (e.g. through insertion of extension
    # nodes).
    root = _SmartExprNode.make_tree(rhs)
    res = _Evaluator().visit(root)
    return SmartBits.from_bits(res), rhs


def eval(expr: SmartExpr, width: int, signed: bool = False):
    lhs = SmartBits[width, signed]()
    lhs @= expr
    return lhs


class SmartifyTypeTransformer(TypeTransformer):
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
    Tsmart = SmartifyTypeTransformer().visit(type(value))
    Tsmart = Tsmart.qualify(Direction.Undirected)
    smart_value = Tsmart()
    return _InitializeSmartValueTransformer(value).visit(smart_value)
