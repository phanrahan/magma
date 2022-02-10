from magma.simulator.python_simulator import PythonSimulator
import magma as m
from hwtypes import BitVector
import pytest


def test_bit():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        m.wire(io.I, io.O)

    sim = PythonSimulator(Main)
    for value in [False, True]:
        sim.set_value(Main.I, value)
        sim.evaluate()
        assert sim.get_value(Main.O) == value

    try:
        sim.set_value(Main.I, 22)
        assert False, "Should throw type error"
    except TypeError as e:
        assert str(
            e) == "Can only set Bit I with a boolean value or 0 or 1, not 22 (type=<class 'int'>)"


def test_array():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bit]), O=m.Out(m.Array[2, m.Bit]))

        m.wire(io.I, io.O)

    sim = PythonSimulator(Main)
    for value in range(0, 4):
        bv = BitVector[2](value)
        bools = bv.as_bool_list()
        sim.set_value(Main.I, bools)
        sim.evaluate()
        assert sim.get_value(Main.O) == bools

        sim.set_value(Main.I, bv)
        sim.evaluate()
        assert sim.get_value(Main.O) == bools

    try:
        sim.set_value(Main.I, 22)
        assert False, "Should throw type error"
    except TypeError as e:
        assert str(
            e) == "Calling set_value with I of type Array[(2, Out(Bit))] only works with a list of values or a BitVector"


@pytest.mark.parametrize('T', [m.Bits, m.UInt])
def test_uint(T):
    class Main(m.Circuit):
        io = m.IO(I=m.In(T[2]), O=m.Out(T[2]))

        m.wire(io.I, io.O)

    sim = PythonSimulator(Main)
    for value in range(0, 4):
        bv = BitVector[2](value)
        bools = bv.as_bool_list()
        sim.set_value(Main.I, bools)
        sim.evaluate()
        assert sim.get_value(Main.O) == value

        sim.set_value(Main.I, bv)
        sim.evaluate()
        assert sim.get_value(Main.O) == value

        sim.set_value(Main.I, value)
        sim.evaluate()
        assert sim.get_value(Main.O) == value


def test_sint():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.SInt[2]), O=m.Out(m.SInt[2]))

        m.wire(io.I, io.O)

    sim = PythonSimulator(Main)
    for value in range(-2, 2):
        bv = BitVector[2](value)
        bools = bv.as_bool_list()
        sim.set_value(Main.I, bools)
        sim.evaluate()
        assert sim.get_value(Main.O) == value

        sim.set_value(Main.I, bv)
        sim.evaluate()
        assert sim.get_value(Main.O) == value

        sim.set_value(Main.I, value)
        sim.evaluate()
        assert sim.get_value(Main.O) == value
