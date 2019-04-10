import magma as m


def test_sfixed_simple():
    x = m.SFixed[25, 2]
    assert x.W == 25
    assert x.I == 2
