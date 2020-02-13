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
    if T is m.Array[5, m.Bits[5]]:
        wires = ""
        for i in range(5):
            for j in range(5):
                wires += f"wire(Main.I[{i}][{j}], wire_I_x.in[{i * 5 + j}])\n"
        for i in range(5):
            for j in range(5):
                wires += f"wire(x[{i}][{j}], wire_x_O.in[{i * 5 + j}])\n"
                wires += f"wire(wire_I_x.out[{i * 5 + j}], x[{i}][{j}])\n"
        for i in range(5):
            for j in range(5):
                wires += f"wire(wire_x_O.out[{i * 5 + j}], Main.O[{i}][{j}])\n"
        wires = wires[:-1]  # remove trailing newline
    elif T is m.Tuple[m.Bits[5], m.Bit]:
        wires = ""
        offset = 0
        for i in range(len(T.fields)):
            if issubclass(T[i], m.Array):
                for j in range(len(T[i])):
                    wires += f"wire(Main.I[{i}][{j}], wire_I_x.in[{i + offset + j}])\n"
            else:
                wires += f"wire(Main.I[{i}], wire_I_x.in[{offset}])\n"
            offset += T.flat_length() - 1
        offset = 0
        for i in range(len(T.fields)):
            if issubclass(T[i], m.Array):
                for j in range(len(T[i])):
                    wires += f"wire(x[{i}][{j}], wire_x_O.in[{i + offset + j}])\n"
                    wires += f"wire(wire_I_x.out[{i + offset + j}], x[{i}][{j}])\n"
            else:
                wires += f"wire(x[{i}], wire_x_O.in[{offset}])\n"
                wires += f"wire(wire_I_x.out[{offset}], x[{i}])\n"
            offset += T.flat_length() - 1
        offset = 0
        for i in range(len(T.fields)):
            if issubclass(T[i], m.Array):
                for j in range(len(T[i])):
                    wires += f"wire(wire_x_O.out[{i + offset + j}], Main.O[{i}][{j}])\n"
            else:
                wires += f"wire(wire_x_O.out[{offset}], Main.O[{i}])\n"
            offset += T.flat_length() - 1
        wires = wires[:-1]  # remove trailing newline
    else:
        index = "[0]" if T is m.Bit else ""
        wires = f"""\
wire(Main.I, wire_I_x.in{index})
wire(x, wire_x_O.in{index})
wire(wire_I_x.out{index}, x)
wire(wire_x_O.out{index}, Main.O)\
"""
    assert repr(Main) == f"""\
Main = DefineCircuit("Main", "I", {m.In(T)}, "O", {m.Out(T)})
x = {T}(name="x")
wire_I_x = Wire(name="wire_I_x")
wire_x_O = Wire(name="wire_x_O")
{wires}
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
    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")\
                  .replace("=", "")
    m.compile(f"build/insert_coreir_wires_arr_tuple_{T_str}", Main)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_arr_tuple_{T_str}.v",
                             f"gold/insert_coreir_wires_arr_tuple_{T_str}.v")
