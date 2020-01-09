from magma import *
import pytest

Array2 = Array[2,Bit]
Array4 = Array[4,Bit]

def test_array():
    print(Array2)

    A2 = Array[2,Bit]
    B2 = Array[2,BitIn]
    C2 = Array[2,BitOut]
    assert A2 == A2
    assert B2 == B2
    assert C2 == C2

    assert A2 != B2
    assert A2 != C2
    assert B2 != C2

    A4 = Array[4,Bit]
    assert A4 == Array4
    assert A2 != A4

    assert issubclass(m.In(m.Array[2, m.Bit]), m.In(m.Array[2, m.Bit]))
    assert isinstance(m.In(m.Array[2, m.Bit])(), m.In(m.Array[2, m.Bit]))

    assert issubclass(m.In(m.Array[2, m.Bit]), m.Array[2, m.Bit])
    assert isinstance(m.In(m.Array[2, m.Bit])(), m.Array[2, m.Bit])

    assert not issubclass(m.In(m.Array[2, m.Bit]), m.Out(m.Array[2, m.Bit]))
    assert not isinstance(m.In(m.Array[2, m.Bit])(), m.Out(m.Array[2, m.Bit]))


def test_val():
    Array4In = Array[4, BitIn]
    Array4Out = Array[4, BitOut]

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

    A24 = Array[2,Array[4,Bit]]
    print(A24)

    assert isinstance(A24, ArrayMeta)

    assert A24 == Array[2,Array4]

    # constructor

    a = A24(name='a')
    assert isinstance(a, ArrayType)
    print(a[0])
    assert isinstance(a[0], ArrayType)
    print(a[0][0])
    assert isinstance(a[0][0], Bit)


def test_construct():
    a1 = Array[2, Bit]([1,1])
    print(type(a1))
    assert isinstance(a1, ArrayType)

    a1 = Array[2, Bit](0x3)
    assert a1 == m.array([VCC, VCC])

    with pytest.raises(TypeError):
        a1 = Array[2, Array[3, Bit]](0x3)

def test_whole():
    Reg2 = DefineCircuit("Reg2", "I0", In(Array2), "I1", In(Array2))
    a = Reg2.I0
    a1 = Array[2, Bit]([a[0], a[1]])
    print((a1.iswhole(a1.ts)))

    reg2 = Reg2()
    a = reg2.I0
    b = reg2.I1

    a1 = Array[2, Bit]([a[0], a[1]])
    print((a1.iswhole(a1.ts)))

    a2 = Array[2, Bit]([a[0], b[1]])
    print((a2.iswhole(a2.ts)))

    a3 = Array[2, Bit]([0,1])
    print((a3.iswhole(a3.ts)))

    a4 = a3[:1]
    print((a4.iswhole(a4.ts)))

def test_wire():
    a0 = Array2(name='a0')
    #assert a0.direction is None

    a1 = Array2(name='a1')
    #assert a1.direction is None

    wire(a0, a1)

    assert a0.wired()
    assert a1.wired()

    assert a1.driven()

    assert a0.trace() is a1
    assert a1.trace() is a0

    #print a0.driven()
    assert a0.value() is None
    assert a1.value() is a0

    b0 = a0[0]
    b1 = a1[0]

    assert b0.port.wires is b1.port.wires

    wires = b0.port.wires
    assert len(b0.port.wires.inputs) == 1
    assert len(b0.port.wires.outputs) == 1
    print('inputs:', [str(p) for p in wires.inputs])
    print('outputs:', [str(p) for p in wires.outputs])
