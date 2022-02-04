import magma as m
import operator
import pytest
from magma.testing import check_files_equal
from magma import *
from magma.simulator import PythonSimulator
from hwtypes import SIntVector

Array2 = Array[2, Bit]
Array4 = Array[4, Bit]


def test():

    A2 = SInt[2]
    B2 = In(SInt[2])
    C2 = Out(SInt[2])
    assert A2 == A2
    assert B2 == B2
    assert C2 == C2

    assert A2 == B2
    assert A2 == C2
    assert B2 == C2

    assert A2 is not B2
    assert A2 is not C2
    assert B2 is not C2

    A4 = SInt[4]
    assert A4 == Array4
    assert A2 != A4


def test_val():
    Array4In = In(SInt[4])
    Array4Out = Out(SInt[4])

    assert Flip(Array4In) == Array4Out
    assert Flip(Array4Out) == Array4In

    a0 = Array4Out(name='a0')
    print(a0)

    a1 = Array4In(name='a1')
    print(a1)

    a1.wire(a0)

    b0 = a1[0]

    a3 = a1[0:2]


def test_flip():
    SInt2 = SInt[2]
    AIn = In(SInt2)
    AOut = Out(SInt2)

    print(AIn)
    print(AOut)

    assert AIn == Array2
    assert AOut == Array2
    assert AIn == AOut

    assert AIn is not Array2
    assert AOut is not Array2
    assert AIn is not AOut

    A = In(AOut)
    assert A == AIn
    print(A)

    A = Flip(AOut)
    assert A == AIn

    A = Out(AIn)
    assert A == AOut

    A = Flip(AIn)
    assert A == AOut
    print(A)


def test_construct():
    class Foo(m.Circuit):
        a1 = sint([1, 1])
        print(type(a1))
        assert isinstance(a1, SInt)
        assert isinstance(a1, Bits)
        assert not isinstance(a1, UInt)

        assert isinstance(SInt[15](a1), SInt)
        assert repr(SInt[16](
            a1)) == "SInt[16](-1)"

        # Test explicit conversion
        assert isinstance(uint(a1), UInt)
        assert not isinstance(uint(a1), SInt)

        assert not isinstance(uint(1, 1), SInt)


