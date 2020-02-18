from magma.testing import check_files_equal
import operator
import pytest
from magma import *
from magma.simulator import PythonSimulator
from hwtypes import BitVector

Array2 = Array[2,Bit]
Array4 = Array[4,Bit]

def test():

    A2 = UInt[2]
    B2 = In(UInt[2])
    C2 = Out(UInt[2])
    assert A2 == A2
    assert B2 == B2
    assert C2 == C2

    assert A2 != B2
    assert A2 != C2
    assert B2 != C2

    # A4 = UInt[4]
    # assert A4 == Array4
    # assert A2 != A4


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

    assert AIn  != Array2
    assert AOut != Array2
    assert AIn != AOut

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
    a1 = uint([1,1])
    print(type(a1))
    assert isinstance(a1, UInt)
    assert isinstance(a1, Bits)
    assert not isinstance(a1, SInt)

    assert isinstance(UInt[15](a1), UInt)
    assert repr(m.UInt[16](a1)) == "bits([VCC, VCC, GND, GND, GND, GND, GND, GND, GND, GND, GND, GND, GND, GND, GND, GND])"

    # Test explicit conversion
    assert isinstance(sint(a1), SInt)
    assert not isinstance(sint(a1), UInt)

    assert not isinstance(sint(1, 1), UInt)


@pytest.mark.parametrize("n", [1, 3])
@pytest.mark.parametrize("op", ["eq", "lt", "le", "gt", "ge"])
def test_compare(n, op):
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.UInt[n]), "I1", m.In(m.UInt[n]), "O", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            io.O <= getattr(operator, op)(io.I0, io.I1)

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = BitVector.random(n)
        I1 = BitVector.random(n)
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
magma_Bits_{n}_{op}_inst0 = magma_Bits_{n}_{op}()
wire(TestBinary.I0, magma_Bits_{n}_{op}_inst0.in0)
wire(TestBinary.I1, magma_Bits_{n}_{op}_inst0.in1)
wire(magma_Bits_{n}_{op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    m.compile(f"build/TestUInt{n}{op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestUInt{n}{op}.v",
                             f"gold/TestUInt{n}{op}.v")


@pytest.mark.parametrize("n", [1, 3])
@pytest.mark.parametrize("op", ["add", "sub", "mul", "floordiv", "mod"])
def test_binary(n, op):
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.UInt[n]), "I1", m.In(m.UInt[n]), "O", m.Out(m.UInt[n])]
        @classmethod
        def definition(io):
            io.O <= getattr(operator, op)(io.I0, io.I1)

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = BitVector.random(n)
        I1 = BitVector.random(n)
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
magma_Bits_{n}_{op}_inst0 = magma_Bits_{n}_{op}()
wire(TestBinary.I0, magma_Bits_{n}_{op}_inst0.in0)
wire(TestBinary.I1, magma_Bits_{n}_{op}_inst0.in1)
wire(magma_Bits_{n}_{op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    m.compile(f"build/TestUInt{n}{op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestUInt{n}{op}.v",
                             f"gold/TestUInt{n}{op}.v")


@pytest.mark.parametrize("n", [1, 3])
def test_adc(n):
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.UInt[n]), "I1", m.In(m.UInt[n]), "CIN", m.In(m.Bit), "O", m.Out(m.UInt[n]), "COUT", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            result, carry = io.I0.adc(io.I1, io.CIN)
            io.O <= result
            io.COUT <= carry

    in0_wires = "\n".join(f"wire(TestBinary.I0[{i}], magma_Bits_{n + 1}_add_inst0.in0[{i}])"
                          for i in range(n))
    in0_wires += f"\nwire(GND, magma_Bits_{n + 1}_add_inst0.in0[{n}])"

    in1_wires = "\n".join(f"wire(TestBinary.I1[{i}], magma_Bits_{n + 1}_add_inst0.in1[{i}])"
                          for i in range(n))
    in1_wires += f"\nwire(GND, magma_Bits_{n + 1}_add_inst0.in1[{n}])"

    carry_wires = "\n".join(f"wire(GND, magma_Bits_{n + 1}_add_inst1.in1[{i + 1}])" for i in range(n))

    out_wires = "\n".join(f"wire(magma_Bits_{n + 1}_add_inst1.out[{i}], TestBinary.O[{i}])"
                          for i in range(n))
    out_wires += f"\nwire(magma_Bits_{n + 1}_add_inst1.out[{n}], TestBinary.COUT)"

    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(UInt[{n}]), "I1", In(UInt[{n}]), "CIN", In(Bit), "O", Out(UInt[{n}]), "COUT", Out(Bit))
magma_Bits_{n + 1}_add_inst0 = magma_Bits_{n + 1}_add()
magma_Bits_{n + 1}_add_inst1 = magma_Bits_{n + 1}_add()
{in0_wires}
{in1_wires}
wire(magma_Bits_{n + 1}_add_inst0.out, magma_Bits_{n + 1}_add_inst1.in0)
wire(TestBinary.CIN, magma_Bits_{n + 1}_add_inst1.in1[0])
{carry_wires}
{out_wires}
EndCircuit()\
"""
    m.compile(f"build/TestUInt{n}adc", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestUInt{n}adc.v",
                             f"gold/TestUInt{n}adc.v")

    sim = PythonSimulator(TestBinary)
    for _ in range(2):
        I0 = BitVector.random(n)
        I1 = BitVector.random(n)
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == I0 + I1
        assert sim.get_value(TestBinary.COUT) == (I0.zext(1) + I1.zext(1))[-1]
