import magma as m


def test_sfixed_simple():
    x = m.SFixed[-1.5, 1.5, .1]
    assert True, "Creating an SFixed should not crash"

