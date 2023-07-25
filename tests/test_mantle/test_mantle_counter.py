import tempfile

import magma as m
from magma.mantle import Counter
import fault


def test_counter_to():
    tester = fault.SynchronousTester(Counter(6))
    for j in range(2):
        for i in range(6):
            tester.circuit.O.expect(i)
            tester.advance_cycle()
    with tempfile.TemporaryDirectory() as tempdir:
        tester.compile_and_run("verilator", magma_output="mlir-verilog",
                               magma_opts={"check_circt_opt_version": False},
                               directory=tempdir)


def test_counter_to_cout():
    tester = fault.SynchronousTester(Counter(6, has_cout=True))
    for j in range(2):
        for i in range(6):
            tester.circuit.O.expect(i)
            tester.circuit.COUT.expect(i == 5)
            tester.advance_cycle()
    with tempfile.TemporaryDirectory() as tempdir:
        tester.compile_and_run("verilator", magma_output="mlir-verilog",
                               magma_opts={"check_circt_opt_version": False},
                               directory=tempdir)


def test_counter_to_enable():
    tester = fault.SynchronousTester(Counter(6, has_enable=True))
    for i in range(3):
        tester.circuit.O.expect(0)
        tester.advance_cycle()
    tester.circuit.CE = 1
    for i in range(3):
        tester.circuit.O.expect(i)
        tester.advance_cycle()
    with tempfile.TemporaryDirectory() as tempdir:
        tester.compile_and_run("verilator", magma_output="mlir-verilog",
                               magma_opts={"check_circt_opt_version": False},
                               directory=tempdir)


def test_counter_to_reset():
    tester = fault.SynchronousTester(Counter(6, reset_type=m.Reset))
    tester.circuit.RESET = 0
    for i in range(3):
        tester.circuit.O.expect(i)
        tester.advance_cycle()
    tester.circuit.RESET = 1
    tester.advance_cycle()
    tester.circuit.RESET = 0
    for i in range(3):
        tester.circuit.O.expect(i)
        tester.advance_cycle()
    with tempfile.TemporaryDirectory() as tempdir:
        tester.compile_and_run("verilator", magma_output="mlir-verilog",
                               magma_opts={"check_circt_opt_version": False},
                               directory=tempdir)
