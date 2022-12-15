from magma import *

def test_braid():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class _Top(Circuit):
        io = IO()
        lut0 = And2(name='lut0')
        lut1 = And2(name='lut1')

        lut = braid([lut0,lut1])
        assert repr(lut) == 'AnonymousCircuitType("I0", array([lut0.I0, lut1.I0]), "I1", array([lut0.I1, lut1.I1]), "O", array([lut0.O, lut1.O]))'

        lut = braid([lut0,lut1], foldargs={'I1':'O'})
        assert repr(lut) == 'AnonymousCircuitType("I0", array([lut0.I0, lut1.I0]), "I1", lut0.I1, "O", lut1.O)'

        lut = braid([lut0,lut1], scanargs={'I1':'O'})
        assert repr(lut) == 'AnonymousCircuitType("I0", array([lut0.I0, lut1.I0]), "I1", lut0.I1, "O", array([lut0.O, lut1.O]))'


def test_compose():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class _Top(Circuit):
        io = IO()
        lut1 = Buf(name='lut1')
        lut2 = Buf(name='lut2')
        lut3 = compose(lut1, lut2)

    lut1 = _Top.lut1
    lut2 = _Top.lut2
    lut3 = _Top.lut3

    assert repr(lut1) == 'lut1 = Buf(name="lut1")'
    assert repr(lut2) == 'lut2 = Buf(name="lut2")'
    assert repr(lut3) == 'AnonymousCircuitType("I", lut2.I, "O", lut1.O)'


