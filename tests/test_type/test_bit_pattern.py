import os

import fault
import magma as m


def test_bit_pattern_simple():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bit))
        bit_pat = m.BitPattern("b??1??01?")
        io.O @= bit_pat == io.I

    m.compile("build/Foo", Foo)

    tester = fault.Tester(Foo)
    tester.circuit.I = 0b00100010
    tester.eval()
    tester.circuit.O.expect(1)
    tester.circuit.I = 0b10100010
    tester.eval()
    tester.circuit.O.expect(1)
    tester.circuit.I = 0b10100000
    tester.eval()
    tester.circuit.O.expect(0)
    tester.compile_and_run("verilator",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
