import magma as m
from magma.testing import check_files_equal
import operator
import pytest
from magma import *
from magma.simulator import PythonSimulator
from hwtypes import UIntVector

Array2 = Array[2, Bit]
Array4 = Array[4, Bit]


def test():

    A2 = UInt[2]
    B2 = In(UInt[2])
    C2 = Out(UInt[2])
    assert A2 == A2
    assert B2 == B2
    assert C2 == C2

    assert A2 == B2
    assert A2 == C2
    assert B2 == C2

    assert A2 is not B2
    assert A2 is not C2
    assert B2 is not C2

    A4 = UInt[4]
    assert A4 == Array4
    assert A2 != A4


def test_val():
    Array4In = In(UInt[4])
    Array4Out = Out(UInt[4])

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
    UInt2 = UInt[2]
    AIn = In(UInt2)
    AOut = Out(UInt2)

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
        a1 = uint([1, 1])
        print(type(a1))
        assert isinstance(a1, UInt)
        assert isinstance(a1, Bits)
        assert not isinstance(a1, SInt)

        assert isinstance(UInt[15](a1), UInt)
        assert repr(UInt[16](
            a1)) == "UInt[16](3)"

        # Test explicit conversion
        assert isinstance(sint(a1), SInt)
        assert not isinstance(sint(a1), UInt)

        assert not isinstance(sint(1, 1), UInt)


