from magma import *
from magma.clock import *
from magma.backend.coreir_ import CoreIRBackend
from magma.bitutils import *
from coreir.context import *
from magma.simulator.coreir_simulator import CoreIRSimulator
import coreir
from magma.scope import Scope

def simulator_nested(simple):
    width = 8
    testValInt = 80
    testValBits = int2seq(testValInt)
    c = coreir.Context()
    cirb = CoreIRBackend(c)
    scope = Scope()
    inDims = [4, 3, width]
    toNest = Array(inDims[1], Array(inDims[2], Bit))
    inType = In(Array(inDims[0], toNest))
    if simple:
        outType = Out(Array(inDims[0], toNest))
    else:
        outType = Out(Array(2, Array(2, toNest)))
    args = ['I', inType, 'O', outType] + ClockInterface(False, False)

    testcircuit = DefineCircuit('test_simulator_nested_simple{}'.format(str(simple)), *args)

    if simple:
        wire(testcircuit.I, testcircuit.O)
    else:
        wire(testcircuit.I[:2], testcircuit.O[0])
        wire(testcircuit.I[2:4], testcircuit.O[1])

    EndCircuit()


    sim = CoreIRSimulator(testcircuit, testcircuit.CLK, context=cirb.context,
                          namespaces=["aetherlinglib", "commonlib", "mantle", "coreir", "global"])

    for i in range(inDims[0]):
        for j in range(inDims[1]):
           get = sim.get_value(testcircuit.I[i][j], scope)
           assert(len(get) == width)
           sim.set_value(testcircuit.I[i][j], int2seq((((i*inDims[1])+j)*inDims[2]), width), scope)

    sim.evaluate()
    sim.get_value(testcircuit.I, scope)
    sim.get_value(testcircuit.O, scope)

def test_simulator_nested_simple():
    simulator_nested(True)

def test_simulator_nested_complex():
    simulator_nested(False)
