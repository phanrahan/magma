from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    print(repr(And2))
    and2 = And2()
    print(repr(type(and2)))
    and2.name = 'and2'
    print(and2)
    print(repr(and2))
    #assert str(lut0.interface) == '"I0", In(Bit), "I1", In(Bit), "O", Out(Bit)'

    Or2 = DeclareCircuit('Or2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    or2 = Or2()
    or2.name = 'or2'
    print(or2)
    print(repr(type(or2)))
    #assert str(or2.interface) == '"I0", In(Bit), "I1", In(Bit), "O", Out(Bit)'

    lut = fork(and2,or2)
    print(lut)
    #print(repr(lut.interface))
    print(type(lut))
    print(repr(lut))
    #assert str(lut.interface) == '"I0", In(Bit), "I1", In(Bit), "O", Out(Array(2,Bit))'

test()
