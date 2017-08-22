from magma import *

def test():
    LUT2 = DeclareCircuit('LUT2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    lut1 = LUT2(name='lut1')
    lut2 = uncurry(lut1)
    lut3 = curry(lut2)
    print(repr(lut1))
    print(repr(lut2))
    print(repr(lut3))

test()
