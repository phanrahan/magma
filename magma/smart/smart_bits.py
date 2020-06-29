import abc
import dataclasses
import operator

from magma.bits import Bits, BitsMeta
from magma.conversions import uint
from magma.debug import debug_wire
from magma.protocol_type import MagmaProtocolMeta, MagmaProtocol


def _is_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        return False
    return True


class _SmartBitsMeta(MagmaProtocolMeta):
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


@dataclasses.dataclass
class _SmartExprContext:
    max_operand_width: int = -1

    def consume(self, expr):
        self.max_operand_width = max(self.max_operand_width,
                                     expr.max_operand_width())


class _SmartExpr(abc.ABC):
    @abc.abstractmethod
    def resolve(self, context: _SmartExprContext):
        raise NotImplementedError()


class _SmartBitsExpr(_SmartExpr):
    def __init__(self, bits):
        self._bits = bits

    def resolve(self, context: _SmartExprContext):
        return self._bits

    def max_operand_width(self, ):
        return len(self._bits)


class _SmartOpExpr(_SmartExpr):
    def __init__(self, op, *args):
        self._op = op
        self._args = args

    def resolve(self, context: _SmartExprContext):
        args = [arg.resolve(context) for arg in self._args]
        args = [arg._force_width(context.max_operand_width) for arg in args]
        args = [arg._get_magma_value_() for arg in args]
        args = [uint(arg) for arg in args]
        result = self._op(*args)
        return SmartBits._make(result)

    def max_operand_width(self):
        return max(arg.max_operand_width() for arg in self._args)


def _make_expr(op, *args):
    promote = lambda a: a if isinstance(a, _SmartExpr) else _SmartBitsExpr(a)
    args = map(promote, args)
    return _SmartOpExpr(op, *args)


class SmartBits(MagmaProtocol, metaclass=_SmartBitsMeta):
    def __init__(self, value=None):
        if value is None:
            value = type(self)._to_magma_()()
        self._value = value

    def _get_magma_value_(self):
        return self._value

    def __add__(self, other):
        assert isinstance(other, SmartBits)
        return _make_expr(operator.add, self, other)

    def __le__(self, other):
        assert isinstance(other, SmartBits)
        return _make_expr(operator.le, self, other)

    def __lshift__(self, other):
        assert isinstance(other, SmartBits)
        return _make_expr(operator.lshift, self, other)

    def __invert__(self):
        return _make_expr(operator.invert, self)

    @debug_wire
    def wire(self, other, debug_info):
        if isinstance(other, SmartBits):
            rhs = other._force_width(len(self))
            MagmaProtocol.wire(self, rhs)
        elif isinstance(other, _SmartExpr):
            context = _SmartExprContext()
            context.consume(_SmartBitsExpr(self))
            # Pre-process rhs of assignment into context.
            context.consume(other)
            resolved = other.resolve(context)
            self.wire(resolved)
        else:
            raise ValueError(f"Can not wire {type(self)} to {type(other)}")

    def __len__(self):
        return len(type(self)._T)

    def _force_width(self, width):
        diff = len(self) - width
        if diff == 0:
            return self
        value = self._get_magma_value_()
        value = value.zext(-diff) if diff < 0 else value[:-diff]
        return SmartBits._make(value)

    @staticmethod
    def _make(value):
        assert isinstance(value, Bits)
        return SmartBits[len(value)](value)


class SmartBit(SmartBits[1]):
    pass
