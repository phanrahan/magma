import magma as m


def test_sfixed_simple():
    x = m.SFixed[-1.5, 1.5, .1]
    assert x.low == -1.5
    assert x.high == 1.5
    assert x.step == .1
