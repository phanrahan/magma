from magma import *

def test_lut():
    class LUT2(Circuit):
        name = "LUT2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class _Top(Circuit):
        io = IO()
        lut1 = LUT2(name='lut1')
        lut2 = uncurry(lut1)
        lut3 = curry(lut2)

    lut1 = _Top.lut1
    lut2 = _Top.lut2
    lut3 = _Top.lut3

    assert repr(lut1) == 'lut1 = LUT2(name="lut1")'
    assert repr(lut2) == 'AnonymousCircuitType("I", array([lut1.I0, lut1.I1]), "O", lut1.O)'
    assert repr(lut3) == 'AnonymousCircuitType("I0", lut1.I0, "I1", lut1.I1, "O", lut1.O)'

def test_rom():
    class ROM2(Circuit):
        name = "ROM2"
        io = IO(I=In(Array[2,Bit]), O=Out(Bit))

    class _Top(Circuit):
        io = IO()
        rom1 = ROM2(name='rom1')
        rom2 = curry(rom1)
        rom3 = uncurry(rom2)

    rom1 = _Top.rom1
    rom2 = _Top.rom2
    rom3 = _Top.rom3

    assert repr(rom1) == 'rom1 = ROM2(name="rom1")'
    assert repr(rom2) == 'AnonymousCircuitType("I0", rom1.I[0], "I1", rom1.I[1], "O", rom1.O)'
    assert repr(rom3) == 'AnonymousCircuitType("I", array([rom1.I[0], rom1.I[1]]), "O", rom1.O)'


