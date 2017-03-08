from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    Or2 = DeclareCircuit('Or2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    lut0 = uncurry(And2())
    lut1 = uncurry(Or2())
    lut = flat(lut0,lut1)
    assert str(lut.interface) == 'I : Array(4,In(Bit)) -> O : Array(2,Out(Bit))'
