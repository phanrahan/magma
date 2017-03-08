from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    lut0 = And2()
    lut1 = And2()

    lut = braid([lut0,lut1])
    assert str(lut.interface) == 'I0 : Array(2,In(Bit)), I1 : Array(2,In(Bit)) -> O : Array(2,Out(Bit))'

    lut = braid([lut0,lut1], foldargs={'I1':'O'})
    assert str(lut.interface) == 'I0 : Array(2,In(Bit)), I1 : In(Bit) -> O : Out(Bit)'

    lut = braid([lut0,lut1], scanargs={'I1':'O'})
    assert str(lut.interface) == 'I0 : Array(2,In(Bit)), I1 : In(Bit) -> O : Array(2,Out(Bit))'
