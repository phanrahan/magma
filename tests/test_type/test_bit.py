from magma import Bit, BitIn, BitOut, BitType, BitKind, In, Out, Flip, VCC, GND, wire

def test_bit():
    assert isinstance(Bit,    BitKind)
    assert isinstance(BitIn,  BitKind)
    assert isinstance(BitOut, BitKind)

    #assert not Bit.isinput()
    #assert not Bit.isoutput()

    #assert BitIn.isinput()
    #assert BitOut.isoutput()

    assert Bit is Bit
    assert BitIn is BitIn
    assert BitOut is BitOut

    assert Bit is not BitIn
    assert Bit is not BitOut
    assert BitIn is not BitOut

    assert str(Bit) == 'Bit'
    assert str(BitIn) == 'In(Bit)'
    assert str(BitOut) == 'Out(Bit)'

def test_bit_flip():
    bout = Out(Bit)
    bin = In(Bit)
    assert bout is BitOut
    assert bin is BitIn

    bin = In(BitIn)
    bout = Out(BitIn)
    assert bout is BitOut
    assert bin is BitIn

    bin = In(BitOut)
    bout = Out(BitOut)
    assert bout is BitOut
    assert bin is BitIn

    bin = Flip(BitOut)
    bout = Flip(BitIn)
    assert bout is BitOut
    assert bin is BitIn

def test_bit_val():
    b = BitIn(name="a")
    assert isinstance(b, BitType)
    assert isinstance(b, BitIn)
    assert b.isinput()
    assert str(b) == "a"
    assert isinstance(b, BitIn)
    assert b.isinput()

    b = BitOut(name="a")
    assert b.isoutput()
    assert str(b) == "a"
    assert isinstance(b, BitOut)
    assert b.isoutput()

    b = Bit(name="a")
    assert str(b) == "a"
    assert isinstance(b, Bit)
    assert not b.isinput()
    assert not b.isoutput()
    assert not b.isinout()

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
    assert b0.isoutput()

    b1 = BitIn(name='b1')
    assert b1.isinput()

    print('wire(b0,b1)')
    wire(b0,b1)
    assert b0.port.wires is b1.port.wires

    #wires = b0.port.wires
    #print 'inputs:', [str(p) for p in wires.inputs]
    #print 'outputs:', [str(p) for p in wires.outputs]
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
    assert b0.isoutput()

    b1 = BitIn(name='b1')
    assert b1.isinput()

    print('wire(b1,b0)')
    wire(b1,b0)
    assert b0.port.wires is b1.port.wires

    #wires = b0.port.wires
    #print 'inputs:', [str(p) for p in wires.inputs]
    #print 'outputs:', [str(p) for p in wires.outputs]

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
    wire(b0,b1)
    assert b0.port.wires is b1.port.wires

    #wires = b0.port.wires
    #print 'inputs:', [str(p) for p in wires.inputs]
    #print 'outputs:', [str(p) for p in wires.outputs]
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
    wire(b0,b1)
    #assert b0.port.wires is b1.port.wires

    #wires = b0.port.wires
    #print 'inputs:', [str(p) for p in wires.inputs]
    #print 'outputs:', [str(p) for p in wires.outputs]

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
    wire(b0,b1)
    #assert b0.port.wires is b1.port.wires

    #wires = b0.port.wires
    #print 'inputs:', [str(p) for p in wires.inputs]
    #print 'outputs:', [str(p) for p in wires.outputs]

    assert len(b0.port.wires.inputs) == 0
    assert len(b0.port.wires.outputs) == 0

    assert not b0.wired()
    assert not b1.wired()

    assert b0.trace() is None
    assert b1.trace() is None

    assert b0.value() is None
    assert b1.value() is None
