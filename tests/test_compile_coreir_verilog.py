import sys
import os
from magma.testing.utils import check_files_equal
import magma as m
m.set_mantle_target("coreir")


def test(caplog):
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))

    main = m.DefineCircuit("main", "I", m.In(m.Bits(2)), "O", m.Out(m.Bit))

    and2 = And2()

    m.wire(main.I[0], and2.I0)
    m.wire(main.I[1], and2.I1)
    m.wire(and2.O, main.O)

    m.EndCircuit()
    sys.modules['mantle'] = True  # Mock mantle import
    m.compile("build/test_coreir_compile_verilog", main)
    del sys.modules['mantle']
    assert check_files_equal(__file__, "build/test_coreir_compile_verilog.v",
                             "gold/test_coreir_compile_verilog.v")
    assert caplog.records[0].msg == "`m.compile` called with `output == verilog` and `m.mantle_target == \"coreir\"` and mantle has been imported, When generating verilog from circuits from the \"coreir\" mantle target, you should set `output=\"coreir-verilog\"`."
