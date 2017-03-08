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


