from magma import *

def test():
    ROM2 = DeclareCircuit('ROM2', "I", In(Array(2,Bit)), "O", Out(Bit))
    rom1 = ROM2()
    assert str(rom1.interface) == 'I : Array(2,In(Bit)) -> O : Out(Bit)'

    rom2 = curry(rom1)
    assert str(rom2.interface) == 'I0 : In(Bit), I1 : In(Bit) -> O : Out(Bit)'

    rom3 = uncurry(rom2)
    assert str(rom3.interface) == 'I : Array(2,In(Bit)) -> O : Out(Bit)'
