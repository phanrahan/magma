import magma as m
from magma.testing import check_files_equal


def test_const_logic():
    class Main(m.Circuit):
        io = m.IO(O=m.Out(m.Array[1, m.Bits[3]]))

        io.O @= m.array([m.bits(0, 3)])

    m.compile("build/test_const", Main, output="coreir")
    assert check_files_equal(__file__, f"build/test_const.json",
                             f"gold/test_const.json")
