from magma import *

def test():
    ROM2 = DeclareCircuit('ROM2', "I", In(Array(2,Bit)), "O", Out(Bit))
    rom1 = ROM2()
    rom2 = curry(rom1)
    rom3 = uncurry(rom2)
    print(repr(rom1))
    print(repr(rom2))
    print(repr(rom3))

test()
