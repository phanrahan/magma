import pytest
import magma as m
from magma.testing import magma_debug_section


def _make_unconnected_io():
    class _Circuit(m.Circuit):
        IO = ["I", m.In(m.Bits[1]), "O", m.Out(m.Bits[2])]

        @classmethod
        def definition(io):
            # Leave io.O[1] unwired.
            io.O[0] <= io.I[0]

    return _Circuit


def _make_unconnected_instance():
    class _Buffer(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            io.O <= io.I

    class _Circuit(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            buf = _Buffer()
            # Leave buf.I unwired.
            io.O <= buf.O

    return _Circuit


def _make_unconnected_autowired(typ):
    class _Buffer(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit), "X", m.In(typ)]

        @classmethod
        def definition(io):
            io.O <= io.I

    class _Circuit(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit), "X", m.In(typ)]

        @classmethod
        def definition(io):
            buf = _Buffer()
            buf.I <= io.I
            io.O <= buf.O

    return _Circuit


def test_unconnected_io(caplog):
    with magma_debug_section():
        Circuit = _make_unconnected_io()
        logs = caplog.records
        assert len(logs) == 1
        for log in logs:
            assert log.levelname == "ERROR"
        expected = """\x1b[1mtests/test_circuit/test_unconnected.py:7\x1b[0m: Output port _Circuit.O not driven
>>     class _Circuit(m.Circuit):"""
        assert logs[0].msg == expected


def test_unconnected_instance(caplog):
    with magma_debug_section():
        Circuit = _make_unconnected_instance()
        logs = caplog.records
        assert len(logs) == 1
        for log in logs:
            assert log.levelname == "ERROR"
        expected = """\x1b[1mtests/test_circuit/test_unconnected.py:31\x1b[0m: Input port buf.I not driven
>>             buf = _Buffer()"""
        assert logs[0].msg == expected


@pytest.mark.parametrize("typ", [m.Clock, m.Reset, m.AsyncReset])
def test_unconnected_autowired(typ, caplog):
    with magma_debug_section():
        Circuit = _make_unconnected_autowired(typ)
        logs = caplog.records
        assert len(logs) == 0
