import pytest
import magma as m
from magma import In, Out, Flip
from magma.testing import check_files_equal
from magma.bit import Bit, VCC, GND, Digital
import operator
BitIn = In(Bit)
BitOut = Out(Bit)


def test_bit():
    assert m.Bit == m.Bit
    assert m.BitIn == m.BitIn
    assert m.BitOut == m.BitOut

    assert m.Bit != m.BitIn
    assert m.Bit != m.BitOut
    assert m.BitIn != m.BitOut

    assert str(m.Bit) == 'Bit'
    assert str(m.BitIn) == 'In(Bit)'
    assert str(m.BitOut) == 'Out(Bit)'


def test_bit_flip():

    bout = Out(Bit)
    bin = In(Bit)
    assert bout == BitOut
    assert bin == BitIn

    bin = In(BitIn)
    bout = Out(BitOut)
    assert bout == BitOut
    assert bin == BitIn

    bin = In(BitOut)
    bout = Out(BitOut)
    assert bout == BitOut
    assert bin == BitIn

    bin = Flip(BitOut)
    bout = Flip(BitIn)
    assert bout == BitOut
    assert bin == BitIn


def test_bit_val():
    b = BitIn(name="a")
    assert isinstance(b, Bit)
    assert isinstance(b, BitIn)
    assert b.is_input()
    assert str(b) == "a"
    assert isinstance(b, BitIn)
    assert b.is_input()

    b = BitOut(name="a")
    assert b.is_output()
    assert str(b) == "a"
    assert isinstance(b, Bit)
    assert isinstance(b, BitOut)
    assert b.is_output()

    b = Bit(name="a")
    assert str(b) == "a"
    assert isinstance(b, Bit)
    assert isinstance(b, Bit)
    assert not b.is_input()
    assert not b.is_output()
    assert not b.is_inout()


def test_vcc():
    assert str(VCC) == "VCC"
    assert isinstance(VCC, Digital)

    assert str(GND) == "GND"
    assert isinstance(GND, Digital)

    assert VCC is VCC
    assert VCC is not GND
    assert GND is GND


def test_wire1():
    b0 = BitOut(name='b0')
    assert b0.is_output()

    b1 = BitIn(name='b1')
    assert b1.is_input()

    print('wire(b0,b1)')
    m.wire(b0, b1)
    assert b0.port.wires is b1.port.wires

    # wires = b0.port.wires
    # print 'inputs:', [str(p) for p in wires.inputs]
    # print 'outputs:', [str(p) for p in wires.outputs]
    assert len(b0.port.wires.inputs) == 1
    assert len(b0.port.wires.outputs) == 1

    assert b0.wired()
    assert b1.wired()

    assert b0.trace() is b1
    assert b1.trace() is b0

    assert b0.value() is None
    assert b1.value() is b0


def test_wire2():
    b0 = BitOut(name='b0')
    assert b0.is_output()

    b1 = BitIn(name='b1')
    assert b1.is_input()

    print('wire(b1,b0)')
    m.wire(b1, b0)
    assert b0.port.wires is b1.port.wires

    # wires = b0.port.wires
    # print 'inputs:', [str(p) for p in wires.inputs]
    # print 'outputs:', [str(p) for p in wires.outputs]

    assert len(b0.port.wires.inputs) == 1
    assert len(b0.port.wires.outputs) == 1

    assert b0.wired()
    assert b1.wired()

    assert b0.trace() is b1
    assert b1.trace() is b0

    assert b0.value() is None
    assert b1.value() is b0


def test_wire3():
    b0 = Bit(name='b0')
    b1 = Bit(name='b1')

    print('wire(b0,b1)')
    m.wire(b0, b1)
    assert b0.port.wires is b1.port.wires

    # wires = b0.port.wires
    # print 'inputs:', [str(p) for p in wires.inputs]
    # print 'outputs:', [str(p) for p in wires.outputs]
    assert len(b0.port.wires.inputs) == 1
    assert len(b0.port.wires.outputs) == 1

    assert b0.wired()
    assert b1.wired()

    assert b0.trace() is b1
    assert b1.trace() is b0

    assert b0.value() is None
    assert b1.value() is b0


def test_wire4():
    b0 = BitIn(name='b0')
    b1 = BitIn(name='b1')

    print('wire(b0,b1)')
    m.wire(b0, b1)
    # assert b0.port.wires is b1.port.wires

    # wires = b0.port.wires
    # print 'inputs:', [str(p) for p in wires.inputs]
    # print 'outputs:', [str(p) for p in wires.outputs]

    assert len(b0.port.wires.inputs) == 0
    assert len(b0.port.wires.outputs) == 0

    assert not b0.wired()
    assert not b1.wired()

    assert b0.trace() is None
    assert b1.trace() is None

    assert b0.value() is None
    assert b1.value() is None


