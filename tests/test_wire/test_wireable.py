import pytest
import magma as m


def test_uint_sint(caplog):
    # Should not be able to wire uint/sint
    class Main(m.Circuit):
        io = m.IO(a=m.In(m.UInt[16]), b=m.Out(m.SInt[16]))
        io.b @= io.a
        assert not io.b.driven()
    expected = """\
Cannot wire Main.a (Out(UInt[16])) to Main.b (In(SInt[16]))
>>         io.b @= io.a\
"""
    assert caplog.messages[0][-len(expected):] == expected

    class Main2(m.Circuit):
        io = m.IO(a=m.In(m.SInt[16]), b=m.Out(m.UInt[16]))
        io.b @= io.a
        assert not io.b.driven()
    expected = """\
Cannot wire Main2.a (Out(SInt[16])) to Main2.b (In(UInt[16]))
>>         io.b @= io.a\
"""
    assert caplog.messages[1][-len(expected):] == expected


def test_trace_infinite_loop():
    x = m.Bits[8](name="x")
    y = m.Bits[8](name="y")
    z = m.Bits[8](name="z")

    # Combinational loop
    x @= y
    z @= x
    y @= z
    with pytest.raises(RecursionError) as e:
        y.trace()

    assert str(e.value) == """\
RecursionError when calling trace on y, do you have a \
combinational loop?\
"""
