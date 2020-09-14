import magma as m
from magma.testing import check_files_equal


def test_valid_simple():
    class TestValidSimple(m.Circuit):
        io = m.IO(
            I=m.In(m.Valid[m.Bits[5]]),
            O=m.Out(m.Valid[m.Bits[5]])
        )
        assert isinstance(io.I, m.Valid)
        io.O @= io.I

    m.compile("build/TestValidSimple", TestValidSimple)
    assert check_files_equal(__file__, f"build/TestValidSimple.v",
                             f"gold/TestValidSimple.v")


def test_valid_tuple():
    class TestValidTuple(m.Circuit):
        io = m.IO(
            I=m.In(m.Valid[m.Tuple[m.Bit, m.Bits[5]]]),
            O=m.Out(m.Valid[m.Tuple[m.Bit, m.Bits[5]]])
        )
        io.O @= io.I

    m.compile("build/TestValidTuple", TestValidTuple)
    assert check_files_equal(__file__, f"build/TestValidTuple.v",
                             f"gold/TestValidTuple.v")
