import os
import magma as m
from magma.testing import check_files_equal


def test_simple_def():
    os.environ["MAGMA_CODEGEN_DEBUG_INFO"] = "1"
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))

    main = m.DefineCircuit("main", "I", m.In(m.Bits(2)), "O", m.Out(m.Bit))

    and2 = And2()

    m.wire(main.I[0], and2.I0)
    m.wire(main.I[1], and2.I1)
    m.wire(and2.O, main.O)

    m.EndCircuit()

    m.compile("build/test_simple_def", main)
    del os.environ["MAGMA_CODEGEN_DEBUG_INFO"]
    assert check_files_equal(__file__, f"build/test_simple_def.v",
                             f"gold/test_simple_def.v")
