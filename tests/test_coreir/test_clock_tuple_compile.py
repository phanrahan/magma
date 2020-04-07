import magma as m
import magma.testing
from magma.testing import check_files_equal


def test_auto_wire_tuple_clocks():
    class Intf(m.Product):
        clk = m.In(m.Clock)
        rst = m.In(m.Reset)

    class Foo(m.Circuit):
        io = m.IO(clocks=Intf, I=m.In(m.Bit), O=m.Out(m.Bit))

    class Main(m.Circuit):
        io = m.IO(clocks=Intf, I=m.In(m.Bit), O=m.Out(m.Bit))

        foo = Foo()
        foo.I @= io.I
        io.O @= foo.O


    m.compile("build/test_auto_wire_tuple_clocks", Main)
    check_files_equal(__file__,
        "build/test_auto_wire_tuple_clocks.v",
        "gold/test_auto_wire_tuple_clocks.v"
                      )
