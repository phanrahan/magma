from magma import Bit, BitIn, BitOut, BitType, BitKind, In, Out, Flip

def test_bit():
    assert isinstance(Bit,    BitKind)
    assert isinstance(BitIn,  BitKind)
    assert isinstance(BitOut, BitKind)

    assert not Bit.isinput()
    assert not Bit.isoutput()

    assert BitIn.isinput()
    assert BitOut.isoutput()

    assert Bit == Bit
    assert BitIn == BitIn
    assert BitOut == BitOut

    assert Bit != BitIn
    assert Bit != BitOut
    assert BitIn != BitOut

    assert str(Bit) == 'Bit'
    assert str(BitIn) == 'In(Bit)'
    assert str(BitOut) == 'Out(Bit)'

def test_bit_flip():
    bout = Out(Bit)
    bin = In(Bit)
    assert bout == BitOut
    assert bin == BitIn

    bin = In(BitIn)
    bout = Out(BitIn)
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
