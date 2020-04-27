import os

import magma as m
from magma.testing import check_files_equal

import fault


def test_add_1_bit():
    class test_add_1_bit(m.Circuit):
        io = m.IO(I=m.In(m.Bits[5]), C=m.In(m.Bit), O=m.Out(m.Bits[5]))

        io.O @= m.uint(io.C, 5) + m.uint(io.I)

    m.compile('build/test_add_1_bit', test_add_1_bit, inline=True)

    assert check_files_equal(__file__, f"build/test_add_1_bit.v",
                             f"gold/test_add_1_bit.v")

    tester = fault.Tester(test_add_1_bit)
    tester.circuit.I = 2
    tester.circuit.C = 1
    tester.eval()
    tester.circuit.O.expect(3)
    tester.circuit.I = 4
    tester.circuit.C = 0
    tester.eval()
    tester.circuit.O.expect(4)

    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
