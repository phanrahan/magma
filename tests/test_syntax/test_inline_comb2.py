import magma as m
from magma.testing import check_files_equal


def test_inline_comb2_basic():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        @m.inline_combinational2
        def logic(self):
            if self.io.I:
                self.io.O @= 0
            else:
                self.io.O @= 1

    m.compile("build/test_inline_comb_basic2", Foo)
    assert check_files_equal(__file__, "build/test_inline_comb_basic2.v",
                             "gold/test_inline_comb_basic2.v")
