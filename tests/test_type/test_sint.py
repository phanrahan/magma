import operator
import pytest
from magma.testing import check_files_equal
from magma import *

Array2 = Array[2,Bit]
Array4 = Array[4,Bit]

def test():

    A2 = SInt[2]
    B2 = In(SInt[2])
    C2 = Out(SInt[2])
    assert A2 == A2
    assert B2 == B2
    assert C2 == C2

    assert A2 != B2
    assert A2 != C2
    assert B2 != C2

    # A4 = SInt[4]
    # assert A4 == Array4
    # assert A2 != A4


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
    a1 = sint([1,1])
    print(type(a1))
    assert isinstance(a1._value, SInt)


@pytest.mark.parametrize("n", [7, 3])
@pytest.mark.parametrize("op", ["eq", "lt", "le", "gt", "ge"])
def test_compare(n, op):
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.SInt[n]), "I1", m.In(m.SInt[n]), "O", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            io.O <= getattr(operator, op)(io.I0, io.I1)

    op = {
        "eq": "eq",
        "le": "sle",
        "lt": "slt",
        "ge": "sge",
        "gt": "sgt"
    }[op]
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(SInt[{n}]), "I1", In(SInt[{n}]), "O", Out(Bit))
magma_Bits_{n}_{op}_inst0 = magma_Bits_{n}_{op}()
wire(TestBinary.I0, magma_Bits_{n}_{op}_inst0.in0)
wire(TestBinary.I1, magma_Bits_{n}_{op}_inst0.in1)
wire(magma_Bits_{n}_{op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    m.compile(f"build/TestSInt{n}{op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestSInt{n}{op}.v",
                             f"gold/TestSInt{n}{op}.v")


@pytest.mark.parametrize("n", [7, 3])
@pytest.mark.parametrize("op", ["add", "sub", "mul", "floordiv", "mod", "rshift"])
def test_binary(n, op):
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.SInt[n]), "I1", m.In(m.SInt[n]), "O", m.Out(m.SInt[n])]
        @classmethod
        def definition(io):
            io.O <= getattr(operator, op)(io.I0, io.I1)

    if op == "floordiv":
        op = "sdiv"
    elif op == "mod":
        op = "srem"
    elif op == "rshift":
        op = "ashr"
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(SInt[{n}]), "I1", In(SInt[{n}]), "O", Out(SInt[{n}]))
magma_Bits_{n}_{op}_inst0 = magma_Bits_{n}_{op}()
wire(TestBinary.I0, magma_Bits_{n}_{op}_inst0.in0)
wire(TestBinary.I1, magma_Bits_{n}_{op}_inst0.in1)
wire(magma_Bits_{n}_{op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    m.compile(f"build/TestSInt{n}{op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestSInt{n}{op}.v",
                             f"gold/TestSInt{n}{op}.v")


@pytest.mark.parametrize("n", [7, 3])
def test_adc(n):
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.SInt[n]), "I1", m.In(m.SInt[n]), "CIN", m.In(m.Bit), "O", m.Out(m.SInt[n]), "COUT", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            result, carry = io.I0.adc(io.I1, io.CIN)
            io.O <= result
            io.COUT <= carry

    in0_wires = "\n".join(f"wire(TestBinary.I0[{i}], magma_Bits_{n + 1}_add_inst0.in0[{i}])"
                          for i in range(n))
    in0_wires += f"\nwire(TestBinary.I0[{n - 1}], magma_Bits_{n + 1}_add_inst0.in0[{n}])"

    in1_wires = "\n".join(f"wire(TestBinary.I1[{i}], magma_Bits_{n + 1}_add_inst0.in1[{i}])"
                          for i in range(n))
    in1_wires += f"\nwire(TestBinary.I1[{n - 1}], magma_Bits_{n + 1}_add_inst0.in1[{n}])"

    carry_wires = "\n".join(f"wire(GND, magma_Bits_{n + 1}_add_inst1.in1[{i + 1}])" for i in range(n))

    out_wires = "\n".join(f"wire(magma_Bits_{n + 1}_add_inst1.out[{i}], TestBinary.O[{i}])"
                          for i in range(n))
    out_wires += f"\nwire(magma_Bits_{n + 1}_add_inst1.out[{n}], TestBinary.COUT)"

    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(SInt[{n}]), "I1", In(SInt[{n}]), "CIN", In(Bit), "O", Out(SInt[{n}]), "COUT", Out(Bit))
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
    m.compile(f"build/TestSInt{n}adc", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestSInt{n}adc.v",
                             f"gold/TestSInt{n}adc.v")


@pytest.mark.parametrize("n", [7, 3])
def test_negate(n):
    class TestNegate(m.Circuit):
        IO = ["I", m.In(m.SInt[n]), "O", m.Out(m.SInt[n])]
        @classmethod
        def definition(io):
            io.O <= -io.I

    assert repr(TestNegate) == f"""\
TestNegate = DefineCircuit("TestNegate", "I", In(SInt[{n}]), "O", Out(SInt[{n}]))
magma_Bits_{n}_neg_inst0 = magma_Bits_{n}_neg()
wire(TestNegate.I, magma_Bits_{n}_neg_inst0.in)
wire(magma_Bits_{n}_neg_inst0.out, TestNegate.O)
EndCircuit()\
"""
    m.compile(f"build/TestSInt{n}neg", TestNegate, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestSInt{n}neg.v",
                             f"gold/TestSInt{n}neg.v")
