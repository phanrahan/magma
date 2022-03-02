import magma as m


def test_io_flip():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))


    class Bar(m.Circuit):
        io = m.Flip(Foo.io)
        assert io.I.is_input()
        assert io.O.is_output()
