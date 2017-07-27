from magma import *

def test():
    # types

    A2 = Tuple(x=Bit, y=Bit)
    print(A2)
    assert isinstance(A2, TupleKind)
    print(str(A2))
    #assert str(A2) == 'Tuple(x=Bit,y=Bit)'
    assert A2 == A2

    B2 = Tuple(x=In(Bit), y=In(Bit))
    assert isinstance(B2, TupleKind)
    #assert str(B2) == 'Tuple(x=In(Bit),y=In(Bit))'
    assert B2 == B2

    C2 = Tuple(x=Out(Bit), y=Out(Bit))
    assert isinstance(C2, TupleKind)
    #assert str(C2) == 'Tuple(x=Out(Bit),y=Out(Bit))'
    assert C2 == C2

    assert A2 != B2
    assert A2 != C2
    assert B2 != C2

    # functions

    #print('tuple_("x",1,"y",1)')
    #a1 = tuple_("x",1,"y",1)
    #assert isinstance(a1, TupleType)


def test_val():
    A2 = Tuple(x=Bit, y=Bit)

    # constructor

    a = A2(name='a')
    print('created A2')
    assert isinstance(a, TupleType)
    assert str(a) == 'a'

    # selectors

    print('a["x"]')
    b = a['x']
    assert isinstance(b, BitType)
    assert str(b) == 'a.x'

    print('a.x')
    b = a.x
    assert isinstance(b, BitType)
    assert str(b) == 'a.x'

def test_flip():
    Tuple2 = Tuple(x=In(Bit), y=Out(Bit))
    print(Tuple2)
    print(Flip(Tuple2))

    Tin = In(Tuple2)
    Tout = Out(Tuple2)

    print(Tin)
    print(Tout)

    assert Tin != Tuple2
    assert Tout != Tuple2
    assert Tin != Tout

    T = In(Tout)
    assert T == Tin

    T = Flip(Tout)
    assert T == Tin
    print(T)


    T = Out(Tin)
    assert T == Tout

    T = Flip(Tin)
    assert T == Tout
    print(T)

def test_construct():
    print('tuple_("x",1,"y",1)')
    a1 = tuple_("x",1,"y",1)
    assert isinstance(a1, TupleType)
