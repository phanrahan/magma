import magma as m
from magma.testing import check_files_equal
from hwtypes import BitVector


def test_slice_fixed_range():
    class TestSlice(m.Circuit):
        io = m.IO(
            I=m.In(m.Bits[10]),
            x=m.In(m.Bits[2]),
            O=m.Out(m.Bits[6])
        )

        io.O @= m.slice(io.I, start=io.x, width=6)

    m.compile("build/TestSlice", TestSlice)
    assert check_files_equal(__file__,
                             "build/TestSlice.v",
                             "gold/TestSlice.v")

    try:
        import fault
        tester = fault.Tester(TestSlice)
        I = BitVector[10](0x2DE)
        tester.circuit.I = I
        for x in range(0, 4):
            tester.circuit.x = x
            tester.eval()
            tester.circuit.O.expect(I[x:x + 6])
        import os
        build_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "build"
        )
        tester.compile_and_run("verilator", skip_compile=True, directory=build_dir,
                               flags=["-Wno-unused"])
    except ImportError:
        pass
