from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    lut0 = And2(name='lut0')
    lut1 = And2(name='lut1')

    lut = braid([lut0,lut1])
    print(repr(lut))

    lut = braid([lut0,lut1], foldargs={'I1':'O'})
    print(repr(lut))

    lut = braid([lut0,lut1], scanargs={'I1':'O'})
    print(repr(lut))

test()
