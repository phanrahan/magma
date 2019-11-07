import magma as m
from magma.testing import check_files_equal
import hwtypes
import operator
import tempfile
import kratos.debug
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


def build_kratos_debug_info(circuit, is_top):
    inst_to_defn_map = {}
    for instance in circuit.instances:
        instance_inst_to_defn_map = \
            build_kratos_debug_info(type(instance), is_top=False)
        for k, v in instance_inst_to_defn_map.values():
            key = instance.name + "." + k
            if is_top:
                key = circuit.name + "." + key
            inst_to_defn_map[key] = v
        inst_name = instance.name
        if is_top:
            inst_name = circuit.name + "." + instance.name
        if instance.kratos is not None:
            inst_to_defn_map[inst_name] = instance.kratos
    return inst_to_defn_map


def test_simple_alu():
    inst_to_defn_map = build_kratos_debug_info(SimpleALU, is_top=True)
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
        kratos.debug.dump_external_database(generators, top_module_name, f"{directory}debug.db")
        tester.compile_and_run(target,
                               directory=directory,
                               flags=["-Wno-fatal"], skip_compile=True)

    except ImportError:
        pass
