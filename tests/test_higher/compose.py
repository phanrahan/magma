from magma import *

def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    lut1 = Buf(name='lut1')
    lut2 = Buf(name='lut2')
    lut3 = compose(lut1, lut2)

    print(repr(lut1))
    print(repr(lut2))
    print(repr(lut3))

test()

