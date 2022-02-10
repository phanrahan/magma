"""
Test the `m.Bits` type
"""

import operator
import pytest
import magma as m
from magma import Bits
from magma.testing import check_files_equal
from magma.simulator import PythonSimulator
from hwtypes import BitVector

ARRAY2 = m.Array[2, m.Bit]
ARRAY4 = m.Array[4, m.Bit]


def test_bits_basic():
    """
    Basic bits tests
    """
    bits_2 = m.Bits[2]
    bits_in_2 = m.In(m.Bits[2])
    bits_out_2 = m.Out(m.Bits[2])
    assert bits_in_2.undirected_t == bits_2
    assert bits_2 == m.Bits[2]
    assert bits_in_2 == m.In(bits_2)
    assert bits_out_2 == m.Out(bits_2)

    assert bits_2 == bits_in_2
    assert bits_2 == bits_out_2
    assert bits_in_2 == bits_out_2

    assert bits_2 is not bits_in_2
    assert bits_2 is not bits_out_2
    assert bits_in_2 is not bits_out_2

    bits_4 = m.Bits[4]
    assert bits_4 == ARRAY4
    assert bits_2 != bits_4

    assert m.Bits[11]().is_oriented(m.Direction.Undirected)

def test_qualify_bits():
    assert str(m.In(Bits)) == "In(Bits)"
    assert str(m.Out(m.In(Bits))) == "Out(Bits)"
    assert str(m.In(Bits)[5, m.Bit]) == "In(Bits[5])"
    assert str(m.Out(m.In(Bits))[5, m.Bit]) == "Out(Bits[5])"

    # Bits qualifer overrides child qualifer
    assert str(m.In(Bits)[5, m.Out(m.Bit)]) == "In(Bits[5])"

    assert m.In(Bits) is m.In(Bits)
    assert m.Out(m.In(Bits)) is m.Out(Bits)
    assert m.In(Bits)[5, m.Bit] is m.Bits[5, m.In(m.Bit)]
    assert m.Out(m.In(Bits))[5, m.Bit] is Bits[5, m.Out(m.Bit)]

    # Bits qualifer overrides child qualifer
    assert m.In(Bits)[5, m.Out(m.Bit)] is Bits[5, m.In(m.Bit)]


def test_val():
    """
    Test instances of Bits[4] work correctly
    """
    bits_4_in = m.In(m.Bits[4])
    bits_4_out = m.Out(m.Bits[4])

    assert m.Flip(bits_4_in) == bits_4_out
    assert m.Flip(bits_4_out) == bits_4_in

    a_0 = bits_4_out(name='a0')
    print(a_0, type(a_0))

    a_1 = bits_4_in(name='a1')
    print(a_1, type(a_1))

    a_1.wire(a_0)

    b_0 = a_1[0]
    assert b_0 is a_1[0], "getitem failed"

    a_3 = a_1[0:2]
    assert all(a is b for a, b in zip(a_3, a_1[0:2])), "getitem of slice failed"


def test_flip():
    """
    Test flip interface
    """
    bits_2 = m.Bits[2]
    a_in = m.In(bits_2)
    a_out = m.Out(bits_2)

    print(a_in)
    print(a_out)

    assert a_in == ARRAY2
    assert a_out == ARRAY2
    assert a_in == a_out

    assert a_in is not ARRAY2
    assert a_out is not ARRAY2
    assert a_in is not a_out

    in_a_out = m.In(a_out)
    assert in_a_out == a_in
    print(in_a_out)

    a_out_flipped = m.Flip(a_out)
    assert a_out_flipped == a_in

    out_a_in = m.Out(a_in)
    assert out_a_in == a_out

    a_in_flipped = m.Flip(a_in)
    assert a_in_flipped == a_out
    print(a_in_flipped)


def test_construct():
    """
    Test `m.bits` interface
    """
    class Foo(m.Circuit):
        a_1 = m.bits([1, 1])
        print(type(a_1))
        assert isinstance(a_1, m.BitsType)

        # test promote
        assert isinstance(m.Bits[16](a_1), m.Bits)
        assert repr(m.Bits[16](
            a_1)) == "Bits[16](3)"


def test_const():
    """
    Test constant constructor interface
    """

    def check_equal(x, y):
        return int(x) == int(y)

    class Foo(m.Circuit):
        data = m.Bits[16]
        zero = data(0)
        assert check_equal(zero, m.bits(0, 16))

        assert check_equal(data(16), m.Bits[16].make_constant(16))
        assert check_equal(m.Bits[4](0xe), m.Bits[16].make_constant(0xe, 4))
        assert check_equal(m.Bits[4](0xe), m.Bits.make_constant(0xe, 4))


