from magma import *
from magma.backend import verilog
from magma.verilator.verilator import compile as compileverilator
from magma.verilator.verilator import run_verilator_test
from magma.verilator.function import testvectors
import itertools
from magma.python_simulator import PythonSimulator
from magma.scope import Scope

def insert_coreir_stdlib_include(verilog_file):
    file_path = os.path.dirname(__file__)
    verilog_file = os.path.join(file_path, verilog_file)

    with open(verilog_file, "r") as f:
        contents = f.readlines()

    contents.insert(0, "`include \"stdlib.v\"\n")
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
    insert_coreir_stdlib_include("build/test_1_bit_logic.v")
    run_verilator_test('test_1_bit_logic', 'sim_test_1_bit_logic_main', 'test_circuit1')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c, d in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list()[0])
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list()[0])
        simulator.set_value(TestCircuit.c, scope, c.as_bool_list()[0])
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.d, scope) == d.as_bool_list()[0]


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
    insert_coreir_stdlib_include("build/test_bits_logic.v")
    run_verilator_test('test_bits_logic', 'sim_test_bits_logic_main', 'test_circuit2')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c, d in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.set_value(TestCircuit.c, scope, c.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.d, scope) == d.as_bool_list()


def test_bits_lshift():
    class TestCircuit(Circuit):
        name = "test_lshift"
        # IO = ["a", In(Bits(4)), "b", In(Bits(4)), "c", Out(Bits(4)), "d", Out(Bits(4))]
        IO = ["a", In(Bits(4)), "b", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            b = circuit.a << 2
            # d = circuit.a >> 3
            # tmp3 = circuit.a << circuit.b
            # tmp4 = circuit.a >> circuit.c
            # d = tmp1 & tmp2 ^ tmp3 | tmp4
            # wire(c, circuit.c)
            wire(b, circuit.b)
    compile("build/test_bits_lshift", TestCircuit)
    def f(a):
        return a << 2
        # tmp3 = a << b
        # tmp4 = a >> c
        # return tmp1 & tmp2 ^ tmp3 | tmp4

    compileverilator('build/sim_test_bits_lshift_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_bits_lshift.v")
    run_verilator_test('test_bits_lshift', 'sim_test_bits_lshift_main', 'test_lshift')


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

    compileverilator('build/sim_test_bits_dlshift_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_bits_dlshift.v")
    run_verilator_test('test_bits_dlshift', 'sim_test_bits_dlshift_main', 'test_dlshift')


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

    compileverilator('build/sim_test_bits_rshift_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_bits_rshift.v")
    run_verilator_test('test_bits_rshift', 'sim_test_bits_rshift_main', 'test_rshift')


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

    compileverilator('build/sim_test_bits_drshift_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_bits_drshift.v")
    run_verilator_test('test_bits_drshift', 'sim_test_bits_drshift_main', 'test_drshift')


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

    compileverilator('build/sim_test_uint_add_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_uint_add.v")
    run_verilator_test('test_uint_add', 'sim_test_uint_add_main', 'test_uint_add')


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

    compileverilator('build/sim_test_uint_sub_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_uint_sub.v")
    run_verilator_test('test_uint_sub', 'sim_test_uint_sub_main', 'test_uint_sub')


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

    compileverilator('build/sim_test_uint_mul_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_uint_mul.v")
    run_verilator_test('test_uint_mul', 'sim_test_uint_mul_main', 'test_uint_mul')


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

    compileverilator('build/sim_test_uint_div_main.cpp', TestCircuit, f, input_ranges=(range(0, 1 << 4), range(1, 1 << 4)))
    insert_coreir_stdlib_include("build/test_uint_div.v")
    run_verilator_test('test_uint_div', 'sim_test_uint_div_main', 'test_uint_div')


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
    insert_coreir_stdlib_include("build/test_uint_lt.v")
    run_verilator_test('test_uint_lt', 'sim_test_uint_lt_main', 'test_uint_lt')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c.as_bool_list()[0]


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
    insert_coreir_stdlib_include("build/test_uint_le.v")
    run_verilator_test('test_uint_le', 'sim_test_uint_le_main', 'test_uint_le')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c.as_bool_list()[0]


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
    insert_coreir_stdlib_include("build/test_uint_gt.v")
    run_verilator_test('test_uint_gt', 'sim_test_uint_gt_main', 'test_uint_gt')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c.as_bool_list()[0]


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
    insert_coreir_stdlib_include("build/test_uint_ge.v")
    run_verilator_test('test_uint_ge', 'sim_test_uint_ge_main', 'test_uint_ge')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c.as_bool_list()[0]


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

    compileverilator('build/sim_test_sint_add_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_add.v")
    run_verilator_test('test_sint_add', 'sim_test_sint_add_main', 'test_sint_add')


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

    compileverilator('build/sim_test_sint_sub_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_sub.v")
    run_verilator_test('test_sint_sub', 'sim_test_sint_sub_main', 'test_sint_sub')


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

    compileverilator('build/sim_test_sint_mul_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_mul.v")
    run_verilator_test('test_sint_mul', 'sim_test_sint_mul_main', 'test_sint_mul')


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

    compileverilator('build/sim_test_sint_div_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_div.v")
    run_verilator_test('test_sint_div', 'sim_test_sint_div_main', 'test_sint_div')


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
    insert_coreir_stdlib_include("build/test_sint_lt.v")
    run_verilator_test('test_sint_lt', 'sim_test_sint_lt_main', 'test_sint_lt')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c.as_bool_list()[0]


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
    insert_coreir_stdlib_include("build/test_sint_le.v")
    run_verilator_test('test_sint_le', 'sim_test_sint_le_main', 'test_sint_le')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c.as_bool_list()[0]


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
    insert_coreir_stdlib_include("build/test_sint_gt.v")
    run_verilator_test('test_sint_gt', 'sim_test_sint_gt_main', 'test_sint_gt')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c.as_bool_list()[0]


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
    insert_coreir_stdlib_include("build/test_sint_ge.v")

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for a, b, c in test_vectors:
        simulator.set_value(TestCircuit.a, scope, a.as_bool_list())
        simulator.set_value(TestCircuit.b, scope, b.as_bool_list())
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.c, scope) == c.as_bool_list()[0], "Failed on {}, {}, {}".format(a, b, c)

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

    compileverilator('build/sim_test_sint_arithmetic_right_shift_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_arithmetic_right_shift.v")
    run_verilator_test('test_sint_arithmetic_right_shift', 'sim_test_sint_arithmetic_right_shift_main', 'test_sint_arithmetic_right_shift')


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

    compileverilator('build/sim_test_sint_dynamic_arithmetic_right_shift_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_dynamic_arithmetic_right_shift.v")
    run_verilator_test('test_sint_dynamic_arithmetic_right_shift', 'sim_test_sint_dynamic_arithmetic_right_shift_main', 'test_sint_dynamic_arithmetic_right_shift')
