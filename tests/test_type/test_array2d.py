from magma import *

def test():
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
