from magma import *

def test():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))
    assert str(And2) == 'And2'
    print(repr(And2))
    assert repr(And2) == 'And2 = DeclareCircuit("And2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))'

    and2 = And2()
    and2.name = 'and2'
    assert str(and2) == 'and2'
    print(repr(and2))
    assert str(and2.I0) == 'I0'
    print(repr(and2.I0))

test()
