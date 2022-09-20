import pytest
import magma as m


def test_uint_sint(caplog):
    # Should not be able to wire uint/sint
    class Main(m.Circuit):
        io = m.IO(a=m.In(m.UInt[16]), b=m.Out(m.SInt[16]))
        io.b @= io.a
        assert not io.b.driven()
    expected = """\
Cannot wire Main.a (Out(UInt[16])) to Main.b (In(SInt[16]))\
"""
    assert caplog.messages[0][-len(expected):] == expected

    class Main2(m.Circuit):
        io = m.IO(a=m.In(m.SInt[16]), b=m.Out(m.UInt[16]))
        io.b @= io.a
        assert not io.b.driven()
    expected = """\
Cannot wire Main2.a (Out(SInt[16])) to Main2.b (In(UInt[16]))\
"""
    assert caplog.messages[1][-len(expected):] == expected


@pytest.mark.parametrize('Ts', [
    (m.Bit, m.Bits[1]),
    (m.Bits[1], m.Bit),
])
def test_bit_bits1(Ts):
    class Main(m.Circuit):
        io = m.IO(a=m.In(Ts[0]), b=m.Out(Ts[1]))
        io.b @= io.a

    # NOTE: We  call compile here to ensure a wiring error was not reported
    # (otherwise it would raise an exception)
    m.compile('build/Main', Main)
