from magma import *

def test_flat():
    F = DeclareCircuit('F', "I", In(Array[2,Bits[2]]), "O", Out(Bit))
    f = F(name="f")
    g = flat(f)
    print(g)
    assert len(g.interface) == 2
    assert len(g.I) == 4

def test_partition():
    F = DeclareCircuit('F', "I", In(Bits[4]), "O", Out(Bit))
    f = F(name="f")
    g = partition(f, 2)
    print(g.interface)
    assert len(g.interface) == 3
    assert len(g.I0) == 2
    assert len(g.I1) == 2

test_flat()

