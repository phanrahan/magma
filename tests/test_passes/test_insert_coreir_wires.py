import magma as m
from magma.t import Direction
from magma.testing import check_files_equal
import pytest
import copy


@pytest.mark.parametrize(
    "T",
    [m.Bit, m.Bits[5], m.Array[5, m.Bits[5]], m.Tuple[m.Bits[5], m.Bit]]
)
def test_insert_coreir_wires_basic(T):
    class Main(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))

        x = T(name="x")
        x @= io.I
        io.O @= x
    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")
    m.compile(f"build/insert_coreir_wires_{T_str}", Main, inline=True)
    assert check_files_equal(__file__, f"build/insert_coreir_wires_{T_str}.v",
                             f"gold/insert_coreir_wires_{T_str}.v")

    if T is m.Array[5, m.Bits[5]]:
        wires = ""
        for i in range(5):
            j = i * 5
            wires += f"wire(_x[{i}], x.in[slice({i * 5}, {(i + 1) * 5}, None)])\n"
            wires += f"wire(Main.I[{i}], _x[{i}])\n"
        for i in range(5):
            for j in range(5):
                wires += f"wire(x.out[{i * 5 + j}], Main.O[{i}][{j}])\n"
        wires = wires[:-1]  # remove trailing newline
    elif T is m.Tuple[m.Bits[5], m.Bit]:
        wires = ""
        offset = 0
        for i in range(len(T.fields)):
            if issubclass(T[i], m.Array):
                wires += f"wire(_x[{i}], x.in[slice({offset}, {len(T[i])}, None)])\n"
                wires += f"wire(Main.I[{i}], _x[{i}])\n"
            else:
                wires += f"wire(_x[{i}], x.in[{offset}])\n"
                wires += f"wire(Main.I[{i}], _x[{i}])\n"
            offset += T.flat_length() - 1
        offset = 0
        for i in range(len(T.fields)):
            if issubclass(T[i], m.Array):
                for j in range(len(T[i])):
                    wires += f"wire(x.out[{i + offset + j}], Main.O[{i}][{j}])\n"
            else:
                wires += f"wire(x.out[{offset}], Main.O[{i}])\n"
            offset += T.flat_length() - 1
        wires = wires[:-1]  # remove trailing newline
    else:
        wires = f"""\
wire(_x, x.in)
wire(Main.I, _x)
wire(x.out, Main.O)\
"""
    assert repr(Main) == f"""\
Main = DefineCircuit("Main", "I", {m.In(T)}, "O", {m.Out(T)})
_x = {T}(name="_x")
x = Wire(name="x")
{wires}
EndCircuit()\
""", repr(Main)


@pytest.mark.parametrize(
    "T",
    [m.Bit, m.Bits[5], m.Array[5, m.Bits[5]], m.Tuple[m.Bits[5], m.Bit]]
)
def test_insert_coreir_wires_instance(T):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))

    class Main(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))

        x = T(name="x")
        foo = Foo()
        x @= foo.O
        foo.I @= io.I
        io.O @= x

    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")
    m.compile(f"build/insert_coreir_wires_instance_{T_str}", Main, inline=True)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_instance_{T_str}.v",
                             f"gold/insert_coreir_wires_instance_{T_str}.v")


def test_insert_coreir_wires_mixed_tuple():
    class T(m.Product):
        x = m.In(m.Bit)
        y = m.Out(m.Bit)

    class Foo(m.Circuit):
        io = m.IO(z=T)

    class Main(m.Circuit):
        io = m.IO(z=T)

        a = T.qualify(Direction.Undirected)(name="a")
        foo = Foo()
        a.x @= foo.z.y
        a.y @= io.z.x
        foo.z.x @= a.y
        io.z.y @= a.x

    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")\
                  .replace("=", "")
    m.compile(f"build/insert_coreir_wires_tuple_{T_str}", Main, inline=True)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_tuple_{T_str}.v",
                             f"gold/insert_coreir_wires_tuple_{T_str}.v")


