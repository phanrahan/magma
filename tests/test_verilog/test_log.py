import os
import pytest
import shutil

import fault
import magma as m
from magma.backend.mlir.mlir_to_verilog import circt_opt_binary_exists
import magma.testing


def test_log(capsys):

    class TestLog(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
        ff = m.Register(m.Bit, has_enable=True)(name="ff")
        io.O @= ff(io.I)
        m.log.debug("ff.O=%d, ff.I=%d", ff.O, ff.I.value()).when(
            m.posedge(io.CLK)
        ).if_(io.CE)
        m.log.info("ff.O=%d, ff.I=%d", ff.O, ff.I.value()).when(
            m.posedge(io.CLK)
        ).if_(io.CE)
        m.log.warning("ff.O=%d, ff.I=%d", ff.O, ff.I.value()).when(
            m.posedge(io.CLK)
        ).if_(io.CE)
        m.log.error("ff.O=%d, ff.I=%d", ff.O, ff.I.value()).when(
            m.posedge(io.CLK)
        ).if_(io.CE)

    if not circt_opt_binary_exists():
        m.compile("build/TestLog", TestLog, output="mlir")
        assert m.testing.check_files_equal(
            __file__,
            f"build/TestLog.mlir",
            f"gold/TestLog.mlir"
        )
        return
    m.compile("build/TestLog", TestLog, output="mlir-verilog")
    assert m.testing.check_files_equal(
        __file__,
        f"build/TestLog.v",
        f"gold/TestLog.v"
    )
    assert not os.system(
        "cd tests/test_verilog/build "
        "&& verilator --lint-only TestLog.v --top-module TestLog"
    )

    tester = fault.SynchronousTester(TestLog, TestLog.CLK)
    tester.poke(TestLog.CE, 1)
    tester.poke(TestLog.I, 1)
    tester.expect(TestLog.O, 0)
    tester.advance_cycle()
    tester.poke(TestLog.I, 0)
    tester.expect(TestLog.O, 1)
    tester.advance_cycle()
    tester.expect(TestLog.O, 0)
    tester.poke(TestLog.CE, 0)
    tester.poke(TestLog.I, 1)
    tester.advance_cycle()
    tester.expect(TestLog.O, 0)
    tester.poke(TestLog.I, 1)
    tester.advance_cycle()
    tester.expect(TestLog.O, 0)
    tester.poke(TestLog.CE, 1)
    tester.advance_cycle()
    tester.expect(TestLog.O, 1)
    tester.advance_cycle()

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(
        target="verilator", directory=directory,
        flags=['-Wno-unused'], skip_compile=True,
        disp_type="realtime"
    )
    out, err = capsys.readouterr()

    # Expect no "DEBUG".
    assert f"""
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[INFO] ff.O=1, ff.I=0
[WARNING] ff.O=1, ff.I=0
[ERROR] ff.O=1, ff.I=0
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[INFO] ff.O=1, ff.I=1
[WARNING] ff.O=1, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in out, out

    # Force recompile for new define.
    shutil.rmtree(os.path.join(directory, "obj_dir"))
    tester.compile_and_run(
        target="verilator", directory=directory,
        flags=['-Wno-unused', '+define+MAGMA_LOG_LEVEL=2'], skip_compile=True,
        disp_type="realtime"
    )
    out, err = capsys.readouterr()

    # Expect no "INFO".
    assert f"""
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[WARNING] ff.O=1, ff.I=0
[ERROR] ff.O=1, ff.I=0
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[WARNING] ff.O=1, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in out, out

    # Force recompile for new define.
    shutil.rmtree(os.path.join(directory, "obj_dir"))
    tester.compile_and_run(
        target="verilator", directory=directory,
        flags=['-Wno-unused', '+define+MAGMA_LOG_LEVEL=3'], skip_compile=True,
        disp_type="realtime"
    )
    out, err = capsys.readouterr()
    # Expect only "ERROR".
    assert f"""
[ERROR] ff.O=0, ff.I=1
[ERROR] ff.O=1, ff.I=0
[ERROR] ff.O=0, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in out, out

    # Force recompile for new define.
    shutil.rmtree(os.path.join(directory, "obj_dir"))
    tester.compile_and_run(
        target="verilator", directory=directory,
        flags=['-Wno-unused', '+define+MAGMA_LOG_LEVEL=0'], skip_compile=True,
        disp_type="realtime"
    )
    out, err = capsys.readouterr()
    # Expect all log levels.
    assert f"""
[DEBUG] ff.O=0, ff.I=1
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[DEBUG] ff.O=1, ff.I=0
[INFO] ff.O=1, ff.I=0
[WARNING] ff.O=1, ff.I=0
[ERROR] ff.O=1, ff.I=0
[DEBUG] ff.O=0, ff.I=1
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[DEBUG] ff.O=1, ff.I=1
[INFO] ff.O=1, ff.I=1
[WARNING] ff.O=1, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in out, out


def test_flog():

    class TestFLog(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
        ff = m.Register(m.Bit, has_enable=True)(name="ff")
        io.O @= ff(io.I)
        with m.File("test_flog.log", "a") as log_file:
            m.log.debug("ff.O=%d, ff.I=%d", ff.O, ff.I.value(), file=log_file)\
                .when(m.posedge(io.CLK))\
                .if_(io.CE)
            m.log.info("ff.O=%d, ff.I=%d", ff.O, ff.I.value(), file=log_file)\
                .when(m.posedge(io.CLK))\
                .if_(io.CE)
            m.log.warning("ff.O=%d, ff.I=%d", ff.O, ff.I.value(), file=log_file)\
                .when(m.posedge(io.CLK))\
                .if_(io.CE)
            m.log.error("ff.O=%d, ff.I=%d", ff.O, ff.I.value(), file=log_file)\
                .when(m.posedge(io.CLK))\
                .if_(io.CE)

    if not circt_opt_binary_exists():
        m.compile("build/TestFLog", TestFLog, output="mlir")
        assert m.testing.check_files_equal(
            __file__,
            f"build/TestFLog.mlir",
            f"gold/TestFLog.mlir"
        )
        return
    m.compile("build/TestFLog", TestFLog, output="mlir-verilog")
    assert m.testing.check_files_equal(
        __file__,
        f"build/TestFLog.v",
        f"gold/TestFLog.v"
    )
    assert not os.system(
        "cd tests/test_verilog/build "
        "&& verilator --lint-only TestFLog.v --top-module TestFLog"
    )

    tester = fault.SynchronousTester(TestFLog, TestFLog.CLK)
    tester.poke(TestFLog.CE, 1)
    tester.poke(TestFLog.I, 1)
    tester.expect(TestFLog.O, 0)
    tester.advance_cycle()
    tester.poke(TestFLog.I, 0)
    tester.expect(TestFLog.O, 1)
    tester.advance_cycle()
    tester.expect(TestFLog.O, 0)
    tester.poke(TestFLog.CE, 0)
    tester.poke(TestFLog.I, 1)
    tester.advance_cycle()
    tester.expect(TestFLog.O, 0)
    tester.poke(TestFLog.I, 1)
    tester.advance_cycle()
    tester.expect(TestFLog.O, 0)
    tester.poke(TestFLog.CE, 1)
    tester.advance_cycle()
    tester.expect(TestFLog.O, 1)
    tester.advance_cycle()

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(
        target="verilator", directory=directory,
        flags=['-Wno-unused'], skip_compile=True,
        disp_type="realtime"
    )
    # Expect no "DEBUG".
    with open(os.path.join(directory, "test_flog.log"), "r") as f:
        assert f"""\
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[INFO] ff.O=1, ff.I=0
[WARNING] ff.O=1, ff.I=0
[ERROR] ff.O=1, ff.I=0
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[INFO] ff.O=1, ff.I=1
[WARNING] ff.O=1, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in f.read()
