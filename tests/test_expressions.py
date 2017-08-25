from magma import *
from magma.backend import verilog
from magma.verilator.verilator import compile as compileverilator
from magma.verilator.verilator import run_verilator_test
from magma.verilator.function import testvectors
import itertools
from magma.python_simulator import PythonSimulator
from magma.scope import Scope

def insert_coreir_include(verilog_file):
    file_path = os.path.dirname(__file__)
    verilog_file = os.path.join(file_path, verilog_file)

    with open(verilog_file, "r") as f:
        contents = f.readlines()

    contents.insert(0, "`include \"{}\"\n".format(coreir_primitives_file_path))
    with open(verilog_file, "w") as f:
        f.write("".join(contents))

def test_1_bit_logic():
    class TestCircuit(Circuit):
        name = "test_circuit1"
        IO = ["a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit)]
        @classmethod
        def definition(circuit):
            d = ~(circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_1_bit_logic", TestCircuit)
    def f(a, b, c):
        return ~(a & b) | (b ^ c)

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_1_bit_logic_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_1_bit_logic.v")
    run_verilator_test('test_1_bit_logic', 'sim_test_1_bit_logic_main', 'test_circuit1')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c, d in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.set_value(TestCircuit.c, scope, c)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.d, scope) == d


def test_bits_logic():
    class TestCircuit(Circuit):
        name = "test_circuit2"
        IO = ["a", In(Bits(4)), "b", In(Bits(4)), "c", In(Bits(4)), "d", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            d = ~(circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_bits_logic", TestCircuit)
    def f(a, b, c):
        return ~(a & b) | (b ^ c)

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_bits_logic_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_bits_logic.v")
    run_verilator_test('test_bits_logic', 'sim_test_bits_logic_main', 'test_circuit2')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c, d in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.set_value(TestCircuit.c, scope, c)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.d, scope) == d


def test_bits_eq():
    class TestCircuit(Circuit):
        name = "test_eq"
        IO = ["a", In(Bits(4)), "b", In(Bits(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a == circuit.b
            wire(c, circuit.c)
    compile("build/test_bits_eq", TestCircuit)
    def f(a, b):
        return a == b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_bits_eq_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_bits_eq.v")
    run_verilator_test('test_bits_eq', 'sim_test_bits_eq_main', 'test_eq')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_bits_lshift():
    class TestCircuit(Circuit):
        name = "test_lshift"
        IO = ["a", In(Bits(4)), "b", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            b = circuit.a << 2
            wire(b, circuit.b)
    compile("build/test_bits_lshift", TestCircuit)
    def f(a):
        return a << 2

    test_vectors = testvectors(TestCircuit, f)

    compileverilator('build/sim_test_bits_lshift_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_bits_lshift.v")
    run_verilator_test('test_bits_lshift', 'sim_test_bits_lshift_main', 'test_lshift')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.b, scope) == b


def test_bits_dlshift():
    class TestCircuit(Circuit):
        name = "test_dlshift"
        IO = ["a", In(Bits(4)), "b", In(UInt(4)), "c", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a << circuit.b
            wire(c, circuit.c)
    compile("build/test_bits_dlshift", TestCircuit)
    def f(a, b):
        return a << b

    test_vectors = testvectors(TestCircuit, f)

    compileverilator('build/sim_test_bits_dlshift_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_bits_dlshift.v")
    run_verilator_test('test_bits_dlshift', 'sim_test_bits_dlshift_main', 'test_dlshift')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_bits_rshift():
    class TestCircuit(Circuit):
        name = "test_rshift"
        IO = ["a", In(Bits(4)), "b", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            b = circuit.a >> 3
            wire(b, circuit.b)
    compile("build/test_bits_rshift", TestCircuit)
    def f(a):
        return a >> 3

    test_vectors = testvectors(TestCircuit, f)

    compileverilator('build/sim_test_bits_rshift_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_bits_rshift.v")
    run_verilator_test('test_bits_rshift', 'sim_test_bits_rshift_main', 'test_rshift')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.b, scope) == b


def test_bits_drshift():
    class TestCircuit(Circuit):
        name = "test_drshift"
        IO = ["a", In(Bits(4)), "b", In(UInt(4)), "c", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a >> circuit.b
            wire(c, circuit.c)
    compile("build/test_bits_drshift", TestCircuit)
    def f(a, b):
        return a >> b

    test_vectors = testvectors(TestCircuit, f)

    compileverilator('build/sim_test_bits_drshift_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_bits_drshift.v")
    run_verilator_test('test_bits_drshift', 'sim_test_bits_drshift_main', 'test_drshift')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_uint_add():
    class TestCircuit(Circuit):
        name = "test_uint_add"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a + circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_add", TestCircuit)
    def f(a, b):
        return a + b

    test_vectors = testvectors(TestCircuit, f)

    compileverilator('build/sim_test_uint_add_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_uint_add.v")
    run_verilator_test('test_uint_add', 'sim_test_uint_add_main', 'test_uint_add')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_uint_sub():
    class TestCircuit(Circuit):
        name = "test_uint_sub"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a - circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_sub", TestCircuit)
    def f(a, b):
        return a - b

    test_vectors = testvectors(TestCircuit, f)

    compileverilator('build/sim_test_uint_sub_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_uint_sub.v")
    run_verilator_test('test_uint_sub', 'sim_test_uint_sub_main', 'test_uint_sub')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_uint_mul():
    class TestCircuit(Circuit):
        name = "test_uint_mul"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a * circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_mul", TestCircuit)
    def f(a, b):
        return a * b

    test_vectors = testvectors(TestCircuit, f)

    compileverilator('build/sim_test_uint_mul_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_uint_mul.v")
    run_verilator_test('test_uint_mul', 'sim_test_uint_mul_main', 'test_uint_mul')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_uint_div():
    class TestCircuit(Circuit):
        name = "test_uint_div"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a / circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_div", TestCircuit)
    def f(a, b):
        return a / b

    test_vectors = testvectors(TestCircuit, f, input_ranges=(range(0, 1 << 4),
        range(1, 1 << 4)))
    compileverilator('build/sim_test_uint_div_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_uint_div.v")
    run_verilator_test('test_uint_div', 'sim_test_uint_div_main', 'test_uint_div')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_uint_lt():
    class TestCircuit(Circuit):
        name = "test_uint_lt"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a < circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_lt", TestCircuit)
    def f(a, b):
        return a < b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_uint_lt_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_uint_lt.v")
    run_verilator_test('test_uint_lt', 'sim_test_uint_lt_main', 'test_uint_lt')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_uint_le():
    class TestCircuit(Circuit):
        name = "test_uint_le"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a <= circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_le", TestCircuit)
    def f(a, b):
        return a <= b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_uint_le_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_uint_le.v")
    run_verilator_test('test_uint_le', 'sim_test_uint_le_main', 'test_uint_le')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_uint_gt():
    class TestCircuit(Circuit):
        name = "test_uint_gt"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a > circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_gt", TestCircuit)
    def f(a, b):
        return a > b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_uint_gt_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_uint_gt.v")
    run_verilator_test('test_uint_gt', 'sim_test_uint_gt_main', 'test_uint_gt')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_uint_ge():
    class TestCircuit(Circuit):
        name = "test_uint_ge"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a >= circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_ge", TestCircuit)
    def f(a, b):
        return a >= b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_uint_ge_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_uint_ge.v")
    run_verilator_test('test_uint_ge', 'sim_test_uint_ge_main', 'test_uint_ge')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_sint_add():
    class TestCircuit(Circuit):
        name = "test_sint_add"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a + circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_add", TestCircuit)
    def f(a, b):
        return a + b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_add_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_add.v")
    run_verilator_test('test_sint_add', 'sim_test_sint_add_main', 'test_sint_add')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_sint_sub():
    class TestCircuit(Circuit):
        name = "test_sint_sub"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a - circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_sub", TestCircuit)
    def f(a, b):
        return a - b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_sub_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_sub.v")
    run_verilator_test('test_sint_sub', 'sim_test_sint_sub_main', 'test_sint_sub')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_sint_mul():
    class TestCircuit(Circuit):
        name = "test_sint_mul"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a * circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_mul", TestCircuit)
    def f(a, b):
        return a * b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_mul_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_mul.v")
    run_verilator_test('test_sint_mul', 'sim_test_sint_mul_main', 'test_sint_mul')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_sint_div():
    class TestCircuit(Circuit):
        name = "test_sint_div"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a * circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_div", TestCircuit)
    def f(a, b):
        return a * b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_div_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_div.v")
    run_verilator_test('test_sint_div', 'sim_test_sint_div_main', 'test_sint_div')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_sint_lt():
    class TestCircuit(Circuit):
        name = "test_sint_lt"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a < circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_lt", TestCircuit)
    def f(a, b):
        return a < b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_lt_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_lt.v")
    run_verilator_test('test_sint_lt', 'sim_test_sint_lt_main', 'test_sint_lt')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_sint_le():
    class TestCircuit(Circuit):
        name = "test_sint_le"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a <= circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_le", TestCircuit)
    def f(a, b):
        return a <= b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_le_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_le.v")
    run_verilator_test('test_sint_le', 'sim_test_sint_le_main', 'test_sint_le')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_sint_gt():
    class TestCircuit(Circuit):
        name = "test_sint_gt"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a > circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_gt", TestCircuit)
    def f(a, b):
        return a > b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_gt_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_gt.v")
    run_verilator_test('test_sint_gt', 'sim_test_sint_gt_main', 'test_sint_gt')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c


def test_sint_ge():
    class TestCircuit(Circuit):
        name = "test_sint_ge"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(Bit)]
        @classmethod
        def definition(circuit):
            c = circuit.a >= circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_ge", TestCircuit)
    def f(a, b):
        return a >= b

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_ge_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_ge.v")

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c, "Failed on {}, {}, {}".format(a, b, c)

def test_sint_arithmetic_right_shift():
    class TestCircuit(Circuit):
        name = "test_sint_arithmetic_right_shift"
        IO = ["a", In(SInt(4)), "b", Out(SInt(4))]
        @classmethod
        def definition(circuit):
            b = circuit.a.arithmetic_shift_right(2)
            wire(b, circuit.b)
    compile("build/test_sint_arithmetic_right_shift", TestCircuit)
    def f(a):
        return a.arithmetic_shift_right(2)

    test_vectors = testvectors(TestCircuit, f)
    compileverilator('build/sim_test_sint_arithmetic_right_shift_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_arithmetic_right_shift.v")
    run_verilator_test('test_sint_arithmetic_right_shift',
            'sim_test_sint_arithmetic_right_shift_main',
            'test_sint_arithmetic_right_shift')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.b, scope) == b


def test_sint_dynamic_arithmetic_right_shift():
    class TestCircuit(Circuit):
        name = "test_sint_dynamic_arithmetic_right_shift"
        IO = ["a", In(SInt(4)), "b", In(UInt(4)), "c", Out(SInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a.arithmetic_shift_right(circuit.b)
            wire(c, circuit.c)
    compile("build/test_sint_dynamic_arithmetic_right_shift", TestCircuit)
    def f(a, b):
        return a.arithmetic_shift_right(b)

    test_vectors = testvectors(TestCircuit, f, input_ranges=(range(-2**3, 2**3),
        range(0, 1 << 4)))
    compileverilator('build/sim_test_sint_dynamic_arithmetic_right_shift_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_sint_dynamic_arithmetic_right_shift.v")
    run_verilator_test('test_sint_dynamic_arithmetic_right_shift',
            'sim_test_sint_dynamic_arithmetic_right_shift_main',
            'test_sint_dynamic_arithmetic_right_shift')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a)
        simulator.set_value(TestCircuit.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c, (a.as_bool_list(), b.as_bool_list(), c.as_bool_list())
