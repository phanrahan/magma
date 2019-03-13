from magma import *

def test_lut():
    LUT2 = DeclareCircuit('LUT2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    lut1 = LUT2(name='lut1')
    lut2 = uncurry(lut1)
    lut3 = curry(lut2)
    assert repr(lut1) == 'lut1 = LUT2(name="lut1")'
    assert repr(lut2) == 'AnonymousCircuitType("I", array([lut1.I0, lut1.I1]), "O", lut1.O)'
    assert repr(lut3) == 'AnonymousCircuitType("I0", lut1.I0, "I1", lut1.I1, "O", lut1.O)'

def test_rom():
    ROM2 = DeclareCircuit('ROM2', "I", In(Array[2,Bit]), "O", Out(Bit))
    rom1 = ROM2(name='rom1')
    rom2 = curry(rom1)
    rom3 = uncurry(rom2)
    assert repr(rom1) == 'rom1 = ROM2(name="rom1")'
    assert repr(rom2) == 'AnonymousCircuitType("I0", rom1.I[0], "I1", rom1.I[1], "O", rom1.O)'
    assert repr(rom3) == 'AnonymousCircuitType("I", array([rom1.I[0], rom1.I[1]]), "O", rom1.O)'