@pytest.mark.parametrize("n", [1, 3])
@pytest.mark.parametrize("op", ["eq", "lt", "le", "gt", "ge"])
def test_compare(n, op):
    class TestBinary(Circuit):
        io = IO(I0=In(UInt[n]), I1=In(UInt[n]), O=Out(Bit))
        io.O <= getattr(operator, op)(io.I0, io.I1)

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = UIntVector.random(n)
        I1 = UIntVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == getattr(operator, op)(I0, I1)

    op = {
        "eq": "eq",
        "le": "ule",
        "lt": "ult",
        "ge": "uge",
        "gt": "ugt"
    }[op]
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(UInt[{n}]), "I1", In(UInt[{n}]), "O", Out(Bit))
magma_UInt_{n}_{op}_inst0 = magma_UInt_{n}_{op}()
wire(TestBinary.I0, magma_UInt_{n}_{op}_inst0.in0)
wire(TestBinary.I1, magma_UInt_{n}_{op}_inst0.in1)
wire(magma_UInt_{n}_{op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    compile(f"build/TestUInt{n}{op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestUInt{n}{op}.v",
                             f"gold/TestUInt{n}{op}.v")


@pytest.mark.parametrize("n", [1, 3])
@pytest.mark.parametrize("op", ["add", "sub", "mul", "floordiv", "mod"])
def test_binary(n, op):
    class TestBinary(Circuit):
        io = IO(I0=In(UInt[n]), I1=In(UInt[n]), O=Out(UInt[n]))
        io.O <= getattr(operator, op)(io.I0, io.I1)

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = UIntVector.random(n)
        I1 = UIntVector.random(n)
        if op in ["floordiv", "mod"]:
            while I1 == 0:
                I1 = UIntVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == getattr(operator, op)(I0, I1)

    if op == "floordiv":
        op = "udiv"
    elif op == "mod":
        op = "urem"
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(UInt[{n}]), "I1", In(UInt[{n}]), "O", Out(UInt[{n}]))
magma_UInt_{n}_{op}_inst0 = magma_UInt_{n}_{op}()
wire(TestBinary.I0, magma_UInt_{n}_{op}_inst0.in0)
wire(TestBinary.I1, magma_UInt_{n}_{op}_inst0.in1)
wire(magma_UInt_{n}_{op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    compile(f"build/TestUInt{n}{op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestUInt{n}{op}.v",
                             f"gold/TestUInt{n}{op}.v")


@pytest.mark.parametrize("n", [1, 3])
def test_adc(n):
    class TestBinary(Circuit):
        io = IO(I0=In(UInt[n]), I1=In(UInt[n]), CIN=In(
            Bit), O=Out(UInt[n]), COUT=Out(Bit))

        result, carry = io.I0.adc(io.I1, io.CIN)
        io.O <= result
        io.COUT <= carry

    if n > 1:
        in0_wires = f"wire(TestBinary.I0, magma_UInt_{n + 1}_add_inst0.in0[slice(0, {n}, None)])"
    else:
        in0_wires = "\n".join(f"wire(TestBinary.I0[{i}], magma_UInt_{n + 1}_add_inst0.in0[{i}])"
                              for i in range(n))
    in0_wires += f"\nwire(GND, magma_UInt_{n + 1}_add_inst0.in0[{n}])"

    if n > 1:
        in1_wires = f"wire(TestBinary.I1, magma_UInt_{n + 1}_add_inst0.in1[slice(0, {n}, None)])"
    else:
        in1_wires = "\n".join(f"wire(TestBinary.I1[{i}], magma_UInt_{n + 1}_add_inst0.in1[{i}])"
                              for i in range(n))
    in1_wires += f"\nwire(GND, magma_UInt_{n + 1}_add_inst0.in1[{n}])"

    carry_wires = "\n".join(
        f"wire(GND, magma_UInt_{n + 1}_add_inst1.in1[{i + 1}])" for i in range(n))

    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(UInt[{n}]), "I1", In(UInt[{n}]), "CIN", In(Bit), "O", Out(UInt[{n}]), "COUT", Out(Bit))
magma_UInt_{n + 1}_add_inst0 = magma_UInt_{n + 1}_add()
magma_UInt_{n + 1}_add_inst1 = magma_UInt_{n + 1}_add()
{in0_wires}
{in1_wires}
wire(magma_UInt_{n + 1}_add_inst0.out, magma_UInt_{n + 1}_add_inst1.in0)
wire(TestBinary.CIN, magma_UInt_{n + 1}_add_inst1.in1[0])
{carry_wires}
wire(magma_UInt_{n + 1}_add_inst1.out[slice(0, {n}, None)], TestBinary.O)
wire(magma_UInt_{n + 1}_add_inst1.out[{n}], TestBinary.COUT)
EndCircuit()\
"""
    compile(f"build/TestUInt{n}adc", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestUInt{n}adc.v",
                             f"gold/TestUInt{n}adc.v")

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = UIntVector.random(n)
        I1 = UIntVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == I0 + I1
        assert sim.get_value(TestBinary.COUT) == (I0.zext(1) + I1.zext(1))[-1]


@pytest.mark.parametrize("op", [operator.floordiv, operator.mod])
def test_rops(op):
    x = UIntVector.random(5)

    class Main(m.Circuit):
        io = m.IO(I=m.In(m.UInt[5]), O=m.Out(m.UInt[5]))
        io.O @= op(x, io.I)

    sim = PythonSimulator(Main)
    I = UIntVector.random(5)
    while I == 0:
        # Avoid divide by 0
        I = UIntVector.random(5)

    sim.set_value(Main.I, I)
    sim.evaluate()
    assert sim.get_value(Main.O) == op(x, I)


@pytest.mark.parametrize("op, op_str", [
    (operator.floordiv, "//"),
    (operator.mod, "%")
])
def test_rop_type_error(op, op_str):
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.UInt[2]))
        with pytest.raises(TypeError) as e:
            print(op(UIntVector[32](0xDEADBEEF), io.I))
        assert str(e.value) == (
            f"unsupported operand type(s) for {op_str}: 'UIntVector[32]' and "
            "'UInt[(2, Out(Bit))]'"
        )

        x = m.UInt[5]()
        y = m.UInt[4]()
        with pytest.raises(TypeError) as e:
            op(x, y)
        assert str(e.value) == (
            f"unsupported operand type(s) for {op_str}: 'UInt[(5, Bit)]' and "
            "'UInt[(4, Bit)]'"
        )


def test_uint_promote():
    class TestBinary(Circuit):
        io = IO(I=In(UInt[3]), O=Out(UInt[6]))
        io.O @= UInt[6](io.I)
        assert int(io.O[4].trace()) == 0
        assert int(io.O[5].trace()) == 0
