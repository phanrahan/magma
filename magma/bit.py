"""
Definition of magma's Bit type
* Subtype of the Digital type
* Implementation of hwtypes.AbstractBit
"""
import keyword
import typing as tp
import functools
import hwtypes as ht
from hwtypes.bit_vector_abc import AbstractBit, TypeFamily
from .t import Direction
from .digital import Digital, DigitalMeta
from .digital import VCC, GND  # TODO(rsetaluri): only here for b.c.

from magma.compatibility import IntegerTypes
from magma.debug import debug_wire
from magma.family import get_family
from magma.interface import IO
from magma.language_utils import primitive_to_python
from magma.protocol_type import magma_type, MagmaProtocol
from magma.operator_utils import output_only


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


_IMPLICITLY_COERCED_ITE_TYPES = (int, ht.BitVector, ht.Bit)


class Bit(Digital, AbstractBit, metaclass=DigitalMeta):
    __hash__ = Digital.__hash__

    @staticmethod
    def get_family() -> TypeFamily:
        return get_family()

    def __init__(self, value=None, name=None):
        super().__init__(name=name)
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
        # CoreIR uses not instead of invert name
        return type(self).undirected_t._declare_unary_op("not")()(self)

    @bit_cast
    @output_only("Cannot use == on an input")
    def __eq__(self, other):
        if self is other:
            return True
        # CoreIR doesn't define an eq primitive for bits
        return ~(self ^ other)

    @bit_cast
    @output_only("Cannot use != on an input")
    def __ne__(self, other):
        # CoreIR doesn't define an ne primitive for bits
        return self ^ other

    @bit_cast
    def __and__(self, other):
        return type(self).undirected_t._declare_binary_op("and")()(self, other)

    @bit_cast
    def __or__(self, other):
        return type(self).undirected_t._declare_binary_op("or")()(self, other)

    @bit_cast
    def __xor__(self, other):
        return type(self).undirected_t._declare_binary_op("xor")()(self, other)

    def ite(self, t_branch, f_branch):
        if isinstance(t_branch, list) and isinstance(f_branch, list):
            if not len(t_branch) == len(f_branch):
                raise TypeError("Bit.ite of two lists expects the same length")
            return [self.ite(x, y) for x, y in zip(t_branch, f_branch)]

        if self.const():
            return t_branch if bool(self) else f_branch
        if isinstance(t_branch, tuple):
            return tuple(self.ite(t, f) for t, f in zip(t_branch, f_branch))
        # NOTE(rsetaluri): CoreIR flips t/f cases.
        # NOTE(rseatluri): self._mux is monkey patched in
        # magma/primitives/mux.py to avoid circular dependency.
        return self._mux([f_branch, t_branch], self)

    @debug_wire
    def wire(self, o, debug_info):
        # Cast to Bit here so we don't get a Digital instead
        if isinstance(o, (IntegerTypes, bool, ht.Bit)):
            o = Bit(o)
        return super().wire(o, debug_info)


BitIn = Bit[Direction.In]
BitOut = Bit[Direction.Out]
BitInOut = Bit[Direction.InOut]
