from magma import *

def test():
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
