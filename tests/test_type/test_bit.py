from magma import *

def test():
    assert isinstance(Bit,    BitKind)
    assert isinstance(BitIn,  BitKind)
    assert isinstance(BitOut, BitKind)

    assert not Bit._isinput()
    assert not Bit._isoutput()

    assert BitIn._isinput()
    assert BitOut._isoutput()

    assert Bit == Bit
    assert BitIn == BitIn
    assert BitOut == BitOut

    assert Bit != BitIn
    assert Bit != BitOut
    assert BitIn != BitOut

    assert str(Bit) == 'Bit'
    assert str(BitIn) == 'In(Bit)'
    assert str(BitOut) == 'Out(Bit)'
