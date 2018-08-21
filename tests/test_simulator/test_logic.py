from .test_primitives import *
from magma.simulator import PythonSimulator
from magma.scope import *

def test():
    args = ['I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit)] + ClockInterface(False, False, False)

    testcircuit = DefineCircuit('TestCircuit', *args)
    andy = PRIM_AND()
    ori = PRIM_OR()
    ori2 = PRIM_OR()
    n = PRIM_NOT()

    wire(testcircuit.I0, andy.I0)
    wire(testcircuit.I1, andy.I1)
    wire(testcircuit.I0, ori.I0)
    wire(testcircuit.I1, n.I)
    wire(n.O, ori.I1)

    wire(ori.O, ori2.I0)
    wire(andy.O, ori2.I1)

    wire(ori2.O, testcircuit.O)
    EndCircuit()

    sim = PythonSimulator(testcircuit)
    sim.evaluate()
    v = sim.get_value(testcircuit.O)
    assert v == True

    sim.set_value(testcircuit.I1, True)
    sim.evaluate()
    v = sim.get_value(testcircuit.O)
    assert v == False

    sim.set_value(testcircuit.I0, True)
    sim.evaluate()
    v = sim.get_value(testcircuit.O)
    assert v == True


