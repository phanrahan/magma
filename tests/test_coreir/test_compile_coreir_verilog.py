import sys
import os
from magma.testing.utils import check_files_equal
import magma as m
m.set_mantle_target("coreir")
import pytest


def test_compile(caplog):
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))
    # Make it a mock mantle module
    class MockMantle:
        pass
    MockMantle.__name__ = "mantle.coreir.arith"
    And2.debug_info = m.debug.debug_info(And2.debug_info.filename,
                                         And2.debug_info.lineno,
                                         MockMantle)

    main = m.DefineCircuit("main", "I", m.In(m.Bits(2)), "O", m.Out(m.Bit))

    and2 = And2()

    m.wire(main.I[0], and2.I0)
    m.wire(main.I[1], and2.I1)
    m.wire(and2.O, main.O)

    m.EndCircuit()
    m.compile("build/test_compile_coreir_verilog", main)
    assert check_files_equal(__file__, "build/test_compile_coreir_verilog.v",
                             "gold/test_compile_coreir_verilog.v")
    assert caplog.records[0].msg == "`m.compile` called with `output == verilog` and `m.mantle_target == \"coreir\"` and mantle has been imported, When generating verilog from circuits from the \"coreir\" mantle target, you should set `output=\"coreir-verilog\"`. Doing this automatically."
