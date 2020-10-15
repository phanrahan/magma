import os

from hwtypes import BitVector, Bit
import fault

import magma as m


def test_set_bit():
    class test_set_bit(m.Circuit):
        io = m.IO(I=m.In(m.Bits[4]),
                  val=m.In(m.Bit),
                  idx=m.In(m.Bits[2]),
                  O=m.Out(m.Bits[4]))
        io.O @= m.set_bit(io.I, io.val, io.idx)

    tester = fault.Tester(test_set_bit)
    for i in range(5):
        tester.circuit.I = I = BitVector.random(4)
        tester.circuit.val = val = Bit.random()
        tester.circuit.idx = idx = BitVector.random(2)
        tester.eval()
        I[int(idx)] = val
        tester.circuit.O.expect(I)

    m.compile("build/test_set_bit", test_set_bit)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
