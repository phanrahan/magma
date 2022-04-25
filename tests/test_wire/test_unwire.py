import pytest
import magma as m


@pytest.mark.parametrize('T', [m.Bit, m.Bits[4], m.Tuple[m.Bit, m.Bits[4]],
                               m.Array[4, m.Bits[4]]])
@pytest.mark.parametrize('func', [lambda x, y: x.unwire(y), m.unwire])
def test_unwire_with_arg(T, func, caplog):
    class Foo(m.Circuit):
        io = m.IO(I0=m.In(T), I1=m.In(T), O=m.Out(T))
        io.O @= io.I0
        func(io.O, io.I0)
        io.O @= io.I1

    assert len(caplog.records) == 0


@pytest.mark.parametrize('T', [m.Bit, m.Bits[4], m.Tuple[m.Bit, m.Bits[4]],
                               m.Array[4, m.Bits[4]]])
@pytest.mark.parametrize('func', [lambda x: x.unwire(), m.unwire])
def test_unwire_no_arg(T, func, caplog):
    class Foo(m.Circuit):
        io = m.IO(I0=m.In(T), I1=m.In(T), O=m.Out(T))
        io.O @= io.I0
        func(io.O)
        io.O @= io.I1

    assert len(caplog.records) == 0
