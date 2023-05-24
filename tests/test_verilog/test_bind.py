import os
import magma as m
import magma.testing
from rtl import RTL
import rtl_monitor
from subprocess import run


def test_bind():
    RTL4 = RTL(4)

    m.compile("build/bind_test", RTL4, inline=True, user_namespace="foo",
              verilog_prefix="bar_")
    assert m.testing.check_files_equal(__file__,
                                       f"build/bind_test.v",
                                       f"gold/bind_test.v")
    assert m.testing.check_files_equal(__file__,
                                       f"build/RTLMonitor.sv",
                                       f"gold/RTLMonitor.sv")

    listings_file = "tests/test_verilog/build/bind_test_bind_files.list"
    with open(listings_file, "r") as f:
        assert f.read() == """\
RTLMonitor.sv\
"""


def test_bind_multi_unique_name():
    class Main(m.Circuit):
        _ignore_undriven_ = True
        io = m.ClockIO()
        RTL4 = RTL(4)()
        RTL5 = RTL(5)()

    m.compile("build/bind_uniq_test", Main, inline=True, drive_undriven=True,
              terminate_unused=True, user_namespace="foo",
              verilog_prefix="bar_", verilog_prefix_extern=True)
    assert m.testing.check_files_equal(__file__,
                                       f"build/bind_uniq_test.v",
                                       f"gold/bind_uniq_test.v")

    assert m.testing.check_files_equal(__file__,
                                       f"build/RTLMonitor.sv",
                                       f"gold/RTLMonitor.sv")

    assert m.testing.check_files_equal(__file__,
                                       f"build/RTLMonitor_unq1.sv",
                                       f"gold/RTLMonitor_unq1.sv")

    listings_file = "tests/test_verilog/build/bind_uniq_test_bind_files.list"
    with open(listings_file, "r") as f:
        assert f.read() == """\
RTLMonitor.sv
RTLMonitor_unq1.sv\
"""
