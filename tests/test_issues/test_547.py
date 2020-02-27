import pytest

import magma as m


def test_basic():
    class Test(m.Circuit):
        io = m.IO(I=m.In(m.Bits[1]), O=m.Out(m.Bits[1]))

        io.O[0] @= io.I[0]


def test_slice():
    class Test(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[2]))

        io.O[:] @= io.I[:]


def test_compound():
    class Test(m.Circuit):
        io = m.IO(I0=m.In(m.Bits[1]), I1=m.In(m.Bits[1]), O=m.Out(m.Bits[2]))

        io.O[0] @= io.I0
        io.O[1] @= io.I1


def test_recursive():
    class Test(m.Circuit):
        io = m.IO(I=m.In(m.Array[3, m.Bits[2]]), O=m.Out(m.Array[3, m.Bits[2]]))

        io.O[0:1][:][0] @= io.I[0:1][:][0]  # [0]
        io.O[1:2][0][0:1] @= io.I[1:2][0][0:1]  # [1][0]
        io.O[1][1:2] @= io.I[1][1:2]  # [1][1]
        io.O[2][:] @= io.I[2][:]


def test_errors(caplog):
    class Test(m.Circuit):
        io = m.IO(I=m.In(m.Bits[1]), O=m.Out(m.Bits[1]))

        io.O[0] = io.I[0]

    logs = caplog.records
    assert any("May not mutate array" in log.msg and log.levelname == "ERROR"
               for log in logs)


def test_product():
    class HandShake(m.Product):
        ready = m.In(m.Bit)
        valid = m.Out(m.Bit)

    class RTL(m.Circuit):
        io = m.IO(handshake=HandShake)

        cls.handshake.valid @= cls.handshake.ready
