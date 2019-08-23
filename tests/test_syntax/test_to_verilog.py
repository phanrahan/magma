import magma as m
from magma.testing import check_files_equal
import mantle
import hwtypes
import operator
import tempfile
import os


class SimpleALU(m.Circuit):
    IO = ["a", m.In(m.UInt[16]), "b", m.In(m.UInt[16]), "c",
          m.Out(m.UInt[16]), "config_", m.In(m.Bits[2])]

    @m.circuit.combinational_to_verilog
    def execute_alu(a: m.UInt[16], b: m.UInt[16], config_: m.Bits[2]) -> \
            m.UInt[16]:
        if config_ == m.bits(0, 2):
            c = a + b
        elif config_ == m.bits(1, 2):
            c = a - b
        elif config_ == m.bits(2, 2):
            c = a * b
        else:
            c = m.bits(0, 16)
        return c

    @classmethod
    def definition(io):
        io.c <= io.execute_alu(io.a, io.b, io.config_)


def test_simple_alu():
    m.compile('build/SimpleALU', SimpleALU, output="coreir-verilog")
    assert check_files_equal(__file__, f"build/SimpleALU.v",
                             f"gold/SimpleALU.v")
    try:
        # Test with fault if available
        import fault
        tester = fault.Tester(SimpleALU)
        ops = [operator.add, operator.sub, operator.mul, operator.floordiv]
        for i, op in enumerate(ops):
            tester.circuit.config_ = i
            tester.circuit.a = a = hwtypes.BitVector.random(16)
            tester.circuit.b = b = hwtypes.BitVector.random(16)
            tester.eval()
            if op == operator.floordiv:
                tester.circuit.c.expect(0)
            else:
                tester.circuit.c.expect(op(a, b))
        directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
        tester.compile_and_run("verilator",
                               directory=directory,
                               flags=["-Wno-fatal"], skip_compile=True)

    except ImportError:
        pass
