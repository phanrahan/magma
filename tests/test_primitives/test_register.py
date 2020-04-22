import os

import magma as m
from magma.testing import check_files_equal
from magma.primitives import Register

import fault


def test_basic_reg():
    class test_basic_reg(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8])) + m.ClockIO(has_reset=True)
        io.O @= Register(m.Bits[8], m.Bits[8](0xDE), reset_type=m.Reset)()(io.I)

    m.compile("build/test_basic_reg", test_basic_reg)

    assert check_files_equal(__file__, f"build/test_basic_reg.v",
                             f"gold/test_basic_reg.v")

    tester = fault.SynchronousTester(test_basic_reg, test_basic_reg.CLK)
    tester.circuit.I = 0
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    # Reset val
    tester.circuit.O.expect(0xDE)
    tester.advance_cycle()
    tester.circuit.O.expect(0)
    tester.circuit.I = 1
    tester.advance_cycle()
    tester.circuit.O.expect(1)
    tester.circuit.I = 2
    tester.advance_cycle()
    tester.circuit.O.expect(2)
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    tester.circuit.I = 3
    tester.circuit.O.expect(0xDE)
    tester.advance_cycle()
    tester.circuit.O.expect(3)
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
