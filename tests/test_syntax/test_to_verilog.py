import magma as m
from magma.testing import check_files_equal
import mantle


class SimpleALU(m.Circuit):
    IO = ["a", m.In(m.UInt[16]), "b", m.In(m.UInt[16]), "c",
          m.Out(m.UInt[16]), "config", m.In(m.Bits[2])]

    @m.circuit.combinational_to_verilog
    def execute_alu(a: m.UInt[16], b: m.UInt[16], config: m.Bits[2]) -> \
            m.UInt[16]:
        if config == m.bits(0, 2):
            c = a + b
        elif config == m.bits(1, 2):
            c = a - b
        elif config == m.bits(2, 2):
            c = a * b
        else:
            c = m.bits(0, 16)
        return c

    @classmethod
    def definition(io):
        io.c <= io.execute_alu(io.a, io.b, io.config)


def test_simple_alu():
    m.compile('build/SimpleALU', SimpleALU, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/SimpleALU.v",
                             f"gold/SimpleALU.v")