def test_insert_coreir_wires_array_mixed_tuple():
    class T(m.Product):
        x = m.In(m.Bit)
        y = m.Out(m.Bit)

    class Foo(m.Circuit):
        io = m.IO(z=m.Array[2, T])

    class Main(m.Circuit):
        io = m.IO(z=m.Array[2, T])

        a = T.qualify(Direction.Undirected)(name="a")
        foo = Foo()
        a.x @= foo.z[0].y
        a.y @= io.z[0].x
        foo.z[0].x @= a.y
        io.z[0].y @= a.x
        foo.z[1].x @= io.z[0].x
        io.z[1].y @= foo.z[1].y

    T_str = str(T).replace("[", "").replace("]", "").replace(",", "")\
                  .replace(" ", "").replace("(", "").replace(")", "")\
                  .replace("=", "")
    m.compile(f"build/insert_coreir_wires_arr_tuple_{T_str}", Main, inline=True)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_arr_tuple_{T_str}.v",
                             f"gold/insert_coreir_wires_arr_tuple_{T_str}.v")


def test_insert_coreir_wires_fanout():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O0=m.Out(m.Bit), O1=m.Out(m.Bit))

        x = m.Bit(name="x")
        x @= io.I
        io.O0 @= x
        io.O1 @= x
    m.compile(f"build/insert_coreir_wires_fanout", Main, inline=True)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_fanout.v",
                             f"gold/insert_coreir_wires_fanout.v")


def test_insert_coreir_wires_temp_array_not_whole():
    """
    Should not produce:

module Main (
    input I,
    output O0,
    output O1
);
wire x_0;
wire x_1;
assign x_0 = I;
assign x_1 = I;
assign O0 = x_0;
assign O1 = x_1;
endmodule

    where x is bit-blasted
    """
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O0=m.Out(m.Bit), O1=m.Out(m.Bit))

        x = m.Bits[2](name="x")
        for i in range(2):
            x[i] @= io.I
        io.O0 @= x[0]
        io.O1 @= x[1]
    m.compile(f"build/insert_coreir_wires_temp_array_not_whole", Main, inline=True)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_temp_array_not_whole.v",
                             f"gold/insert_coreir_wires_temp_array_not_whole.v")


def test_insert_coreir_wires_temp_array_not_whole2():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O0=m.Out(m.Bits[2]), O1=m.Out(m.Bits[2]))

        x = m.Array[2, m.Bits[2]](name="x")
        for i in range(2):
            x[i] @= io.I
        io.O0 @= x[0]
        io.O1 @= x[1]
    m.compile(f"build/insert_coreir_wires_temp_array_not_whole2", Main, inline=True)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_temp_array_not_whole2.v",
                             f"gold/insert_coreir_wires_temp_array_not_whole2.v")


def test_insert_coreir_wires_temp_array_not_whole3():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O0=m.Out(m.Bits[2]), O1=m.Out(m.Bits[2]))

        x = m.Array[2, m.Bits[2]](name="x")
        x[0][0] @= io.I[1]
        x[0][1] @= io.I[0]
        x[1][0] @= io.I[0]
        x[1][1] @= io.I[1]

        io.O0[0] @= x[0][0]
        io.O0[1] @= x[1][0]
        io.O1[0] @= x[1][1]
        io.O1[1] @= x[0][1]
    m.compile(f"build/insert_coreir_wires_temp_array_not_whole3", Main, inline=True)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_temp_array_not_whole3.v",
                             f"gold/insert_coreir_wires_temp_array_not_whole3.v")


def test_insert_coreir_wires_temp_array_not_whole_anon():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O0=m.Out(m.Bits[2]), O1=m.Out(m.Bits[2]))

        x = m.Array[2, m.Bits[2]]()
        y = m.Bit(name="y")
        y @= io.I[1]
        z = m.Bit(name="z")
        z @= io.I[0]
        x[0][0] @= y
        x[0][1] @= z
        x[1][0] @= z
        x[1][1] @= y

        io.O0[0] @= x[0][0]
        io.O0[1] @= x[1][0]
        io.O1[0] @= x[1][1]
        io.O1[1] @= x[0][1]
    m.compile(f"build/insert_coreir_wires_temp_array_not_whole_anon", Main, inline=True)
    assert check_files_equal(__file__,
                             f"build/insert_coreir_wires_temp_array_not_whole_anon.v",
                             f"gold/insert_coreir_wires_temp_array_not_whole_anon.v")
