from .test_primitives import PRIM_FF
import magma as m
from magma.simulator import PythonSimulator
from magma.scope import *


def test_sim_ff():
    class TestCircuit(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()
        ff = PRIM_FF()
        m.wire(io.I, ff.D)
        m.wire(ff.Q, io.O)

    sim = PythonSimulator(TestCircuit, TestCircuit.CLK)
    sim.evaluate()
    val = sim.get_value(TestCircuit.O)
    assert(val is False)
    sim.advance()
    val = sim.get_value(TestCircuit.O)
    assert(val is False)

    sim.set_value(TestCircuit.I, True)
    sim.evaluate()
    val = sim.get_value(TestCircuit.O)
    assert(val is False)

    sim.advance()
    val = sim.get_value(TestCircuit.O)
    assert(val is True)

    sim.advance()
    val = sim.get_value(TestCircuit.O)
    assert(val is True)
