"""
Definition of magma's Bit type
* Subtype of the Digital type
* Implementation of hwtypes.AbstractBit
"""
import typing as tp
import functools
from functools import lru_cache
import magma as m
from hwtypes.bit_vector_abc import AbstractBit, TypeFamily
from .t import Direction
from .digital import Digital, DigitalMeta


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


class Bit(Digital, AbstractBit, metaclass=DigitalMeta):
    __hash__ = Digital.__hash__

    @staticmethod
    def get_family() -> TypeFamily:
        return m._Family_

    @classmethod
    @lru_cache(maxsize=None)
    def declare_unary_op(cls, op):
        return m.circuit.DeclareCoreirCircuit(f"magma_Bit_{op}",
                                              "I", m.In(m.Bit),
                                              "O", m.Out(m.Bit),
                                              coreir_name=op,
                                              coreir_lib="corebit")

    @classmethod
    @lru_cache(maxsize=None)
    def declare_binary_op(cls, op):
        return m.circuit.DeclareCoreirCircuit(f"magma_Bit_{op}",
                                              "I0", m.In(m.Bit),
                                              "I1", m.In(m.Bit),
                                              "O", m.Out(m.Bit),
                                              coreir_name=op,
                                              coreir_lib="corebit")

    @classmethod
    @lru_cache(maxsize=None)
    def declare_ite(cls, T):
        t_str = str(T)
        # Sanitize
        t_str = t_str.replace("(", "_")
        t_str = t_str.replace(")", "")
        t_str = t_str.replace("[", "_")
        t_str = t_str.replace("]", "")
        if issubclass(T, Bit):
            return m.circuit.DeclareCoreirCircuit(f"magma_Bit_ite_{t_str}",
                                                  "I0", m.In(T),
                                                  "I1", m.In(T),
                                                  "S", m.In(m.Bit),
                                                  "O", m.Out(T),
                                                  coreir_name="mux",
                                                  coreir_lib="corebit")
        assert issubclass(T, m.Bits)
        return m.circuit.DeclareCoreirCircuit(f"magma_Bit_ite_{t_str}",
                                              "I0", m.In(T),
                                              "I1", m.In(T),
                                              "S", m.In(m.Bit),
                                              "O", m.Out(T),
                                              coreir_genargs={"width": len(T)},
                                              coreir_name="mux",
                                              coreir_lib="coreir")

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
        return self.declare_unary_op("not")()(self)

    @bit_cast
    def __eq__(self, other):
        # CoreIR doesn't define an eq primitive for bits
        return ~(self ^ other)

    @bit_cast
    def __ne__(self, other):
        # CoreIR doesn't define an ne primitive for bits
        return self ^ other

    @bit_cast
    def __and__(self, other):
        return self.declare_binary_op("and")()(self, other)

    @bit_cast
    def __or__(self, other):
        return self.declare_binary_op("or")()(self, other)

    @bit_cast
    def __xor__(self, other):
        return self.declare_binary_op("xor")()(self, other)

    def ite(self, t_branch, f_branch):
        type_ = type(t_branch)
        if type_ != type(f_branch):
            raise TypeError(f"ite expects same type for both branches: {type_} != {type(f_branch)}")
        # Note: coreir flips t/f cases
        return self.declare_ite(type_)()(f_branch, t_branch, self)

    def __bool__(self) -> bool:
        raise NotImplementedError("Converting magma bit to bool not supported")

    def __int__(self) -> int:
        raise NotImplementedError("Converting magma bit to int not supported")


VCC = Bit[Direction.Out](name="VCC")
GND = Bit[Direction.Out](name="GND")

HIGH = VCC
LOW = GND


BitIn = Bit[Direction.In]
BitOut = Bit[Direction.Out]
BitInOut = Bit[Direction.InOut]
