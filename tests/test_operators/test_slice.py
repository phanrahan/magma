import fault
import os
import magma as m
from magma.testing import check_files_equal
from hwtypes import BitVector


def test_get_slice_fixed_range():
    class TestSlice(m.Circuit):
        io = m.IO(
            I=m.In(m.Bits[10]),
            x=m.In(m.Bits[2]),
            O=m.Out(m.Bits[6])
        )

        io.O @= m.get_slice(io.I, start=io.x, width=6)

    m.compile("build/TestSlice", TestSlice)
    assert check_files_equal(__file__,
                             "build/TestSlice.v",
                             "gold/TestSlice.v")

    tester = fault.Tester(TestSlice)
    I = BitVector[10](0x2DE)
    tester.circuit.I = I
    for x in range(0, 4):
        tester.circuit.x = x
        tester.eval()
        tester.circuit.O.expect(I[x:x + 6])
    build_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "build"
    )
    tester.compile_and_run("verilator", skip_compile=True, directory=build_dir,
                           flags=["-Wno-unused"])


def test_set_slice_fixed_range():
    class TestSetSlice(m.Circuit):
        io = m.IO(
            I=m.In(m.Bits[6]),
            x=m.In(m.UInt[2]),
            O=m.Out(m.Bits[12])
        )

        # default value
        O = m.Bits[12](0xFFF)
        io.O @= m.set_slice(O, io.I, start=io.x, width=6)

    m.compile("build/TestSetSlice", TestSetSlice, inline=True)
    assert check_files_equal(__file__, "build/TestSetSlice.v",
                             "gold/TestSetSlice.v")

    tester = fault.Tester(TestSetSlice)
    I = BitVector[6](0)
    tester.circuit.I = I
    for x in range(0, 4):
        tester.circuit.x = x
        tester.eval()
        tester.circuit.O[x:x + 6].expect(I)
        if x > 0:
            tester.circuit.O[:x].expect(0xFFF)
        if x < 4:
            tester.circuit.O[x + 6:].expect(0xFFF)
    build_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "build"
    )
    tester.compile_and_run("verilator", skip_compile=True, directory=build_dir,
                           flags=["-Wno-unused"])
