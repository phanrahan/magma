"""
Bit type primitives factored out into a separate file.
NOTE(leonardt): This avoids a circular dependency between circuit.py, bit.py,
and clock.py
"""
from functools import lru_cache
import operator

import hwtypes as ht

from magma.bit import Bit
from magma.debug import magma_helper_function
from magma.digital import Digital
from magma.circuit import Circuit, coreir_port_mapping
from magma.interface import IO
from magma.language_utils import primitive_to_python
from magma.t import In, Out


@classmethod
@lru_cache(maxsize=None)
def _declare_unary_op(cls, op):
    assert cls.undirected_t is cls
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
def _declare_binary_op(cls, op):
    assert cls.undirected_t is cls
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


# NOTE(leonardt): Monkey patched functions.
Bit._declare_unary_op = _declare_unary_op
Bit._declare_binary_op = _declare_binary_op


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
            primitive = True
            stateful = False
        return _Primitive
    return DefineCorebit


DefineUndriven = make_Define("undriven", "O", Out)
DefineUnused = make_Define("term", "I", In)


@magma_helper_function
def unused(self):
    if self.is_input() or self.is_inout():
        raise TypeError("unused cannot be used with input/inout")
    if not getattr(self, "_magma_unused_", False):
        DefineUnused()().I.wire(self)
        # "Cache" unused calls so only one is produced
        self._magma_unused_ = True


@magma_helper_function
def undriven(self):
    if self.is_output() or self.is_inout():
        raise TypeError("undriven cannot be used with output/inout")
    self.wire(DefineUndriven()().O)


# NOTE(leonardt): Monkey patched functions.
Bit.unused = unused
Bit.undriven = undriven
Digital.unused = unused
Digital.undriven = undriven
