from hwtypes.bit_vector_abc import TypeFamily
import magma as m


def test_basic():
    assert m.get_family() is m._Family_
    family = m.get_family()
    assert isinstance(family, TypeFamily)
    assert family.Bit is m.Bit
    assert family.BitVector is m.Bits
    assert family.Unsigned is m.UInt
    assert family.Signed is m.SInt
