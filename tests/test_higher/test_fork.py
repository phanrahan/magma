from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    Or2 = DeclareCircuit('Or2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    lut0 = And2()
    assert str(lut0.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'

    lut1 = Or2()
    assert str(lut1.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'

    lut = fork(lut0,lut1)
    assert str(lut.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Array(2,Out(Bit))'
