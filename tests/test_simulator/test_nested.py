import magma as m
from magma import *
from magma.clock import *
from magma.backend.coreir.coreir_backend import CoreIRBackend
from magma.bitutils import *
from coreir.context import *
from magma.simulator.coreir_simulator import CoreIRSimulator
from magma.simulator.python_simulator import PythonSimulator
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
    toNest = Array[inDims[1], Array[inDims[2], Bit]]
    inType = In(Array[inDims[0], toNest])
    if simple:
        outType = Out(Array[inDims[0], toNest])
    else:
        outType = Out(Array[2, Array[2, toNest]])
    args = ['I', inType, 'O', outType] + ClockInterface(False, False)

    class testcircuit(Circuit):
        name = 'test_simulator_nested_simple{}'.format(str(simple))
        io = IO(**dict(zip(args[::2], args[1::2])))
        if simple:
            wire(io.I, io.O)
        else:
            wire(io.I[:2], io.O[0])
            wire(io.I[2:4], io.O[1])

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


def test_simulator_nested_array():
    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Array[3, m.Bits[4]]), O=m.Out(m.Array[2, m.Bits[4]]))
        io += m.ClockIO()
        reg = m.Register(m.Array[2, m.Bits[4]])()
        io.O @= reg(io.I[:2])
        io.I[2].unused()

    sim = PythonSimulator(Main, Main.CLK)
    sim.set_value(Main.I, [3, 4])
    sim.evaluate()
    sim.advance_cycle(1)
    assert sim.get_value(Main.O) == [3, 4]
