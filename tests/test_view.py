import magma as m
from magma.view import PortView


def test_port_view_ref():
    T = m.Product.from_fields("anon", dict(x=m.Bit, y=m.Bit))

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T))

    x = PortView[type(Foo.I)](Foo.I, None)
    assert x._get_magma_value_().name.view is x

    y = T()
    y @= x

    assert y.value() is x._get_magma_value_()
    assert y.x.value() is x._get_magma_value_().x
    #assert y.x.value() is x.x._get_magma_value_()
