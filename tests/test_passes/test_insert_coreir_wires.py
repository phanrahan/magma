import magma as m
from magma.passes.insert_coreir_wires import InsertCoreIRWires
from magma.testing import check_files_equal
import pytest


@pytest.mark.parametrize(
    "T", 
    [m.Bit, m.Bits[5], m.Array[5, m.Bits[5]], m.Tuple[m.Bits[5], m.Bit]]
)
def test_insert_coreir_wires_basic(T):
    class Main(m.Circuit):
        IO = ["I", m.In(T), "O", m.Out(T)]

        @classmethod
        def definition(io):
            x = T(name="x")
            x @= io.I
            io.O @= x

    InsertCoreIRWires(Main).run()
    assert repr(Main) == f"""\
Main = DefineCircuit("Main", "I", {m.In(T)}, "O", {m.Out(T)})
wire_I_x = WrappedWire(name="wire_I_x")
wire_x_O = WrappedWire(name="wire_x_O")
wire(Main.I, wire_I_x.I)
x = {T}(name="x")
wire(x, wire_x_O.I)
wire(wire_I_x.O, x)
wire(wire_x_O.O, Main.O)
EndCircuit()\
"""
    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")
    m.compile(f"build/insert_coreir_wires_{T_str}", Main)
    check_files_equal(__file__, f"build/insert_coreir_wires_{T_str}.v",
                      f"gold/insert_coreir_wires_{T_str}.v")


@pytest.mark.parametrize(
    "T", 
    [m.Bit, m.Bits[5], m.Array[5, m.Bits[5]], m.Tuple[m.Bits[5], m.Bit]]
)
def test_insert_coreir_wires_instance(T):
    class Foo(m.Circuit):
        IO = ["I", m.In(T), "O", m.Out(T)]

    class Main(m.Circuit):
        IO = ["I", m.In(T), "O", m.Out(T)]

        @classmethod
        def definition(io):
            x = T(name="x")
            foo = Foo()
            x @= foo.O
            foo.I @= io.I
            io.O @= x

    InsertCoreIRWires(Main).run()
    assert repr(Main) == f"""\
Main = DefineCircuit("Main", "I", {m.In(T)}, "O", {m.Out(T)})
Foo_inst0 = Foo()
wire_Foo_inst0_O_x = WrappedWire(name="wire_Foo_inst0_O_x")
wire_I_Foo_inst0_I = WrappedWire(name="wire_I_Foo_inst0_I")
wire_x_O = WrappedWire(name="wire_x_O")
wire(wire_I_Foo_inst0_I.O, Foo_inst0.I)
wire(Foo_inst0.O, wire_Foo_inst0_O_x.I)
wire(Main.I, wire_I_Foo_inst0_I.I)
x = {T}(name="x")
wire(x, wire_x_O.I)
wire(wire_Foo_inst0_O_x.O, x)
wire(wire_x_O.O, Main.O)
EndCircuit()\
"""
    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")
    m.compile(f"build/insert_coreir_wires_instance_{T_str}", Main)
    check_files_equal(__file__, f"build/insert_coreir_wires_instance_{T_str}.v",
                      f"gold/insert_coreir_wires_instance_{T_str}.v")