def test_wire5():
    b0 = BitOut(name='b0')
    b1 = BitOut(name='b1')

    print('wire(b0,b1)')
    m.wire(b0, b1)
    # assert b0.port.wires is b1.port.wires

    # wires = b0.port.wires
    # print 'inputs:', [str(p) for p in wires.inputs]
    # print 'outputs:', [str(p) for p in wires.outputs]

    assert len(b0.port.wires.inputs) == 0
    assert len(b0.port.wires.outputs) == 0

    assert not b0.wired()
    assert not b1.wired()

    assert b0.trace() is None
    assert b1.trace() is None

    assert b0.value() is None
    assert b1.value() is None


def test_invert():
    class TestInvert(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            io.O <= ~io.I

    assert repr(TestInvert) == """\
TestInvert = DefineCircuit("TestInvert", "I", In(Bit), "O", Out(Bit))
magma_Bit_not_inst0 = magma_Bit_not()
wire(TestInvert.I, magma_Bit_not_inst0.in)
wire(magma_Bit_not_inst0.out, TestInvert.O)
EndCircuit()\
"""
    m.compile("build/TestBitInvert", TestInvert, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBitInvert.v",
                             f"gold/TestBitInvert.v")


@pytest.mark.parametrize("op", ["and_", "or_", "xor"])
def test_binary(op):
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.Bit), "I1", m.In(m.Bit), "O", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            io.O <= getattr(operator, op)(io.I0, io.I1)

    clean_op = op.replace("_", "")
    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(Bit), "I1", In(Bit), \
"O", Out(Bit))
magma_Bit_{clean_op}_inst0 = magma_Bit_{clean_op}()
wire(TestBinary.I0, magma_Bit_{clean_op}_inst0.in0)
wire(TestBinary.I1, magma_Bit_{clean_op}_inst0.in1)
wire(magma_Bit_{clean_op}_inst0.out, TestBinary.O)
EndCircuit()\
"""
    m.compile(f"build/TestBit{clean_op}", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBit{clean_op}.v",
                             f"gold/TestBit{clean_op}.v")


def test_eq():
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.Bit), "I1", m.In(m.Bit), "O", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            # Nasty precidence issue with <= operator means we need parens here
            io.O <= (io.I0 == io.I1)

    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(Bit), "I1", In(Bit), \
"O", Out(Bit))
magma_Bit_not_inst0 = magma_Bit_not()
magma_Bit_xor_inst0 = magma_Bit_xor()
wire(magma_Bit_xor_inst0.out, magma_Bit_not_inst0.in)
wire(TestBinary.I0, magma_Bit_xor_inst0.in0)
wire(TestBinary.I1, magma_Bit_xor_inst0.in1)
wire(magma_Bit_not_inst0.out, TestBinary.O)
EndCircuit()\
"""


def test_ne():
    class TestBinary(m.Circuit):
        IO = ["I0", m.In(m.Bit), "I1", m.In(m.Bit), "O", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            # Nasty precidence issue with <= operator means we need parens here
            io.O <= (io.I0 != io.I1)

    assert repr(TestBinary) == f"""\
TestBinary = DefineCircuit("TestBinary", "I0", In(Bit), "I1", In(Bit), \
"O", Out(Bit))
magma_Bit_xor_inst0 = magma_Bit_xor()
wire(TestBinary.I0, magma_Bit_xor_inst0.in0)
wire(TestBinary.I1, magma_Bit_xor_inst0.in1)
wire(magma_Bit_xor_inst0.out, TestBinary.O)
EndCircuit()\
"""


def test_ite():
    class TestITE(m.Circuit):
        IO = ["I0", m.In(m.Bit), "I1", m.In(m.Bit), "S", m.In(m.Bit),
              "O", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            io.O <= io.S.ite(io.I0, io.I1)

    assert repr(TestITE) == """\
TestITE = DefineCircuit("TestITE", "I0", In(Bit), "I1", In(Bit), "S", In(Bit), \
"O", Out(Bit))
magma_Bit_ite_Out_Bit_inst0 = magma_Bit_ite_Out_Bit()
wire(TestITE.I0, magma_Bit_ite_Out_Bit_inst0.in0)
wire(TestITE.I1, magma_Bit_ite_Out_Bit_inst0.in1)
wire(TestITE.S, magma_Bit_ite_Out_Bit_inst0.sel)
wire(magma_Bit_ite_Out_Bit_inst0.out, TestITE.O)
EndCircuit()\
"""


@pytest.mark.parametrize("op", [int, bool])
def test_errors(op):
    with pytest.raises(NotImplementedError):
        op(m.Bit(name="b"))
