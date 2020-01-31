import pytest

import magma as m

def test_basic():
    class Test(m.Circuit):
        IO = ["I", m.In(m.Bits[1]), "O", m.Out(m.Bits[1])]

        @classmethod
        def definition(io):
            io.O[0] @= io.I[0]

def test_slice():
    class Test(m.Circuit):
        IO = ["I", m.In(m.Bits[2]), "O", m.Out(m.Bits[2])]

        @classmethod
        def definition(io):
            io.O[:] @= io.I[:]

def test_compound():
    class Test(m.Circuit):
        IO = ["I0", m.In(m.Bits[1]), "I1", m.In(m.Bits[1]), "O", m.Out(m.Bits[2])]

        @classmethod
        def definition(io):
            io.O[0] @= io.I0
            io.O[1] @= io.I1

def test_recursive():
    class Test(m.Circuit):
        IO = ["I", m.In(m.Array[3, m.Bits[2]]), "O", m.Out(m.Array[3, m.Bits[2]])]

        @classmethod
        def definition(io):
            io.O[0:1][:][0] @= io.I[0:1][:][0] # [0]
            io.O[1:2][0][0:1] @= io.I[1:2][0][0:1] # [1][0]
            io.O[1][1:2] @= io.I[1][1:2] # [1][1]
            io.O[2][:] @= io.I[2][:]

def test_errors(caplog):
    class Test(m.Circuit):
        IO = ["I", m.In(m.Bits[1]), "O", m.Out(m.Bits[1])]

        @classmethod
        def definition(io):
            io.O[0] = io.I[0]

    assert caplog.records[0].levelname == "ERROR"
