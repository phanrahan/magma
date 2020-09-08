import magma as m


def test_concat():
    b0 = m.bit(1)
    b1 = m.bits(1, 1)
    bits0 = m.concat(b0, b1)
    bits1 = m.concat(m.bits(b0), b1)
    assert bits0 == bits1
    assert type(bits0) == m.Out(m.Bits[2])


def test_ext():
    x0 = m.sint(1, 1)
    x1 = m.zext_by(x0, 2)
    x2 = m.zext_to(x0, 3)
    assert repr(x1) == "sint(1, 3)"
    assert repr(x1) == repr(x2)

    x3 = m.sext_by(x0, 2)
    x4 = m.sext_to(x0, 3)
    assert repr(x3) == "sint(-1, 3)"
    assert repr(x3) == repr(x4)
