import magma as m
import hwtypes as ht
from magma.type_utils import to_hwtypes


def test_bit_to_ht():
    assert to_hwtypes(m.Bit) is ht.Bit


def test_bits_to_ht():
    assert to_hwtypes(m.Bits[5]) is ht.BitVector[5]


def test_sint_to_ht():
    assert to_hwtypes(m.SInt[5]) is ht.SIntVector[5]


def test_uint_to_ht():
    assert to_hwtypes(m.UInt[5]) is ht.UIntVector[5]


def test_tuple_to_ht():
    assert (to_hwtypes(m.Tuple[m.Bit, m.Bits[5]]) is
            ht.Tuple[ht.Bit, ht.BitVector[5]])


def test_product_to_ht():
    class T(m.Product):
        x = m.Bit
        y = m.Bits[5]

    # Need them to be the same name so we just rename the reference
    MT = T

    class T(ht.Product):
        x = ht.Bit
        y = ht.BitVector[5]

    HTT = T

    assert to_hwtypes(MT) == HTT