@pytest.mark.parametrize("n", [7, 3])
@pytest.mark.parametrize("op", ["eq", "lt", "le", "gt", "ge"])
def test_compare(n, op):
    class TestBinary(Circuit):
        io = IO(I0=In(SInt[n]), I1=In(SInt[n]), O=Out(Bit))
        io.O <= getattr(operator, op)(io.I0, io.I1)

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = SIntVector.random(n)
        I1 = SIntVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == getattr(operator, op)(I0, I1)

    op = {
        "eq": "eq",
        "le": "sle",
        "lt": "slt",
        "ge": "sge",
        "gt": "sgt"
    }[op]
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(SInt[{n}]), "I1", In(SInt[{n}]), "O", Out(Bit))
magma_SInt_{n}_{op}_inst0 = magma_SInt_{n}_{op}()
wire(TestBinary.I0, magma_SInt_{n}_{op}_inst0.in0)
wire(TestBinary.I1, magma_SInt_{n}_{op}_inst0.in1)
wire(magma_SInt_{n}_{op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    compile(f"build/TestSInt{n}{op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestSInt{n}{op}.v",
                             f"gold/TestSInt{n}{op}.v")


@pytest.mark.parametrize("n", [7, 3])
@pytest.mark.parametrize("op", ["add", "sub", "mul", "floordiv", "mod", "rshift"])
def test_binary(n, op):
    class TestBinary(Circuit):
        io = IO(I0=In(SInt[n]), I1=In(SInt[n]), O=Out(SInt[n]))
        io.O <= getattr(operator, op)(io.I0, io.I1)

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = SIntVector.random(n)
        I1 = SIntVector.random(n)
        if op in ["floordiv", "mod"]:
            while I1 == 0:
                I1 = SIntVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == getattr(operator, op)(I0, I1)

    if op == "floordiv":
        op = "sdiv"
    elif op == "mod":
        op = "srem"
    elif op == "rshift":
        op = "ashr"
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(SInt[{n}]), "I1", In(SInt[{n}]), "O", Out(SInt[{n}]))
magma_SInt_{n}_{op}_inst0 = magma_SInt_{n}_{op}()
wire(TestBinary.I0, magma_SInt_{n}_{op}_inst0.in0)
wire(TestBinary.I1, magma_SInt_{n}_{op}_inst0.in1)
wire(magma_SInt_{n}_{op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    compile(f"build/TestSInt{n}{op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestSInt{n}{op}.v",
                             f"gold/TestSInt{n}{op}.v")


@pytest.mark.parametrize("n", [7, 3])
def test_adc(n):
    class TestBinary(Circuit):
        io = IO(I0=In(SInt[n]), I1=In(SInt[n]), CIN=In(
            Bit), O=Out(SInt[n]), COUT=Out(Bit))

        result, carry = io.I0.adc(io.I1, io.CIN)
        io.O <= result
        io.COUT <= carry

    carry_wires = "\n".join(
        f"wire(GND, magma_SInt_{n + 1}_add_inst1.in1[{i + 1}])" for i in range(n))


    if n > 1:
        in0_wires = f"wire(TestBinary.I0, magma_SInt_{n + 1}_add_inst0.in0[slice(0, {n}, None)])"
    else:
        in0_wires = "\n".join(f"wire(TestBinary.I0[{i}], magma_SInt_{n + 1}_add_inst0.in0[{i}])"
                              for i in range(n))
    in0_wires += f"\nwire(TestBinary.I0[{n - 1}], magma_SInt_{n + 1}_add_inst0.in0[{n}])"

    if n > 1:
        in1_wires = f"wire(TestBinary.I1, magma_SInt_{n + 1}_add_inst0.in1[slice(0, {n}, None)])"
    else:
        in1_wires = "\n".join(f"wire(TestBinary.I1[{i}], magma_SInt_{n + 1}_add_inst0.in1[{i}])"
                              for i in range(n))
    in1_wires += f"\nwire(TestBinary.I1[{n - 1}], magma_SInt_{n + 1}_add_inst0.in1[{n}])"

    carry_wires = "\n".join(
        f"wire(GND, magma_SInt_{n + 1}_add_inst1.in1[{i + 1}])" for i in range(n))

    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(SInt[{n}]), "I1", In(SInt[{n}]), "CIN", In(Bit), "O", Out(SInt[{n}]), "COUT", Out(Bit))
magma_SInt_{n + 1}_add_inst0 = magma_SInt_{n + 1}_add()
magma_SInt_{n + 1}_add_inst1 = magma_SInt_{n + 1}_add()
{in0_wires}
{in1_wires}
wire(magma_SInt_{n + 1}_add_inst0.out, magma_SInt_{n + 1}_add_inst1.in0)
wire(TestBinary.CIN, magma_SInt_{n + 1}_add_inst1.in1[0])
{carry_wires}
wire(magma_SInt_{n + 1}_add_inst1.out[slice(0, {n}, None)], TestBinary.O)
wire(magma_SInt_{n + 1}_add_inst1.out[{n}], TestBinary.COUT)
EndCircuit()\
"""
    compile(f"build/TestSInt{n}adc", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestSInt{n}adc.v",
                             f"gold/TestSInt{n}adc.v")

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = SIntVector.random(n)
        I1 = SIntVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == I0 + I1
        assert sim.get_value(TestBinary.COUT) == (I0.sext(1) + I1.sext(1))[-1]


@pytest.mark.parametrize("n", [7, 3])
def test_negate(n):
    class TestNegate(Circuit):
        io = IO(I=In(SInt[n]), O=Out(SInt[n]))
        io.O <= -io.I

    assert repr(TestNegate) == f"""\
TestNegate = DefineCircuit("TestNegate", "I", In(SInt[{n}]), "O", Out(SInt[{n}]))
magma_SInt_{n}_neg_inst0 = magma_SInt_{n}_neg()
wire(TestNegate.I, magma_SInt_{n}_neg_inst0.in)
wire(magma_SInt_{n}_neg_inst0.out, TestNegate.O)
EndCircuit()\
"""
    compile(f"build/TestSInt{n}neg", TestNegate, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestSInt{n}neg.v",
                             f"gold/TestSInt{n}neg.v")

    sim = PythonSimulator(TestNegate)
    for _ in range(2):
        I = SIntVector.random(n)
        sim.set_value(TestNegate.I, I)
        sim.evaluate()
        assert sim.get_value(TestNegate.O) == -I


@pytest.mark.parametrize("op", [operator.floordiv, operator.mod])
def test_rops(op):
    x = SIntVector.random(5)

    class Main(m.Circuit):
        io = m.IO(I=m.In(m.SInt[5]), O=m.Out(m.SInt[5]))
        io.O @= op(x, io.I)

    sim = PythonSimulator(Main)
    I = SIntVector.random(5)
    while I == 0:
        # Avoid divide by 0
        I = SIntVector.random(5)

    sim.set_value(Main.I, I)
    sim.evaluate()
    assert sim.get_value(Main.O) == op(x, I)


@pytest.mark.parametrize("op, op_str", [
    (operator.floordiv, "//"),
    (operator.mod, "%")
])
def test_rop_type_error(op, op_str):
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.SInt[2]))
        with pytest.raises(TypeError) as e:
            print(op(SIntVector[32](0xDEADBEEF), io.I))
        assert str(e.value) == (
            f"unsupported operand type(s) for {op_str}: 'SIntVector[32]' and "
            "'SInt[(2, Out(Bit))]'"
        )

        x = m.SInt[5]()
        y = m.SInt[4]()
        with pytest.raises(TypeError) as e:
            op(x, y)
        assert str(e.value) == (
            f"unsupported operand type(s) for {op_str}: 'SInt[(5, Bit)]' and "
            "'SInt[(4, Bit)]'"
        )


def test_sint_promote():
    class TestBinary(Circuit):
        io = IO(I=In(SInt[3]), O=Out(SInt[6]))
        io.O @= SInt[6](io.I)
        assert io.O[4].trace() is io.I[-1]
        assert io.O[5].trace() is io.I[-1]
