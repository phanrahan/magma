import magma as m
from magma.testing import check_files_equal


def test_if_statement_basic():
    class TestIfStatementBasic(m.Circuit):
        IO = ["I", m.In(m.Bits(2)), "S", m.In(m.Bit), "O", m.Out(m.Bit)]

        @m.circuit_def
        def definition(io):
            if io.S:
                m.wire(io.O, io.I[0])
                # io.O = io.I[0]
                # TODO: Alternative syntax
                # io.O <= io.I[0]
                # TODO: Or we could use wire syntax
                # wire(io.O, io.I[0])
            else:
                io.O = io.I[1]
    m.compile("build/test_if_statement_basic", TestIfStatementBasic)
    assert check_files_equal(__file__, f"build/test_if_statement_basic.v",
                             f"gold/test_if_statement_basic.v")


def test_ternary():
    class TestTernary(m.Circuit):
        IO = ["I", m.In(m.Bits(2)), "S", m.In(m.Bit), "O", m.Out(m.Bit)]

        @m.circuit_def
        def definition(io):
            m.wire(io.O, io.I[0] if io.S else io.I[1])
            # io.O = io.I[0] if io.S else io.I[1]
            # TODO: Or non block assign?
            # io.O <= io.I[0] if io.S else io.[1]
    m.compile("build/test_ternary", TestTernary)
    assert check_files_equal(__file__, f"build/test_ternary.v",
                             f"gold/test_ternary.v")
