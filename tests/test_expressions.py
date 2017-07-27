from magma import *
from magma.backend import verilog
from magma.verilator.verilator import compile as compileverilator
from magma.verilator.verilator import run_verilator_test

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
            d = (circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_1_bit_logic", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_1_bit_logic.v", "gold/test_1_bit_logic.v")
    def f(a, b, c):
        return (a & b) | (b ^ c)

    compileverilator('build/sim_test_1_bit_logic_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_1_bit_logic.v")
    run_verilator_test('test_1_bit_logic', 'sim_test_1_bit_logic_main', 'test_circuit1')


def test_bits_logic():
    class TestCircuit(Circuit):
        name = "test_circuit2"
        IO = ["a", In(Bits(4)), "b", In(Bits(4)), "c", In(Bits(4)), "d", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            d = (circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_bits_logic", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_logic.v", "gold/test_bits_logic.v")
    def f(a, b, c):
        return (a & b) | (b ^ c)

    compileverilator('build/sim_test_bits_logic_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_bits_logic.v")
    run_verilator_test('test_bits_logic', 'sim_test_bits_logic_main', 'test_circuit2')


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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
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
        IO = ["a", In(Bits(4)), "b", In(Bits(4)), "c", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a << circuit.b
            wire(c, circuit.c)
    compile("build/test_bits_dlshift", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a):
        return a >> 3

    compileverilator('build/sim_test_bits_rshift_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_bits_rshift.v")
    run_verilator_test('test_bits_rshift', 'sim_test_bits_rshift_main', 'test_rshift')


def test_bits_drshift():
    class TestCircuit(Circuit):
        name = "test_drshift"
        IO = ["a", In(Bits(4)), "b", In(Bits(4)), "c", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a << circuit.b
            wire(c, circuit.c)
    compile("build/test_bits_drshift", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a << b

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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a / b

    compileverilator('build/sim_test_uint_div_main.cpp', TestCircuit, f, input_range=range(1, 1 << 4))
    insert_coreir_stdlib_include("build/test_uint_div.v")
    run_verilator_test('test_uint_div', 'sim_test_uint_div_main', 'test_uint_div')


def test_uint_lt():
    class TestCircuit(Circuit):
        name = "test_uint_lt"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(1))]
        @classmethod
        def definition(circuit):
            c = circuit.a < circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_lt", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a < b

    compileverilator('build/sim_test_uint_lt_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_uint_lt.v")
    run_verilator_test('test_uint_lt', 'sim_test_uint_lt_main', 'test_uint_lt')


def test_uint_le():
    class TestCircuit(Circuit):
        name = "test_uint_le"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(1))]
        @classmethod
        def definition(circuit):
            c = circuit.a <= circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_le", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a <= b

    compileverilator('build/sim_test_uint_le_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_uint_le.v")
    run_verilator_test('test_uint_le', 'sim_test_uint_le_main', 'test_uint_le')


def test_uint_gt():
    class TestCircuit(Circuit):
        name = "test_uint_gt"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(1))]
        @classmethod
        def definition(circuit):
            c = circuit.a > circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_gt", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a > b

    compileverilator('build/sim_test_uint_gt_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_uint_gt.v")
    run_verilator_test('test_uint_gt', 'sim_test_uint_gt_main', 'test_uint_gt')


def test_uint_ge():
    class TestCircuit(Circuit):
        name = "test_uint_ge"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(1))]
        @classmethod
        def definition(circuit):
            c = circuit.a >= circuit.b
            wire(c, circuit.c)
    compile("build/test_uint_ge", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a >= b

    compileverilator('build/sim_test_uint_ge_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_uint_ge.v")
    run_verilator_test('test_uint_ge', 'sim_test_uint_ge_main', 'test_uint_ge')


def test_sint_add():
    class TestCircuit(Circuit):
        name = "test_sint_add"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(4))]
        @classmethod
        def definition(circuit):
            c = circuit.a + circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_add", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
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
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a * b

    compileverilator('build/sim_test_sint_div_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_div.v")
    run_verilator_test('test_sint_div', 'sim_test_sint_div_main', 'test_sint_div')


def test_sint_lt():
    class TestCircuit(Circuit):
        name = "test_sint_lt"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(1))]
        @classmethod
        def definition(circuit):
            c = circuit.a < circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_lt", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a < b

    compileverilator('build/sim_test_sint_lt_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_lt.v")
    run_verilator_test('test_sint_lt', 'sim_test_sint_lt_main', 'test_sint_lt')


def test_sint_le():
    class TestCircuit(Circuit):
        name = "test_sint_le"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(1))]
        @classmethod
        def definition(circuit):
            c = circuit.a <= circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_le", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a <= b

    compileverilator('build/sim_test_sint_le_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_le.v")
    run_verilator_test('test_sint_le', 'sim_test_sint_le_main', 'test_sint_le')


def test_sint_gt():
    class TestCircuit(Circuit):
        name = "test_sint_gt"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(1))]
        @classmethod
        def definition(circuit):
            c = circuit.a > circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_gt", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a > b

    compileverilator('build/sim_test_sint_gt_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_gt.v")
    run_verilator_test('test_sint_gt', 'sim_test_sint_gt_main', 'test_sint_gt')


def test_sint_ge():
    class TestCircuit(Circuit):
        name = "test_sint_ge"
        IO = ["a", In(SInt(4)), "b", In(SInt(4)), "c", Out(SInt(1))]
        @classmethod
        def definition(circuit):
            c = circuit.a >= circuit.b
            wire(c, circuit.c)
    compile("build/test_sint_ge", TestCircuit)
    # assert magma_check_files_equal(__file__, "build/test_bits_shift.v", "gold/test_bits_shift.v")
    def f(a, b):
        return a >= b

    compileverilator('build/sim_test_sint_ge_main.cpp', TestCircuit, f)
    insert_coreir_stdlib_include("build/test_sint_ge.v")
    run_verilator_test('test_sint_ge', 'sim_test_sint_ge_main', 'test_sint_ge')
