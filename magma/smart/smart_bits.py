import abc
import copy
import enum
import inspect
import operator

from magma.bits import Bits, BitsMeta
from magma.conversions import uint, bits
from magma.debug import debug_wire
from magma.protocol_type import MagmaProtocolMeta, MagmaProtocol


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
            if isinstance(node, _SmartBitsExpr):
                return len(node.bits)
            return max(_visit(arg) for arg in node.args)

        max_width = _visit(self.root)
        if self.assignee is not None:
            max_width = max(max_width, len(self.assignee.bits))
        return max_width


class _SmartExprMeta(MagmaProtocolMeta):
    pass


class _SmartOpExprMeta(_SmartExprMeta):
    pass


class _SmartBitsExprMeta(_SmartExprMeta):
    pass


class Determination(enum.Enum):
    SELF_DETERMINED = enum.auto()
    CONTEXT_DETERMINED = enum.auto()


class _SmartExpr(MagmaProtocol, metaclass=_SmartExprMeta):
    def __init__(self, determination):
        self._determination = determination

    @abc.abstractmethod
    def resolve(self):
        raise NotImplementedError()

    @property
    def determination(self):
        return self._determination

    def __add__(self, other):
        assert isinstance(other, _SmartExpr)
        return _SmartBinaryOpExpr(operator.add, self, other)

    def __le__(self, other):
        assert isinstance(other, _SmartExpr)
        return _SmartComparisonOpExpr(operator.le, self, other)

    def __lshift__(self, other):
        assert isinstance(other, _SmartExpr)
        return _SmartShiftOpExpr(operator.lshift, self, other)

    def __invert__(self):
        return _SmartUnaryOpExpr(operator.invert, self)


class _SmartOpExpr(_SmartExpr, metaclass=_SmartOpExprMeta):
    def __init__(self, determination, op, *args):
        super().__init__(determination)
        self._op = op
        self._args = tuple(args)

    @property
    def args(self):
        return self._args

    @property
    def op(self):
        return self._op

    def _update(self, *args):
        self._args = tuple(args)

    def __str__(self):
        if inspect.isbuiltin(self._op):
            op_str = self._op.__name__
        else:
            op_str = str(self._op)
        args = ", ".join(str(arg) for arg in self._args)
        return f"{str(op_str)}({args})"


class _SmartExtendOpExpr(_SmartOpExpr):

    class _Extend:
        def __init__(self, width):
            self._width = width

        def __call__(self, operand):
            return operand.zext(self._width)

        def __str__(self):
            return f"Extend[{self._width}]"

    def __init__(self, width, operand):
        extend = _SmartExtendOpExpr._Extend(width)
        super().__init__(Determination.SELF_DETERMINED, extend, operand)


def _extend_if_needed(expr, to_width):
    diff = expr._width_ - to_width
    assert diff <= 0
    if diff == 0:
        return expr
    expr = _SmartExtendOpExpr(-diff, expr)
    expr._width_ = to_width
    return expr


class _SmartBinaryOpExpr(_SmartOpExpr):
    def __init__(self, op, loperand, roperand):
        super().__init__(Determination.CONTEXT_DETERMINED,
                         op, loperand, roperand)

    def resolve(self, context):
        for arg in self._args:
            arg.resolve(context)
        to_width = context.max_width()
        args = (_extend_if_needed(arg, to_width) for arg in self._args)
        self._update(*args)
        self._width_ = to_width


class _SmartUnaryOpExpr(_SmartOpExpr):
    def __init__(self, op, operand):
        super().__init__(Determination.CONTEXT_DETERMINED, op, operand)

    def resolve(self, context):
        raise NotImplementedError()


class _SmartComparisonOpExpr(_SmartOpExpr):
    def __init__(self, op, loperand, roperand):
        super().__init__(Determination.SELF_DETERMINED,
                         op, loperand, roperand)

    def resolve(self, context):
        context = Context(None, self)
        for arg in self._args:
            arg.resolve(context)
        to_width = max(arg._width_ for arg in self._args)
        args = (_extend_if_needed(arg, to_width) for arg in self._args)
        self._update(*args)
        self._width_ = 1


class _SmartShiftOpExpr(_SmartOpExpr):
    def __init__(self, op, loperand, roperand):
        super().__init__(Determination.CONTEXT_DETERMINED,
                         op, loperand, roperand)

    def resolve(self, context):
        raise NotImplementedError()


class _SmartBitsExpr(_SmartExpr, metaclass=_SmartBitsExprMeta):
    def __init__(self, bits):
        super().__init__(Determination.SELF_DETERMINED)
        self._bits = bits

    @property
    def bits(self):
        return self._bits

    def __str__(self):
        return str(self._bits)

    def resolve(self, context):
        self._width_ = len(self._bits)


class _SmartBitsMeta(_SmartBitsExprMeta):
    def __getitem__(cls, key):
        assert cls is SmartBits
        if _is_int(key):
            T = Bits[key]
        else:
            assert isinstance(key, BitsMeta)
            T = key
        width = len(T)
        return type(cls)(f"SmartBits[{width}]", (cls,), {"_T": T})

    def _to_magma_(cls):
        return cls._T

    def _qualify_magma_(cls, d):
        return SmartBits[cls._T.qualify(d)]

    def _flip_magma_(cls):
        return SmartBits[cls._T.flip()]

    def _from_magma_value_(cls, value):
        return cls(value)

    def __repr__(cls):
        return f"SmartBits[{len(cls._T)}]"


class SmartBits(_SmartBitsExpr, metaclass=_SmartBitsMeta):
    def __init__(self, value=None):
        super().__init__(self)
        if value is None:
            value = type(self)._to_magma_()()
        self._value = value

    def _get_magma_value_(self):
        return self._value

    @debug_wire
    def wire(self, other, debug_info):
        if not isinstance(other, _SmartExpr):
            raise ValueError(f"Can not wire {type(self)} to {type(other)}")
        evaluated = _eval(self, other)
        evaluated = evaluated.force_width(len(self))
        MagmaProtocol.wire(self, evaluated)

    def __len__(self):
        return len(type(self)._T)

    def force_width(self, width):
        diff = len(self) - width
        if diff == 0:
            return self
        value = self._get_magma_value_()
        value = value.zext(-diff) if diff < 0 else value[:-diff]
        return SmartBits.make(value)

    @staticmethod
    def make(value):
        assert isinstance(value, Bits)
        return SmartBits[len(value)](value)

    def __str__(self):
        return f"SmartBits[{len(self)}]({str(self._value)})"


class SmartBit(SmartBits[1]):
    pass


def _eval(lhs, rhs):
    assert isinstance(lhs, SmartBits)
    assert isinstance(rhs, _SmartExpr)

    rhs = copy.deepcopy(rhs)
    rhs.resolve(Context(lhs, rhs))

    print (rhs)

    def __eval(node):
        if isinstance(node, _SmartBitsExpr):
            return node
        if isinstance(node, _SmartOpExpr):
            args = (__eval(arg) for arg in node.args)
            args = (uint(arg.bits._get_magma_value_()) for arg in args)
            raw = node.op(*args)
            return SmartBits.make(bits(raw))
        raise NotImplementedError(node)
        #return SmartBits.make(Bits[len(lhs)](0))

    return __eval(rhs)
