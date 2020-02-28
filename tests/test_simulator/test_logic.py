from .test_primitives import *
import magma as m
from magma.simulator import PythonSimulator
from magma.scope import *


def test_sim_logic():
    class TestCircuit(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO()
        andy = PRIM_AND()
        ori = PRIM_OR()
        ori2 = PRIM_OR()
        n = PRIM_NOT()

        m.wire(io.I0, andy.I0)
        m.wire(io.I1, andy.I1)
        m.wire(io.I0, ori.I0)
        m.wire(io.I1, n.I)
        m.wire(n.O, ori.I1)

        m.wire(ori.O, ori2.I0)
        m.wire(andy.O, ori2.I1)

        m.wire(ori2.O, io.O)

    sim = PythonSimulator(TestCircuit)
    sim.evaluate()
    v = sim.get_value(TestCircuit.O)
    assert v is True

    sim.set_value(TestCircuit.I1, True)
    sim.evaluate()
    v = sim.get_value(TestCircuit.O)
    assert v is False

    sim.set_value(TestCircuit.I0, True)
    sim.evaluate()
    v = sim.get_value(TestCircuit.O)
    assert v == True


