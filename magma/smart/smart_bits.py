import abc
import dataclasses
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


@dataclasses.dataclass
class _SmartExprContext:
    max_operand_width: int = -1

    def consume(self, expr):
        self.max_operand_width = max(self.max_operand_width,
                                     expr.max_operand_width())


class _SmartExprMeta(MagmaProtocolMeta):
    pass


class _SmartOpExprMeta(_SmartExprMeta):
    pass


class _SmartBitsExprMeta(_SmartExprMeta):
    pass


class _SmartExpr(MagmaProtocol, metaclass=_SmartExprMeta):
    def __add__(self, other):
        assert isinstance(other, _SmartExpr)
        return _SmartOpExpr(operator.add, self, other)

    def __le__(self, other):
        assert isinstance(other, _SmartExpr)
        return _SmartOpExpr(operator.le, self, other)

    def __lshift__(self, other):
        assert isinstance(other, _SmartExpr)
        return _SmartOpExpr(operator.lshift, self, other)

    def __invert__(self):
        return _SmartOpExpr(operator.invert, self)

    @abc.abstractmethod
    def resolve(self, context: _SmartExprContext):
        raise NotImplementedError()

    @abc.abstractmethod
    def max_operand_width(self):
        pass


class _SmartOpExpr(_SmartExpr, metaclass=_SmartOpExprMeta):
    def __init__(self, op, *args):
        self._op = op
        self._args = args

    def resolve(self, context: _SmartExprContext):
        args = [arg.resolve(context) for arg in self._args]
        args = [arg.force_width(context.max_operand_width) for arg in args]
        args = [arg._get_magma_value_() for arg in args]
        args = [uint(arg) for arg in args]
        result = bits(self._op(*args))
        return SmartBits.make(result)

    def max_operand_width(self):
        return max(arg.max_operand_width() for arg in self._args)


class _SmartBitsExpr(_SmartExpr, metaclass=_SmartBitsExprMeta):
    def __init__(self, bits):
        self._bits = bits

    def resolve(self, context: _SmartExprContext):
        return self._bits

    def max_operand_width(self):
        return len(self._bits)


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
        if isinstance(other, SmartBits):
            rhs = other.force_width(len(self))
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


class SmartBit(SmartBits[1]):
    pass
