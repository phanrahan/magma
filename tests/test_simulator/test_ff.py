from tests.test_simulator.test_primitives import *
from magma.python_simulator import PythonSimulator
from magma.scope import *

def test():
    args = ['I', In(Bit), 'O', Out(Bit)]
    args += ClockInterface(False, False, False)
    
    testcircuit = DefineCircuit('TestCircuit', *args)
    ff = PRIM_FF()
    wire(testcircuit.I, ff.D)
    wire(ff.Q, testcircuit.O)
    EndCircuit()
    
    sim = PythonSimulator(testcircuit)
    sim.evaluate()
    val = sim.get_value(testcircuit.O, Scope())
    assert(val == False)
    sim.step()
    sim.evaluate()
    val = sim.get_value(testcircuit.O, Scope())
    assert(val == False)
    
    sim.set_value(testcircuit.I, Scope(), True)
    sim.evaluate()
    val = sim.get_value(testcircuit.O, Scope())
    assert(val == False)
    
    sim.step()
    sim.evaluate()
    val = sim.get_value(testcircuit.O, Scope())
    assert(val == True)
    
    sim.step()
    sim.evaluate()
    val = sim.get_value(testcircuit.O, Scope())
    assert(val == True)
