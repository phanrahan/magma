from magma import *

def test():
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
