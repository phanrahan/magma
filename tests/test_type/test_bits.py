from magma import *

Array2 = Array[2, Bit]
Array4 = Array[4, Bit]

def test():

    A2 = Bits[2]
    B2 = In(Bits[2])
    C2 = Out(Bits[2])
    assert A2 == A2
    assert B2 == B2
    assert C2 == C2

    assert A2 != B2
    assert A2 != C2
    assert B2 != C2

    # A4 = Bits[4]
    # assert A4 == Array4
    # assert A2 != A4


def test_val():
    Array4In = In(Bits[4])
    Array4Out = Out(Bits[4])

    assert Flip(Array4In) == Array4Out
    assert Flip(Array4Out) == Array4In

    a0 = Array4Out(name='a0')
    print(a0)

    a1 = Array4In(name='a1')
    print(a1)

    a1.wire(a0)

    b0 = a1[0]

    a3 = a1[0:2]

def test_flip():
    Bits2 = Bits[2]
    AIn = In(Bits2)
    AOut = Out(Bits2)

    print(AIn)
    print(AOut)

    assert AIn  != Array2
    assert AOut != Array2
    assert AIn != AOut

    A = In(AOut)
    assert A == AIn
    print(A)

    A = Flip(AOut)
    assert A == AIn

    A = Out(AIn)
    assert A == AOut

    A = Flip(AIn)
    assert A == AOut
    print(A)

def test_construct():
    a1 = bits([1,1])
    print(type(a1))
    assert isinstance(a1, BitsType)

def test_const():
    Data = Bits[16]
    zero = Data(0)
