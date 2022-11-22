import os

import fault
import magma as m
from magma.backend.mlir.mlir_to_verilog import circt_opt_binary_exists
import magma.testing


def test_display(capsys):

    class TestDisplay(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
        ff = m.Register(m.Bit, has_enable=True)(name="ff")
        io.O @= ff(io.I)
        m.display(
            "%0t: ff.O=%d, ff.I=%d", m.time(), ff.O, io.I
        ).when(m.posedge(io.CLK)).if_(io.CE)

    if not circt_opt_binary_exists():
        m.compile("build/TestDisplay", TestDisplay, output="mlir")
        assert m.testing.check_files_equal(
            __file__,
            f"build/TestDisplay.mlir",
            f"gold/TestDisplay.mlir"
        )
        return
    m.compile("build/TestDisplay", TestDisplay, output="mlir-verilog")
    assert not os.system(
        "cd tests/test_verilog/build "
        "&& verilator --lint-only TestDisplay.v --top-module TestDisplay"
    )
    assert m.testing.check_files_equal(
        __file__,
        f"build/TestDisplay.v",
        f"gold/TestDisplay.v"
    )

    tester = fault.SynchronousTester(TestDisplay, TestDisplay.CLK)
    tester.poke(TestDisplay.CE, 1)
    tester.poke(TestDisplay.I, 1)
    tester.expect(TestDisplay.O, 0)
    tester.advance_cycle()
    tester.poke(TestDisplay.I, 0)
    tester.expect(TestDisplay.O, 1)
    tester.advance_cycle()
    tester.expect(TestDisplay.O, 0)
    tester.poke(TestDisplay.CE, 0)
    tester.poke(TestDisplay.I, 1)
    tester.advance_cycle()
    tester.expect(TestDisplay.O, 0)
    tester.poke(TestDisplay.I, 1)
    tester.advance_cycle()
    tester.expect(TestDisplay.O, 0)
    tester.poke(TestDisplay.CE, 1)
    tester.advance_cycle()
    tester.expect(TestDisplay.O, 1)
    tester.advance_cycle()

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(
        target="verilator", directory=directory,
        flags=['-Wno-unused'], skip_compile=True,
        disp_type="realtime"
    )
    out, err = capsys.readouterr()
    assert f"""
0: ff.O=0, ff.I=1
10: ff.O=1, ff.I=0
40: ff.O=0, ff.I=1
50: ff.O=1, ff.I=1
""" in out, out


def test_fdisplay():

    class TestFDisplay(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
        ff = m.Register(m.Bit, has_enable=True)(name="ff")
        io.O @= ff(io.I)
        with m.File("test_fdisplay.log", "a") as log_file:
            m.display(
                "ff.O=%d, ff.I=%d", ff.O, io.I, file=log_file
            ).when(m.posedge(io.CLK)).if_(io.CE)

    if not circt_opt_binary_exists():
        m.compile("build/TestFDisplay", TestFDisplay, output="mlir")
        assert m.testing.check_files_equal(
            __file__,
            f"build/TestFDisplay.mlir",
            f"gold/TestFDisplay.mlir"
        )
        return
    m.compile("build/TestFDisplay", TestFDisplay, output="mlir-verilog")
    assert not os.system(
        "cd tests/test_verilog/build "
        "&& verilator --lint-only TestFDisplay.v --top-module TestFDisplay"
    )
    assert m.testing.check_files_equal(
        __file__,
        f"build/TestFDisplay.v",
        f"gold/TestFDisplay.v"
    )

    tester = fault.SynchronousTester(TestFDisplay, TestFDisplay.CLK)
    tester.poke(TestFDisplay.CE, 1)
    tester.poke(TestFDisplay.I, 1)
    tester.expect(TestFDisplay.O, 0)
    tester.advance_cycle()
    tester.poke(TestFDisplay.I, 0)
    tester.expect(TestFDisplay.O, 1)
    tester.advance_cycle()
    tester.expect(TestFDisplay.O, 0)
    tester.poke(TestFDisplay.CE, 0)
    tester.poke(TestFDisplay.I, 1)
    tester.advance_cycle()
    tester.expect(TestFDisplay.O, 0)
    tester.poke(TestFDisplay.I, 1)
    tester.advance_cycle()
    tester.expect(TestFDisplay.O, 0)
    tester.poke(TestFDisplay.CE, 1)
    tester.advance_cycle()
    tester.expect(TestFDisplay.O, 1)
    tester.advance_cycle()

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(
        target="verilator", directory=directory,
        flags=['-Wno-unused'], skip_compile=True
    )
    with open(os.path.join(directory, "test_fdisplay.log"), "r") as f:
        assert f"""\
ff.O=0, ff.I=1
ff.O=1, ff.I=0
ff.O=0, ff.I=1
ff.O=1, ff.I=1
""" in f.read()
