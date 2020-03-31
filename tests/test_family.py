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
    for t in (m.Bit, m.Bits[1], m.UInt[1], m.SInt[1]):
        assert t.get_family() is family
