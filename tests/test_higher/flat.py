from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    Or2 = DeclareCircuit('Or2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    lut0 = uncurry(And2(name='and2'))
    lut1 = uncurry(Or2(name='or2'))
    lut = flat(lut0,lut1)
    print(repr(lut0))
    print(repr(lut1))
    print(repr(lut))

test()
