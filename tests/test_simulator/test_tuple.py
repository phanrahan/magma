from magma import *
from magma.clock import *
from magma.backend.coreir_ import CoreIRBackend
from magma.bitutils import *
from coreir.context import *
from magma.simulator.coreir_simulator import CoreIRSimulator
import coreir
from magma.scope import Scope

def test_simulator_tuple():
    width = 8
    testValInt = 80
    c = coreir.Context()
    cirb = CoreIRBackend(c, check_context_is_default=False)
    scope = Scope()
    inDims = [2, width]
    tupleEl = Array[inDims[1], Bit]
    class T(Product):
        sel = tupleEl
        data = tupleEl
    nestedTuples = Array[inDims[0], T]
    tupleValues = {'sel':int2seq(testValInt, width), 'data':int2seq(testValInt+20, width)}
    inType = In(nestedTuples)
    outType = Out(Array[2*inDims[0], tupleEl])
    args = ['I', inType, 'O', outType] + ClockInterface(False, False)

    testcircuit = DefineCircuit('test_simulator_tuple', *args)

    wire(testcircuit.I[0].data, testcircuit.O[0])
    wire(testcircuit.I[0].sel, testcircuit.O[1])
    wire(testcircuit.I[1].data, testcircuit.O[2])
    wire(testcircuit.I[1].sel, testcircuit.O[3])

    EndCircuit()

    sim = CoreIRSimulator(testcircuit, testcircuit.CLK, context=cirb.context,
                          namespaces=["aetherlinglib", "commonlib", "mantle", "coreir", "global"])

    sim.set_value(testcircuit.I, [tupleValues, tupleValues], scope)
    getArrayInTuple = sim.get_value(testcircuit.I[0].data, scope)
    getTuples = sim.get_value(testcircuit.I, scope)
    assert getArrayInTuple == tupleValues['data']
    assert getTuples[0] == tupleValues
    assert getTuples[1] == tupleValues

