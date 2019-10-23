import magma as m
from magma.testing import check_files_equal
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


def build_kratos_debug_info(circuit, is_top):
    symbols = []
    inst_to_defn_map = {}
    for instance in circuit.instances:
        instance_symbols, instance_inst_to_defn_map = \
            build_kratos_debug_info(type(instance), is_top=False)
        for symbol in instance_symbols:
            symbol = instance.name + "." + symbol
            if is_top:
                symbol = circuit.name + "." + symbol
            symbols.append(symbol)
        for k, v in instance_inst_to_defn_map.values():
            key = instance.name + "." + k
            if is_top:
                key = circuit.name + "." + key
            inst_to_defn_map[key] = v
        inst_name = instance.name
        if is_top:
            inst_name = circuit.name + "." + instance.name
        inst_to_defn_map[inst_name] = type(instance).name
    for key in circuit.interface.ports.keys():
        if is_top:
            key = circuit.name + "." + key
        symbols.append(key)
    return symbols, inst_to_defn_map


def test_simple_alu():
    symbols, inst_to_defn_map = \
        build_kratos_debug_info(SimpleALU, is_top=True)
    assert symbols == ['SimpleALU.execute_alu_inst0.a',
                       'SimpleALU.execute_alu_inst0.b',
                       'SimpleALU.execute_alu_inst0.config_',
                       'SimpleALU.execute_alu_inst0.O', 'SimpleALU.a',
                       'SimpleALU.b', 'SimpleALU.c', 'SimpleALU.config_']
    assert inst_to_defn_map == {'SimpleALU.execute_alu_inst0': 'execute_alu'}
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
