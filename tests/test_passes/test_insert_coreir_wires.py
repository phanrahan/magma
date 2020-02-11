import magma as m
from magma.t import Direction
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
x = {T}(name="x")
wire_I_x = WrappedWire(name="wire_I_x")
wire_x_O = WrappedWire(name="wire_x_O")
wire(Main.I, wire_I_x.I)
wire(x, wire_x_O.I)
wire(wire_I_x.O, x)
wire(wire_x_O.O, Main.O)
EndCircuit()\
""", repr(Main)
    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")
    m.compile(f"build/insert_coreir_wires_{T_str}", Main)
    assert check_files_equal(__file__, f"build/insert_coreir_wires_{T_str}.v",
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
x = {T}(name="x")
Foo_inst0 = Foo()
wire_Foo_inst0_O_x = WrappedWire(name="wire_Foo_inst0_O_x")
wire_I_Foo_inst0_I = WrappedWire(name="wire_I_Foo_inst0_I")
wire_x_O = WrappedWire(name="wire_x_O")
wire(wire_I_Foo_inst0_I.O, Foo_inst0.I)
wire(Foo_inst0.O, wire_Foo_inst0_O_x.I)
wire(Main.I, wire_I_Foo_inst0_I.I)
wire(x, wire_x_O.I)
wire(wire_Foo_inst0_O_x.O, x)
wire(wire_x_O.O, Main.O)
EndCircuit()\
"""
    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")
    m.compile(f"build/insert_coreir_wires_instance_{T_str}", Main)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_instance_{T_str}.v",
                             f"gold/insert_coreir_wires_instance_{T_str}.v")


def test_insert_coreir_wires_mixed_tuple():
    class T(m.Product):
        x = m.In(m.Bit)
        y = m.Out(m.Bit)

    class Foo(m.Circuit):
        IO = ["z", T]

    class Main(m.Circuit):
        IO = ["z", T]

        @classmethod
        def definition(io):
            a = T.qualify(Direction.Undirected)(name="a")
            foo = Foo()
            a.x @= foo.z.y
            a.y @= io.z.x
            foo.z.x @= a.y
            io.z.y @= a.x

    InsertCoreIRWires(Main).run()
    assert repr(Main) == f"""\
Main = DefineCircuit("Main", "z", Tuple(x=In(Bit),y=Out(Bit)))
a = Tuple(x=Bit,y=Bit)(name="a")
Foo_inst0 = Foo()
wire_Foo_inst0_z_y_a_x = WrappedWire(name="wire_Foo_inst0_z_y_a_x")
wire_a_x_z_y = WrappedWire(name="wire_a_x_z_y")
wire_a_y_Foo_inst0_z_x = WrappedWire(name="wire_a_y_Foo_inst0_z_x")
wire_z_x_a_y = WrappedWire(name="wire_z_x_a_y")
wire(wire_a_y_Foo_inst0_z_x.O, Foo_inst0.z.x)
wire(Foo_inst0.z.y, wire_Foo_inst0_z_y_a_x.I)
wire(a.x, wire_a_x_z_y.I)
wire(wire_Foo_inst0_z_y_a_x.O, a.x)
wire(a.y, wire_a_y_Foo_inst0_z_x.I)
wire(wire_z_x_a_y.O, a.y)
wire(Main.z.x, wire_z_x_a_y.I)
wire(wire_a_x_z_y.O, Main.z.y)
EndCircuit()\
""", repr(Main)
    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")\
                  .replace("=", "")
    m.compile(f"build/insert_coreir_wires_tuple_{T_str}", Main)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_tuple_{T_str}.v",
                             f"gold/insert_coreir_wires_tuple_{T_str}.v")


def test_insert_coreir_wires_array_mixed_tuple():
    class T(m.Product):
        x = m.In(m.Bit)
        y = m.Out(m.Bit)

    class Foo(m.Circuit):
        IO = ["z", m.Array[2, T]]

    class Main(m.Circuit):
        IO = ["z", m.Array[2, T]]

        @classmethod
        def definition(io):
            a = T.qualify(Direction.Undirected)(name="a")
            foo = Foo()
            a.x @= foo.z[0].y
            a.y @= io.z[0].x
            foo.z[0].x @= a.y
            io.z[0].y @= a.x
            foo.z[1].x @= io.z[0].x
            io.z[1].y @= foo.z[1].y

    InsertCoreIRWires(Main).run()
    assert repr(Main) == f"""\
Main = DefineCircuit("Main", "z", Array[2, Tuple(x=In(Bit),y=Out(Bit))])
a = Tuple(x=Bit,y=Bit)(name="a")
Foo_inst0 = Foo()
wire_Foo_inst0_z_0_y_a_x = WrappedWire(name="wire_Foo_inst0_z_0_y_a_x")
wire_Foo_inst0_z_1_y_z_1_y = WrappedWire(name="wire_Foo_inst0_z_1_y_z_1_y")
wire_a_x_z_0_y = WrappedWire(name="wire_a_x_z_0_y")
wire_a_y_Foo_inst0_z_0_x = WrappedWire(name="wire_a_y_Foo_inst0_z_0_x")
wire_z_0_x_Foo_inst0_z_1_x = WrappedWire(name="wire_z_0_x_Foo_inst0_z_1_x")
wire_z_0_x_a_y = WrappedWire(name="wire_z_0_x_a_y")
wire(wire_a_y_Foo_inst0_z_0_x.O, Foo_inst0.z[0].x)
wire(wire_z_0_x_Foo_inst0_z_1_x.O, Foo_inst0.z[1].x)
wire(Foo_inst0.z[0].y, wire_Foo_inst0_z_0_y_a_x.I)
wire(Foo_inst0.z[1].y, wire_Foo_inst0_z_1_y_z_1_y.I)
wire(a.x, wire_a_x_z_0_y.I)
wire(wire_Foo_inst0_z_0_y_a_x.O, a.x)
wire(a.y, wire_a_y_Foo_inst0_z_0_x.I)
wire(wire_z_0_x_a_y.O, a.y)
wire(Main.z[0].x, wire_z_0_x_Foo_inst0_z_1_x.I)
wire(Main.z[0].x, wire_z_0_x_a_y.I)
wire(wire_a_x_z_0_y.O, Main.z[0].y)
wire(wire_Foo_inst0_z_1_y_z_1_y.O, Main.z[1].y)
EndCircuit()\
""", repr(Main)
    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")\
                  .replace("=", "")
    m.compile(f"build/insert_coreir_wires_arr_tuple_{T_str}", Main)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_arr_tuple_{T_str}.v",
                             f"gold/insert_coreir_wires_arr_tuple_{T_str}.v")
