import magma as m


def test_concat():
    b0 = m.bit(1)
    b1 = m.bits(1, 1)
    bits0 = m.concat(b0, b1)
    bits1 = m.concat(m.bits(b0), b1)
    assert bits0 == bits1
    assert type(bits0) == m.Out(m.Bits[2])
