import magma as m
from magma.bit import In, Out, Bit, Flip, VCC, GND
BitIn = Bit[In]
BitOut = Bit[Out]


def test_bit():
    assert m.Bit == m.Bit
    assert m.BitIn == m.BitIn
    assert m.BitOut == m.BitOut

    assert m.Bit != m.BitIn
    assert m.Bit != m.BitOut
    assert m.BitIn != m.BitOut

    assert str(m.Bit) == 'Bit'
    assert str(m.BitIn) == 'Bit[In]'
    assert str(m.BitOut) == 'Bit[Out]'


def test_bit_flip():

    bout = Bit[Out]
    bin = Bit[In]
    assert bout == BitOut
    assert bin == BitIn

    bin = BitIn[In]
    bout = BitOut[Out]
    assert bout == BitOut
    assert bin == BitIn

    bin = BitOut[In]
    bout = BitOut[Out]
    assert bout == BitOut
    assert bin == BitIn

    bin = BitOut[Flip]
    bout = BitIn[Flip]
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
    assert isinstance(VCC, BitOut)

    assert str(GND) == "GND"
    assert isinstance(GND, BitOut)

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