def test_setitem_bfloat():
    """
    Test constant constructor interface
    """
    class TestCircuit(m.Circuit):
        io = m.IO(I=m.In(m.BFloat[16]), O=m.Out(m.BFloat[16]))
        a = io.I
        b = a[0:-1].concat(m.bits(0, 1))
        io.O <= b
    assert repr(TestCircuit) == """\
TestCircuit = DefineCircuit("TestCircuit", "I", In(BFloat[16]), "O", Out(BFloat[16]))
wire(TestCircuit.I[0], TestCircuit.O[0])
wire(TestCircuit.I[1], TestCircuit.O[1])
wire(TestCircuit.I[2], TestCircuit.O[2])
wire(TestCircuit.I[3], TestCircuit.O[3])
wire(TestCircuit.I[4], TestCircuit.O[4])
wire(TestCircuit.I[5], TestCircuit.O[5])
wire(TestCircuit.I[6], TestCircuit.O[6])
wire(TestCircuit.I[7], TestCircuit.O[7])
wire(TestCircuit.I[8], TestCircuit.O[8])
wire(TestCircuit.I[9], TestCircuit.O[9])
wire(TestCircuit.I[10], TestCircuit.O[10])
wire(TestCircuit.I[11], TestCircuit.O[11])
wire(TestCircuit.I[12], TestCircuit.O[12])
wire(TestCircuit.I[13], TestCircuit.O[13])
wire(TestCircuit.I[14], TestCircuit.O[14])
wire(GND, TestCircuit.O[15])
EndCircuit()\
"""  # noqa


@pytest.mark.parametrize("n", [1, 3])
def test_invert(n):
    class TestInvert(m.Circuit):
        io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        io.O <= ~io.I

    assert repr(TestInvert) == f"""\
TestInvert = DefineCircuit("TestInvert", "I", In(Bits[{n}]), "O", Out(Bits[{n}]))
magma_Bits_{n}_not_inst0 = magma_Bits_{n}_not()
wire(TestInvert.I, magma_Bits_{n}_not_inst0.in)
wire(magma_Bits_{n}_not_inst0.out, TestInvert.O)
EndCircuit()\
"""
    m.compile(f"build/TestBits{n}Invert", TestInvert, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBits{n}Invert.v",
                             f"gold/TestBits{n}Invert.v")

    sim = PythonSimulator(TestInvert)
    for _ in range(2):
        I = BitVector.random(n)
        sim.set_value(TestInvert.I, I)
        sim.evaluate()
        assert sim.get_value(TestInvert.O) == ~I


