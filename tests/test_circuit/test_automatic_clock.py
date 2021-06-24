import magma as m
from magma.testing import check_files_equal


def test_magma_automatic_clock():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= m.Register(m.Bit)()(io.I)

    m.compile("build/Foo", Foo)
    assert check_files_equal(__file__, f"build/Foo.v",
                             f"gold/Foo.v")
