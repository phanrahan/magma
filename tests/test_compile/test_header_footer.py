import os
import magma as m
from magma.testing import check_files_equal


def test_header_footer():
    class Foo(m.Circuit):
        io = m.IO(x=m.In(m.Bit), y=m.Out(m.Bit))

    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        foo = Foo()
        foo.x @= io.I
        io.O @= foo.y

    header_file = os.path.join(os.path.dirname(__file__), "test_header.v")
    m.compile("build/test_header_footer", Main, header_file=header_file,
              header_str="`ifdef FOO", footer_str="`endif")

    assert check_files_equal(__file__, f"build/test_header_footer.v",
                             f"gold/test_header_footer.v")
