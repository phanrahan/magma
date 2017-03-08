from magma import *

def test():
    LUT2 = DeclareCircuit('LUT2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    lut1 = LUT2()
    assert str(lut1.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'

    lut2 = uncurry(lut1)
    assert str(lut2.interface) == 'I : Array(2,In(Bit)) -> O : Out(Bit)'

    lut3 = curry(lut2)
    assert str(lut3.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'