@pytest.mark.parametrize("n", [1, 3])
@pytest.mark.parametrize("op", ["and_", "or_", "xor", "lshift", "rshift"])
def test_binary(op, n):
    class TestBinary(m.Circuit):
        io = m.IO(I0=m.In(m.Bits[n]), I1=m.In(m.Bits[n]), O=m.Out(m.Bits[n]))
        io.O <= getattr(operator, op)(io.I0, io.I1)

    magma_op = op.replace("_", "")
    magma_op = magma_op.replace("lshift", "shl")
    magma_op = magma_op.replace("rshift", "lshr")
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(Bits[{n}]), "I1", In(Bits[{n}]), \
"O", Out(Bits[{n}]))
magma_Bits_{n}_{magma_op}_inst0 = magma_Bits_{n}_{magma_op}()
wire(TestBinary.I0, magma_Bits_{n}_{magma_op}_inst0.in0)
wire(TestBinary.I1, magma_Bits_{n}_{magma_op}_inst0.in1)
wire(magma_Bits_{n}_{magma_op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    m.compile(f"build/TestBits{n}{magma_op}",
              TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBits{n}{magma_op}.v",
                             f"gold/TestBits{n}{magma_op}.v")

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = BitVector.random(n)
        I1 = BitVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == getattr(operator, op)(I0, I1)


@pytest.mark.parametrize("n", [1, 3])
def test_ite(n):
    class TestITE(m.Circuit):
        io = m.IO(I0=m.In(m.Bits[n]), I1=m.In(m.Bits[n]), S=m.In(m.Bits[n]),
                  O=m.Out(m.Bits[n]))

        io.O <= io.S.ite(io.I0, io.I1)

    assert repr(TestITE) == f"""\
TestITE = DefineCircuit("TestITE", "I0", In(Bits[{n}]), "I1", In(Bits[{n}]), "S", In(Bits[{n}]), "O", Out(Bits[{n}]))
magma_Bit_not_inst0 = magma_Bit_not()
magma_Bits_{n}_eq_inst0 = magma_Bits_{n}_eq()
magma_Bits_{n}_ite_Out_Bits_{n}_inst0 = magma_Bits_{n}_ite_Out_Bits_{n}()
wire(magma_Bits_{n}_eq_inst0.out, magma_Bit_not_inst0.in)
wire(TestITE.S, magma_Bits_{n}_eq_inst0.in0)
wire(BitVector[{n}](0), magma_Bits_{n}_eq_inst0.in1)
wire(TestITE.I0, magma_Bits_{n}_ite_Out_Bits_{n}_inst0.in0)
wire(TestITE.I1, magma_Bits_{n}_ite_Out_Bits_{n}_inst0.in1)
wire(magma_Bit_not_inst0.out, magma_Bits_{n}_ite_Out_Bits_{n}_inst0.sel)
wire(magma_Bits_{n}_ite_Out_Bits_{n}_inst0.out, TestITE.O)
EndCircuit()\
"""
    m.compile(f"build/TestBits{n}ITE", TestITE, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBits{n}ITE.v",
                             f"gold/TestBits{n}ITE.v")

    sim = PythonSimulator(TestITE)
    for S in [0, 1]:
        I0 = BitVector.random(n)
        I1 = BitVector.random(n)
        sim.set_value(TestITE.I0, I0)
        sim.set_value(TestITE.I1, I1)
        sim.set_value(TestITE.S, S)
        sim.evaluate()
        assert sim.get_value(TestITE.O) == (I1 if S else I0)


@pytest.mark.parametrize("n", [1, 3])
def test_eq(n):
    class TestBinary(m.Circuit):
        io = m.IO(I0=m.In(m.Bits[n]), I1=m.In(m.Bits[n]), O=m.Out(m.Bit))
        # Nasty precidence issue with <= operator means we need parens here
        io.O <= (io.I0 == io.I1)

    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(Bits[{n}]), "I1", In(Bits[{n}]), "O", Out(Bit))
magma_Bits_{n}_eq_inst0 = magma_Bits_{n}_eq()
wire(TestBinary.I0, magma_Bits_{n}_eq_inst0.in0)
wire(TestBinary.I1, magma_Bits_{n}_eq_inst0.in1)
wire(magma_Bits_{n}_eq_inst0.out, TestBinary.O)
EndCircuit()\
"""
    m.compile(f"build/TestBits{n}eq", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBits{n}eq.v",
                             f"gold/TestBits{n}eq.v")

    sim = PythonSimulator(TestBinary)
    for i in range(2):
        I0 = BitVector.random(n)
        I1 = BitVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == (I0 == I1)


@pytest.mark.parametrize("n", [1, 3])
def test_zext(n):
    class TestExt(m.Circuit):
        io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n + 3]))
        # Nasty precidence issue with <= operator means we need parens here
        io.O <= io.I.zext(3)

    if n > 1:
        i_wire = f"wire(TestExt.I, TestExt.O[slice(0, {n}, None)])"
    else:
        i_wire = 'wire(TestExt.I[0], TestExt.O[0])'
    gnd_wires = '\n'.join(f'wire(GND, TestExt.O[{i + n}])' for i in range(3))
    assert repr(TestExt) == f"""\
TestExt = DefineCircuit("TestExt", "I", In(Bits[{n}]), "O", Out(Bits[{n + 3}]))
{i_wire}
{gnd_wires}
EndCircuit()\
"""
    m.compile(f"build/TestBits{n}ext", TestExt, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBits{n}ext.v",
                             f"gold/TestBits{n}ext.v")

    sim = PythonSimulator(TestExt)
    for i in range(2):
        I = BitVector.random(n)
        sim.set_value(TestExt.I, I)
        sim.evaluate()
        assert sim.get_value(TestExt.O) == I.zext(3)


@pytest.mark.parametrize("n", [1, 3])
def test_bvcomp(n):
    class TestBinary(m.Circuit):
        io = m.IO(I0=m.In(m.Bits[n]), I1=m.In(m.Bits[n]), O=m.Out(m.Bits[1]))
        # Nasty precidence issue with <= operator means we need parens here
        io.O <= io.I0.bvcomp(io.I1)

    print(repr(TestBinary))
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(Bits[{n}]), "I1", In(Bits[{n}]), "O", Out(Bits[1]))
magma_Bits_{n}_eq_inst0 = magma_Bits_{n}_eq()
wire(TestBinary.I0, magma_Bits_{n}_eq_inst0.in0)
wire(TestBinary.I1, magma_Bits_{n}_eq_inst0.in1)
wire(magma_Bits_{n}_eq_inst0.out, TestBinary.O[0])
EndCircuit()\
"""
    m.compile(f"build/TestBits{n}bvcomp", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBits{n}bvcomp.v",
                             f"gold/TestBits{n}bvcomp.v")

    sim = PythonSimulator(TestBinary)
    for i in range(2):
        I0 = BitVector.random(n)
        I1 = BitVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == (I0 == I1)


@pytest.mark.parametrize("n", [1, 3])
@pytest.mark.parametrize("x", [4, 7])
def test_repeat(n, x):
    class TestRepeat(m.Circuit):
        io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bits[n * x]))
        io.O <= io.I.repeat(x)

    if n == 1:
        wires = "\n".join(f"wire(TestRepeat.I[{i}], TestRepeat.O[{i + j * n}])"
                          for j in range(x) for i in range(n))
    else:
        assert n == 3
        wires = "\n".join(f"wire(TestRepeat.I, TestRepeat.O[slice({i * n}, {(i + 1) * n}, None)])"
                          for i in range(x))
    assert repr(TestRepeat) == f"""\
TestRepeat = DefineCircuit("TestRepeat", "I", In(Bits[{n}]), "O", Out(Bits[{n * x}]))
{wires}
EndCircuit()\
"""
    m.compile(f"build/TestBits{n}x{x}Repeat",
              TestRepeat, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBits{n}x{x}Repeat.v",
                             f"gold/TestBits{n}x{x}Repeat.v")

    sim = PythonSimulator(TestRepeat)
    for i in range(2):
        I = BitVector.random(n)
        sim.set_value(TestRepeat.I, I)
        sim.evaluate()
        assert sim.get_value(TestRepeat.O) == I.repeat(x)


