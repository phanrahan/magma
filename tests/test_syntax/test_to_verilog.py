import pytest
import magma as m
from magma.testing import check_files_equal
import hwtypes
import operator
import kratos.debug
import os
import pytest

pytest.skip("Kratos failure", allow_module_level=True)


class SimpleALU(m.Circuit):
    io = m.IO(a=m.In(m.UInt[16]), b=m.In(m.UInt[16]),
              c=m.Out(m.UInt[16]), config_=m.In(m.Bits[2]))

    @m.circuit.combinational_to_verilog(debug=False)
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

    io.c <= execute_alu(io.a, io.b, io.config_)


def test_simple_alu():
    inst_to_defn_map = m.syntax.build_kratos_debug_info(SimpleALU, is_top=True)
    assert "SimpleALU.execute_alu_inst0" in inst_to_defn_map
    generators = []
    for instance_name, mod in inst_to_defn_map.items():
        mod.instance_name = instance_name
        generators.append(mod)

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
        # dump database
        # change the target to system verilog if you're using ncsim/vcs. fault uses
        # different name for different targets
        target = "verilator"
        if target == "verilator":
            top_module_name = "TOP"
        else:
            top_module_name = "dut"
        kratos.debug.dump_external_database(
            generators, top_module_name, f"{directory}debug.db")
        tester.compile_and_run(target,
                               directory=directory,
                               flags=["-Wno-fatal"], skip_compile=True)

    except ImportError:
        pass


def test_seq_simple():
    @m.circuit.sequential_to_verilog(async_reset=True, debug=False)
    class TestBasicToVerilog:
        def __init__(self):
            self.x: m.Bits[2] = m.bits(0, 2)
            self.y: m.Bits[2] = m.bits(0, 2)

        def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
            # Issue: can't overload temporary name with output name
            _O = self.y
            self.y = self.x
            self.x = I
            return _O

    m.compile('build/TestBasicToVerilog', TestBasicToVerilog, output="verilog")
    assert check_files_equal(__file__, f"build/TestBasicToVerilog.v",
                             f"gold/TestBasicToVerilog.v")
    try:
        # Test with fault if available
        import fault
        target = "verilator"
        tester = fault.Tester(TestBasicToVerilog)
        stream = hwtypes.BitVector.random(10)
        tester.circuit.ASYNCRESET = 0
        tester.eval()
        tester.circuit.ASYNCRESET = 1
        tester.eval()
        tester.circuit.ASYNCRESET = 0
        print(stream.as_bool_list())
        for i in range(len(stream)):
            tester.circuit.I = stream[i]
            tester.print(f"%d\n", tester.circuit.O)
            if i > 1:
                tester.circuit.O.expect(stream[i - 2])
            else:
                tester.circuit.O.expect(0)
            tester.step(2)
        directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
        target = "verilator"
        if target == "verilator":
            top_module_name = "TOP"
        else:
            top_module_name = "dut"
        # TODO automatically obtain the kratos-based circuit
        generators = [TestBasicToVerilog.kratos]
        kratos.debug.dump_external_database(
            generators, top_module_name, f"{directory}debug.db")
        tester.compile_and_run(target,
                               directory=directory,
                               flags=["-Wno-fatal"], magma_output="verilog")

    except ImportError:
        pass
