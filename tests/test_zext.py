import magma as m
from hwtypes import BitVector


def test_zext():
    result = m.zext(m.concat(m.bits(4), m.bits(5)), 3)
    assert m.bits(result).bits() == \
        BitVector[3](4).concat(BitVector[3](5))\
                       .concat(BitVector[3](0)).bits()
