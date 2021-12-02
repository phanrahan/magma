from magma import *


def test_1():
    I0 = make_interface("a", In(Bit), "b", Out(Bits[2]))
    assert str(I0) == 'Interface("a", In(Bit), "b", Out(Bits[2]))'

    i0 = I0()
    print(i0)
    assert str(i0) == 'Interface("a", In(Bit), "b", Out(Bits[2]))'
