from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    and1 = And2()
    assert str(and1.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'

    and2 = uncurry(and1)
    assert str(and2.interface) == 'I : Array(2,In(Bit)) -> O : Out(Bit)'

    and3 = curry(and2)
    assert str(and3.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'
