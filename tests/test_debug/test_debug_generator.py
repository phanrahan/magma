import magma as m
from magma.testing import check_files_equal


def test_debug_generator_basic():
    class Foo(m.Generator2):
        @m.debug
        def __init__(self, n):
            self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bit))
            x = m.Bits[n]()
            x @= ~self.io.I
            self.io.O @= x.reduce_xor()

    m.compile("build/test_debug_generator_basic", Foo(4), inline=True)
    assert check_files_equal(__file__,
                             "build/test_debug_generator_basic.v",
                             "gold/test_debug_generator_basic.v")
