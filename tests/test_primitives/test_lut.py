import os

import magma as m
from magma.testing import check_files_equal
from magma.primitives import LUT

import fault


def test_basic_lut():
    contents = (
        m.Bits[2](0xDE),
        m.Bits[2](0xAD),
        m.Bits[2](0xBE),
        m.Bits[2](0xEF)
    )

    class test_basic_lut(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), O=m.Out(m.Bits[8]))
        io.O @= LUT(m.Bits[8], 4, contents)()(io.I)

    m.compile("build/test_basic_lut", test_basic_lut)

    assert check_files_equal(__file__, f"build/test_basic_lut.v",
                             f"gold/test_basic_lut.v")

    tester = fault.Tester(test_basic_lut)
    for i in range(0, 4):
        tester.circuit.I = i
        tester.eval()
        tester.circuit.O.expect(int(contents[i]))
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
