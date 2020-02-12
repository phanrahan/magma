import magma as m
from magma.testing import check_files_equal


def test_temporary_named_value():
    class Main(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            x = m.Bit(name="x")
            m.wire(io.I, x)
            m.wire(x, io.O)

    m.compile("build/test_temporary_named_value", Main)
    check_files_equal(__file__, "build/test_temporary_named_value.v",
                      "gold/test_temporary_named_value.v")
