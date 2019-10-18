import typing as tp
import functools
from hwtypes.bit_vector_abc import AbstractBit, TypeFamily
from .t import Direction
from .digital import Digital, DigitalMeta, VCC, GND, HIGH, LOW


def bit_cast(fn: tp.Callable[['Bit', 'Bit'], 'Bit']) -> \
        tp.Callable[['Bit', tp.Union['Bit', bool]], 'Bit']:
    @functools.wraps(fn)
    def wrapped(self: 'Bit', other: tp.Union['Bit', bool]) -> 'Bit':
        if isinstance(other, Bit):
            return fn(self, other)
        try:
            other = Bit(other)
        except TypeError:
            return NotImplemented
        return fn(self, other)
    return wrapped


class BitMeta(DigitalMeta):
    pass


class Bit(Digital, AbstractBit, metaclass=BitMeta):
    __hash__ = Digital.__hash__

    @staticmethod
    def get_family() -> TypeFamily:
        # TODO: We'll probably have a circular dependency issue if types are
        # defined in separate files, we could monkey patch a field in __init__
        # after the files are loaded
        raise NotImplementedError()
        return _Family_

    def __init__(self, value=None, name=None):
        super().__init__(name=name)
        # TODO: Port debug_name code
        if value is None:
            self._value = None
        elif isinstance(value, Bit):
            self._value = value._value
        elif isinstance(value, bool):
            self._value = value
        elif isinstance(value, int):
            if value not in {0, 1}:
                raise ValueError('Bit must have value 0 or 1 not {}'.format(value))
            self._value = bool(value)
        elif hasattr(value, '__bool__'):
            self._value = bool(value)
        else:
            raise TypeError("Can't coerce {} to Bit".format(type(value)))

    @property
    def direction(self):
        return type(self).direction

    def __invert__(self):
        return self.__invert()(self)

    @bit_cast
    def __eq__(self, other):
        return self.__eq(self, other)

    @bit_cast
    def __ne__(self, other):
        return self.__ne(self, other)

    @bit_cast
    def __and__(self, other):
        return self.__and(self, other)

    @bit_cast
    def __or__(self, other):
        return self.__or(self, other)

    @bit_cast
    def __xor__(self, other):
        return self.__xor(self, other)

    def ite(self, t_branch, f_branch):
        # TODO: This is basically just a phi/mux, but if we need this func we
        # can patch the same implementation in
        raise NotImplementedError()

    def __bool__(self) -> bool:
        # Don't think we can suppor this in magma
        raise NotImplementedError()

    def __int__(self) -> int:
        # Don't think we can suppor this in magma
        raise NotImplementedError()

    # def __hash__(self) -> int:
    #     return hash(self._value)

    def __repr__(self):
        if self is VCC:
            return '1'
        if self is GND:
            return '0'

        return super().__repr__()


BitIn = Bit[Direction.In]
BitOut = Bit[Direction.Out]
