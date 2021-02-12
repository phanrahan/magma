from magma import *
from magma.clock import *
from magma.backend.coreir.coreir_backend import CoreIRBackend
from magma.bitutils import *
from coreir.context import *
from magma.simulator.coreir_simulator import CoreIRSimulator
import coreir
from magma.scope import Scope

def test_simulator_tuple():
    width = 8
    testValInt = 80
    c = coreir.Context()
    cirb = CoreIRBackend(c)
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

    class testcircuit(Circuit):
        name = "test_simulator_tuple"
        io = IO(**dict(zip(args[::2], args[1::2])))
        wire(io.I[0].data, io.O[0])
        wire(io.I[0].sel, io.O[1])
        wire(io.I[1].data, io.O[2])
        wire(io.I[1].sel, io.O[3])


    sim = CoreIRSimulator(testcircuit, testcircuit.CLK, context=cirb.context,
                          namespaces=["aetherlinglib", "commonlib", "mantle", "coreir", "global"])

    sim.set_value(testcircuit.I, [tupleValues, tupleValues], scope)
    getArrayInTuple = sim.get_value(testcircuit.I[0].data, scope)
    getTuples = sim.get_value(testcircuit.I, scope)
    assert getArrayInTuple == tupleValues['data']
    assert getTuples[0] == tupleValues
    assert getTuples[1] == tupleValues