@pytest.mark.parametrize("op", [operator.and_, operator.or_, operator.xor,
                                operator.lshift, operator.rshift, operator.add,
                                operator.sub, operator.mul])
def test_rops(op):
    x = BitVector.random(5)

    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[5]), O=m.Out(m.Bits[5]))
        io.O @= op(x, io.I)

    sim = PythonSimulator(Main)
    I = BitVector.random(5)
    sim.set_value(Main.I, I)
    sim.evaluate()
    assert sim.get_value(Main.O) == op(x, I)


@pytest.mark.parametrize("op, op_str", [
    (operator.and_, "&"),
    (operator.or_, "|"),
    (operator.xor, "^"),
    (operator.lshift, "<<"),
    (operator.rshift, ">>"),
    (operator.add, "+"),
    (operator.sub, "-"),
    (operator.mul, "*")
])
def test_rop_type_error(op, op_str):
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]))
        with pytest.raises(TypeError) as e:
            print(op(BitVector[32](0xDEADBEEF), io.I))
        assert str(e.value) == (
            f"unsupported operand type(s) for {op_str}: 'BitVector[32]' and "
            "'Bits[(2, Out(Bit))]'"
        )

        x = m.Bits[5]()
        y = m.Bits[4]()
        with pytest.raises(TypeError) as e:
            op(x, y)
        assert str(e.value) == (
            f"unsupported operand type(s) for {op_str}: 'Bits[(5, Bit)]' and "
            "'Bits[(4, Bit)]'"
        )


def test_python_bits_from_int_truncation_error():
    class Foo(m.Circuit):
        with pytest.raises(ValueError) as e:
            m.Bits[2](4)
        assert str(e.value) == (
            "Cannot construct Bits[2] with integer 4 (requires truncation)")
        with pytest.raises(ValueError) as e:
            m.bits(4, 2)
        assert str(e.value) == "Cannot convert 4 to a Bits of length 2"


def test_bits_promote():
    class TestBinary(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]), O=m.Out(m.Bits[6]))
        io.O @= Bits[6](io.I)
        assert int(io.O[4].trace()) == 0
        assert int(io.O[5].trace()) == 0


def test_bits_coerce_typeerror():
    class Dummy:
        def __rand__(self, other):
            return other

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]))
        # Bits.__and__ should get a TypeError in _coerce so we then use
        # Dummy.__rand__
        assert (io.I & Dummy()) is io.I
