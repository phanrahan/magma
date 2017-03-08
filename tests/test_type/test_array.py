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


