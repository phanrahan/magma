import itertools
import pytest
import magma as m
from magma import In, Out, Flip
from magma.testing import check_files_equal
from magma.bit import Bit, VCC, GND, Digital
from magma.simulator import PythonSimulator
import operator
BitIn = In(Bit)
BitOut = Out(Bit)


def test_bit():
    assert m.Bit == m.Bit
    assert m.BitIn == m.BitIn
    assert m.BitOut == m.BitOut

    assert m.Bit == m.BitIn
    assert m.Bit == m.BitOut
    assert m.BitIn == m.BitOut

    assert m.Bit is not m.BitIn
    assert m.Bit is not m.BitOut
    assert m.BitIn is not m.BitOut

    assert str(m.Bit) == 'Bit'
    assert str(m.BitIn) == 'In(Bit)'
    assert str(m.BitOut) == 'Out(Bit)'

    assert issubclass(m.Bit, m.Digital)
    assert isinstance(m.Bit(), m.Digital)

    assert issubclass(m.BitIn, m.Digital)
    assert isinstance(m.BitIn(), m.Digital)

    assert issubclass(m.BitIn, In(m.Digital))
    assert isinstance(m.BitIn(), In(m.Digital))

    assert not issubclass(m.BitIn, Out(m.Digital))
    assert not isinstance(m.BitIn(), Out(m.Digital))

    assert issubclass(m.BitIn, m.Bit)
    assert isinstance(m.BitIn(), m.Bit)

    assert not issubclass(m.BitIn, m.BitOut)
    assert not isinstance(m.BitIn(), m.BitOut)

    assert issubclass(m.BitOut, m.Digital)
    assert isinstance(m.BitOut(), m.Digital)

    assert issubclass(m.BitOut, Out(m.Digital))
    assert isinstance(m.BitOut(), Out(m.Digital))

    assert issubclass(m.BitOut, m.Bit)
    assert isinstance(m.BitOut(), m.Bit)

    assert not issubclass(m.BitOut, m.BitIn)
    assert not isinstance(m.BitOut(), m.BitIn)

    assert not issubclass(m.BitOut, In(m.Digital))
    assert not isinstance(m.BitOut(), In(m.Digital))

    assert m.Bit().is_oriented(m.Direction.Undirected)


@pytest.mark.parametrize("T, direction",
                         itertools.product([m.Digital, m.Bit, m.Clock],
                                           [m.In, m.Out]))
def test_const_bit(T, direction):
    T = direction(T)
    assert isinstance(T(), T)
    assert not T().const()
    for val in 0, 1:
        expected_name = "VCC" if val else "GND"
        bit = T(val)
        assert isinstance(bit, T.undirected_t)
        assert bit.name.name == expected_name


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
    # b0 is treated as an output connected to b1 (treated as input)
    m.wire(b0, b1)

    assert b0.wired()
    assert b1.wired()

    assert b1.driven(), "Should be driven by input"
    assert b1.trace() is b0, "Should trace to b0"

    assert b1.value() is b0, "Value is b0"

    assert b0.driving() == [b1]
    assert b0.value() is b1

    assert b0 is b1._wire.driver.bit
    assert b1 is b0._wire.driving()[0]


def test_wire2():
    b0 = BitOut(name='b0')
    assert b0.is_output()

    b1 = BitIn(name='b1')
    assert b1.is_input()

    m.wire(b1, b0)

    assert b0.wired()
    assert b1.wired()

    assert b0.wired()
    assert b1.wired()

    assert b1.driven(), "Should be driven by input"
    assert b1.trace() is b0, "Should trace to b0"

    assert b1.value() is b0, "Value is b0"
    assert b0.value() is b1, "Value is b1"

    assert b0.driving() == [b1]

    assert b0 is b1._wire.driver.bit
    assert b1 is b0._wire.driving()[0]


def test_wire3():
    b0 = Bit(name='b0')
    b1 = Bit(name='b1')

    m.wire(b0, b1)

    assert b0.wired()
    assert b1.wired()

    assert b0.value() is b1
    assert b1.value() is b0

    assert b0.driving() == [b1]


def test_wire4():
    b0 = BitIn(name='b0')
    b1 = BitIn(name='b1')

    m.wire(b0, b1)

    assert not b0.wired()
    assert not b1.wired()

    assert b0.trace() is None
    assert b1.trace() is None

    assert b0.value() is None
    assert b1.value() is None

    assert b1.driving() == []
    assert b0.driving() == []


def test_wire5():
    b0 = BitOut(name='b0')
    b1 = BitOut(name='b1')

    m.wire(b0, b1)

    assert not b0.wired()
    assert not b1.wired()

    assert b1.driving() == []
    assert b0.driving() == []
    assert b1.value() is None
    assert b0.value() is None


def test_invert():
    class TestInvert(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
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

    sim = PythonSimulator(TestInvert)
    for I in [0, 1]:
        sim.set_value(TestInvert.I, I)
        sim.evaluate()
        assert sim.get_value(TestInvert.O) == (0 if I else 1)


@pytest.mark.parametrize("op", ["and_", "or_", "xor"])
def test_binary(op):
    class TestBinary(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
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

    sim = PythonSimulator(TestBinary)
    for I0, I1 in zip([0, 1], [0, 1]):
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == getattr(operator, op)(I0, I1)


def test_eq():
    class TestBinary(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
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
    m.compile(f"build/TestBiteq", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBiteq.v",
                             f"gold/TestBiteq.v")

    sim = PythonSimulator(TestBinary)
    for I0, I1 in zip([0, 1], [0, 1]):
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == (I0 == I1)


def test_ne():
    class TestBinary(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
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
    m.compile(f"build/TestBitne", TestBinary, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBitne.v",
                             f"gold/TestBitne.v")

    sim = PythonSimulator(TestBinary)
    for I0, I1 in zip([0, 1], [0, 1]):
        sim.set_value(TestBinary.I0, I0)
        sim.set_value(TestBinary.I1, I1)
        sim.evaluate()
        assert sim.get_value(TestBinary.O) == (I0 != I1)


def test_ite():
    class TestITE(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), S=m.In(m.Bit),
                  O=m.Out(m.Bit))

        io.O <= io.S.ite(io.I0, io.I1)

    assert repr(TestITE) == """\
TestITE = DefineCircuit("TestITE", "I0", In(Bit), "I1", In(Bit), "S", In(Bit), \
"O", Out(Bit))
Mux2xBit_inst0 = Mux2xBit()
wire(TestITE.I1, Mux2xBit_inst0.I0)
wire(TestITE.I0, Mux2xBit_inst0.I1)
wire(TestITE.S, Mux2xBit_inst0.S)
wire(Mux2xBit_inst0.O, TestITE.O)
EndCircuit()\
""", repr(TestITE)
    m.compile(f"build/TestBitite", TestITE, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/TestBitite.v",
                             f"gold/TestBitite.v")

    sim = PythonSimulator(TestITE)
    for I0, I1, S in zip([0, 1], [0, 1], [0, 1]):
        sim.set_value(TestITE.I0, I0)
        sim.set_value(TestITE.I1, I1)
        sim.set_value(TestITE.S, S)
        sim.evaluate()
        assert sim.get_value(TestITE.O) == (I1 if S else I0)


@pytest.mark.parametrize("op", [int, bool])
def test_errors(op):
    with pytest.raises(ValueError):
        op(m.Bit(name="b"))
