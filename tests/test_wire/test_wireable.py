import magma as m


def test_uint_sint(caplog):
    # Should not be able to wire uint/sint
    class Main(m.Circuit):
        io = m.IO(a=m.In(m.UInt[16]), b=m.Out(m.SInt[16]))
        io.b @= io.a
        assert not io.b.driven()
    assert caplog.messages[0] == 'Cannot wire Main.b (SInt) to Main.a (UInt)'

    class Main(m.Circuit):
        io = m.IO(a=m.In(m.SInt[16]), b=m.Out(m.UInt[16]))
        io.b @= io.a
        assert not io.b.driven()
    assert caplog.messages[1] == 'Cannot wire Main.b (UInt) to Main.a (SInt)'
