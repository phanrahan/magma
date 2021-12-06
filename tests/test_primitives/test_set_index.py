import os

from hwtypes import BitVector, Bit
import fault

import magma as m


def test_set_index():
    class test_set_index(m.Circuit):
        io = m.IO(I=m.In(m.Bits[4]),
                  val=m.In(m.Bit),
                  idx=m.In(m.UInt[2]),
                  O=m.Out(m.Bits[4]))
        io.O @= m.set_index(io.I, io.val, io.idx)

    tester = fault.Tester(test_set_index)
    for i in range(5):
        tester.circuit.I = I = BitVector.random(4)
        tester.circuit.val = val = Bit.random()
        tester.circuit.idx = idx = BitVector.random(2)
        tester.eval()
        I[int(idx)] = val
        tester.circuit.O.expect(I)

    m.compile("build/test_set_index", test_set_index)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"),
                           flags=["-Wno-unused"])


def test_set_index_array():
    class test_set_index_array(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bits[4]]),
                  val=m.In(m.Bits[4]),
                  idx=m.In(m.UInt[1]),
                  O=m.Out(m.Array[2, m.Bits[4]]))
        io.O @= m.set_index(io.I, io.val, io.idx)

    tester = fault.Tester(test_set_index_array)
    for i in range(5):
        tester.circuit.I = I = [BitVector.random(4), BitVector.random(4)]
        tester.circuit.val = val = BitVector.random(4)
        tester.circuit.idx = idx = BitVector.random(1)
        tester.eval()
        I[int(idx)] = val
        tester.circuit.O.expect(I)

    m.compile("build/test_set_index_array", test_set_index_array)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"),
                           flags=["-Wno-unused"])
