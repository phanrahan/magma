import magma as m
from hwtypes import modifiers

def test_732():
    Mod = modifiers.make_modifier("Mod")

    BV = m.Bits[8]
    ModBits = Mod(m.Bits)
    ModBV = Mod(BV)

    assert issubclass(ModBV, BV)
    assert issubclass(ModBV, ModBits)
