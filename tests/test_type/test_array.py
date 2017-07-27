from magma import *

def test():
    print(Array2)

    A2 = Array(2,Bit)
    B2 = Array(2,BitIn)
    C2 = Array(2,BitOut)
    assert A2 == A2
    assert B2 == B2
    assert C2 == C2

    assert A2 != B2
    assert A2 != C2
    assert B2 != C2

    A4 = Array(4,Bit)
    assert A4 == Array4
    assert A2 != A4


def test_val():
    Array4In = Array(4, BitIn)
    Array4Out = Array(4, BitOut)

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
    AIn = In(Array2)
    AOut = Out(Array2)

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

def test_array2d():
    # types

    A24 = Array(2,Array(4,Bit))
    print(A24)

    assert isinstance(A24, ArrayKind)

    assert A24 == Array(2,Array4)

    # constructor

    a = A24(name='a')
    assert isinstance(a, ArrayType)
    print(a[0])
    assert isinstance(a[0], ArrayType)
    print(a[0][0])
    assert isinstance(a[0][0], BitType)


def test_construct():
    a1 = array(1,1)
    print(type(a1))
    assert isinstance(a1, ArrayType)
