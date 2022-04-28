import magma as m
from magma.testing import check_files_equal


def test_when_with_default():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S) as cond:
            io.O @= io.I[0]

    m.compile("build/test_when_with_default", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_with_default.v",
                             "gold/test_when_with_default.v")


def test_when_nested_with_default():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S[0]) as c0:
            with m.when(io.S[1]) as c1:
                io.O @= io.I[0]

    m.compile("build/test_when_nested_with_default", Foo, inline=True)
    assert check_files_equal(__file__,
                             "build/test_when_nested_with_default.v",
                             "gold/test_when_nested_with_default.v")
