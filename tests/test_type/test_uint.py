from magma.testing import check_files_equal
import operator
import pytest
from magma import *

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


@pytest.mark.parametrize("n", [1, 3])
@pytest.mark.parametrize("op", ["eq", "lt", "le", "gt", "ge"])
def test_compare(n, op):
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.UInt[n]), "I1", m.In(m.UInt[n]), "O", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            io.O <= getattr(operator, op)(io.I0, io.I1)

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
