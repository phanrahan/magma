import magma as m


def test_anon_product_literal():
    I = m.Bit()
    x = m.AnonProduct[{"I": m.Bit, "CE": m.Bit}]()
    x @= m.product(I=I, CE=False)
    assert x.CE.value() is m.GND
