"""
Definition of magma's Bit type
* Subtype of the Digital type
* Implementation of hwtypes.AbstractBit
"""
import keyword
import operator
import typing as tp
import functools
from functools import lru_cache
import hwtypes as ht
from hwtypes.bit_vector_abc import AbstractBit, TypeFamily
from .t import Direction, In, Out
from .digital import Digital, DigitalMeta
from .digital import VCC, GND  # TODO(rsetaluri): only here for b.c.
from magma.circuit import Circuit, coreir_port_mapping
from magma.family import get_family
from magma.interface import IO
from magma.language_utils import primitive_to_python
from magma.protocol_type import get_type


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
        return get_family()

    @classmethod
    @lru_cache(maxsize=None)
    def declare_unary_op(cls, op):
        assert op == "not", f"simulate not implemented for {op}"

        class _MagmaBitOp(Circuit):
            name = f"magma_Bit_{op}"
            coreir_name = op
            coreir_lib = "corebit"
            renamed_ports = coreir_port_mapping
            primitive = True
            stateful = False

            io = IO(I=In(Bit), O=Out(Bit))

            def simulate(self, value_store, state_store):
                I = ht.Bit(value_store.get_value(self.I))
                O = int(~I)
                value_store.set_value(self.O, O)

        return _MagmaBitOp

    @classmethod
    @lru_cache(maxsize=None)
    def declare_binary_op(cls, op):
        python_op_name = primitive_to_python(op)
        python_op = getattr(operator, python_op_name)

        class _MagmaBitOp(Circuit):
            name = f"magma_Bit_{op}"
            coreir_name = op
            coreir_lib = "corebit"
            renamed_ports = coreir_port_mapping
            primitive = True
            stateful = False

            io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

            def simulate(self, value_store, state_store):
                I0 = ht.Bit(value_store.get_value(self.I0))
                I1 = ht.Bit(value_store.get_value(self.I1))
                O = int(python_op(I0, I1))
                value_store.set_value(self.O, O)

        return _MagmaBitOp

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
        t_type = get_type(t_branch)
        f_type = get_type(f_branch)

        # Implicit int conversion
        if t_type is int and f_type is not int:
            t_branch = f_type(t_branch)
            t_type = f_type
        elif t_type is not int and f_type is int:
            f_branch = t_type(t_branch)
            f_type = t_type

        if t_type is not f_type:
            raise TypeError(f"ite expects same type for both branches: {t_type} != {f_type}")
        if self.const():
            if self is type(self).VCC:
                return t_branch
            assert self is type(self).GND
            return f_branch
        if issubclass(t_type, tuple):
            return tuple(self.ite(t, f) for t, f in zip(t_branch, f_branch))
        # Note: coreir flips t/f cases
        # self._Mux monkey patched in magma/primitives/mux.py to avoid circular
        # dependency
        return self._Mux(2, t_type)()(f_branch, t_branch, self)

    def __bool__(self) -> bool:
        raise NotImplementedError("Converting magma bit to bool not supported")

    def __int__(self) -> int:
        raise NotImplementedError("Converting magma bit to int not supported")

    def unused(self):
        if self.is_input() or self.is_inout():
            raise TypeError("unused cannot be used with input/inout")
        if not getattr(self, "_magma_unused_", False):
            DefineUnused()().I.wire(self)
            # "Cache" unused calls so only one is produced
            self._magma_unused_ = True

    def undriven(self):
        if self.is_output() or self.is_inout():
            raise TypeError("undriven cannot be used with output/inout")
        self.wire(DefineUndriven()().O)


def make_Define(_name, port, direction):
    @lru_cache(maxsize=None)
    def DefineCorebit():
        class _Primitive(Circuit):
            renamed_ports = coreir_port_mapping
            name = f"corebit_{_name}"
            coreir_name = _name
            coreir_lib = "corebit"

            def simulate(self, value_store, state_store):
                pass

            # Type must be a bit because coreir uses Bit for the primitive.
            io = IO(**{port: direction(Bit)})
        return _Primitive
    return DefineCorebit


DefineUndriven = make_Define("undriven", "O", Out)
DefineUnused = make_Define("term", "I", In)

# Hack to avoid circular dependency
Digital.unused = Bit.unused
Digital.undriven = Bit.undriven

BitIn = Bit[Direction.In]
BitOut = Bit[Direction.Out]
BitInOut = Bit[Direction.InOut]
