import pytest
import magma as m
from magma.testing import magma_debug_section
from magma.testing.utils import has_error


def _make_unconnected_io():
    class _Circuit(m.Circuit):
        io = m.IO(I=m.In(m.Bits[1]), O=m.Out(m.Bits[2]))

        # Leave io.O[1] unwired.
        io.O[0] <= io.I[0]

    return _Circuit


def _make_unconnected_instance():
    class _Buffer(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        io.O <= io.I

    class _Circuit(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        buf = _Buffer()
        # Leave buf.I unwired.
        io.O <= buf.O

    return _Circuit


def _make_unconnected_autowired(typ):
    class _Buffer(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit), X=m.In(typ))

        io.O <= io.I

    class _Circuit(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit), X=m.In(typ))

        buf = _Buffer()
        buf.I <= io.I
            io.O <= buf.O

    return _Circuit


def test_unconnected_io(caplog):
    with magma_debug_section():
        Circuit = _make_unconnected_io()
        expected = """\x1b[1mtests/test_circuit/test_unconnected.py:8\x1b[0m: Output port _Circuit.O not driven
>>     class _Circuit(m.Circuit):"""
        assert has_error(caplog, expected)


def test_unconnected_instance(caplog):
    with magma_debug_section():
        Circuit = _make_unconnected_instance()
        expected = """\x1b[1mtests/test_circuit/test_unconnected.py:32\x1b[0m: Input port buf.I not driven
>>             buf = _Buffer()"""
        assert has_error(caplog, expected)


@pytest.mark.parametrize("typ", [m.Clock, m.Reset, m.AsyncReset])
def test_unconnected_autowired(typ, caplog):
    with magma_debug_section():
        Circuit = _make_unconnected_autowired(typ)
        assert not any("not driven" in log.msg for log in caplog.records)
