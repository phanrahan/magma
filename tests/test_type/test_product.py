import magma as m


def test_anon_product_literal():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        x = m.AnonProduct[{"I": m.Bit, "CE": m.Bit}]()
        x @= m.product(I=io.I, CE=False)
    assert Foo.x.CE.value() is m.GND
