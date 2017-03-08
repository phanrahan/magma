from magma import *

def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    lut1 = Buf()
    assert str(lut1.interface) == 'I : In(Bit) -> O : Out(Bit)'

    lut2 = Buf()
    assert str(lut2.interface) == 'I : In(Bit) -> O : Out(Bit)'

    lut3 = compose(lut1, lut2)
    assert str(lut3.interface) == 'I : In(Bit) -> O : Out(Bit)'
