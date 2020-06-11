import os
import magma as m
import magma.testing
from rtl import RTL
import rtl_monitor
from subprocess import run


def test_bind():
    RTL4 = RTL.generate(4)

    m.compile("build/bind_test", RTL4, inline=True)
    assert m.testing.check_files_equal(__file__,
                                       f"build/bind_test.v",
                                       f"gold/bind_test.v")
    assert m.testing.check_files_equal(__file__,
                                       f"build/RTLMonitor.sv",
                                       f"gold/RTLMonitor.sv")

    result = run('verilator --version', shell=True, capture_output=True)
    version = float(result.stdout.split()[1])
    if version >= 4.016:
        assert not os.system('cd tests/test_verilog/build && '
                             'verilator --lint-only bind_test.v RTLMonitor.sv '
                             '--top-module RTL -Wno-MODDUP')


def test_bind_multi_unique_name():
    class Main(m.Circuit):
        _ignore_undriven_ = True
        io = m.ClockIO()
        RTL4 = RTL.generate(4)()
        RTL5 = RTL.generate(5)()

    m.compile("build/bind_uniq_test", Main, inline=True, drive_undriven=True,
              terminate_unused=True)
    assert m.testing.check_files_equal(__file__,
                                       f"build/bind_uniq_test.v",
                                       f"gold/bind_uniq_test.v")

    assert m.testing.check_files_equal(__file__,
                                       f"build/RTLMonitor.sv",
                                       f"gold/RTLMonitor.sv")

    assert m.testing.check_files_equal(__file__,
                                       f"build/RTLMonitor_unq1.sv",
                                       f"gold/RTLMonitor_unq1.sv")

    result = run('verilator --version', shell=True, capture_output=True)
    version = float(result.stdout.split()[1])
    if version >= 4.016:
        assert not os.system('cd tests/test_verilog/build && '
                             'verilator --lint-only bind_uniq_test.v '
                             'RTLMonitor.sv RTLMonitor_unq1.sv -Wno-MODDUP')
        # TODO: For now, we ignore duplicate modules since each monitor will
        # regenerate coreir primitives.  # since these have the same definition
        # it's okay, but in general this is a bad flag to have on because if
        # you do have duplicate modules with different definitions, you'd want
        # to catch that
        # When we merge the inline verilog module branch, this will be resolved since
        # bind modules can be represented explicitly in the graph and compiled
        # by coreir, so only one definition per primitive will be emitted
