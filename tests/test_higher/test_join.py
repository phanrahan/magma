from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    and0 = And2()
    assert str(and0.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'

    and1 = And2()
    assert str(and1.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'

    a = join(and0, and1)
    assert str(a.interface) == 'I0 : Array(2,In(Bit)), I1 : Array(2,In(Bit)) -> O : Array(2,Out(Bit))'
