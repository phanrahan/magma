from .test_primitives import *
from magma.simulator import PythonSimulator
from magma.scope import *

def test():
    args = ['I', In(Bit), 'O', Out(Bit)]
    args += ClockInterface(False, False, False)
    
    testcircuit = DefineCircuit('TestCircuit', *args)
    ff = PRIM_FF()
    wire(testcircuit.I, ff.D)
    wire(ff.Q, testcircuit.O)
    EndCircuit()
    
    sim = PythonSimulator(testcircuit, testcircuit.CLK)
    sim.evaluate()
    val = sim.get_value(testcircuit.O)
    assert(val == False)
    sim.advance()
    val = sim.get_value(testcircuit.O)
    assert(val == False)
    
    sim.set_value(testcircuit.I, True)
    sim.evaluate()
    val = sim.get_value(testcircuit.O)
    assert(val == False)
    
    sim.advance()
    val = sim.get_value(testcircuit.O)
    assert(val == True)
    
    sim.advance()
    val = sim.get_value(testcircuit.O)
    assert(val == True)
