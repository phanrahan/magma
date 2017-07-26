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


# def test_uint_logic():
#     class TestCircuit(Circuit):
#         name = "test_circuit4"
#         IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", In(UInt(4)), "d", Out(UInt(4))]
#         @classmethod
#         def definition(circuit):
#             d = (circuit.a & circuit.b) | (circuit.b ^ circuit.c)
#             wire(d, circuit.d)
#     compile("build/test_uint_logic", TestCircuit)
#     # assert magma_check_files_equal(__file__, "build/test_uint_logic.v", "gold/test_uint_logic.v")
#     def f(a, b, c):
#         return (a & b) | (b ^ c)
# 
#     compileverilator('build/sim_test_uint_logic_main.cpp', TestCircuit, f)
#     insert_coreir_stdlib_include("build/test_uint_logic.v")
#     run_verilator_test('test_uint_logic', 'sim_test_uint_logic_main', 'test_circuit4')


# def test_uint_arithmetic():
#     class TestCircuit(Circuit):
#         name = "test_circuit"
#         IO = ["in0", In(UInt(8)), "in1", In(UInt(8)), "out", Out(Bit)]
#         @classmethod
#         def definition(circuit):
#             a = circuit.in0 + circuit.in1
#             b = a - circuit.in1
#             c = a * circuit.in0
#             d = b / c > circuit.in0
#             e = b * c < int2seq(1, 8)
#             f = a - c >= circuit.in0
#             g = b + c <= int2seq(1, 8)
#             wire(g, circuit.out)
#     compile("build/test_uint_arithmetic", TestCircuit)
#     assert magma_check_files_equal(__file__, "build/test_uint_arithmetic.v", "gold/test_uint_arithmetic.v")


# def test_sint_logic():
#     class TestCircuit(Circuit):
#         name = "test_circuit"
#         IO = ["a", In(SInt(8)), "b", In(SInt(8)), "c", In(SInt(8)), "d", In(SInt(3)), "e", Out(SInt(8))]
#         @classmethod
#         def definition(circuit):
#             e = (circuit.a & circuit.b) | (circuit.b ^ ~circuit.c) >> 3 >> circuit.d << 3 << circuit.d
#             wire(e, circuit.e)
#     assert verilog.compile(TestCircuit) == """
# module test_circuit (input signed [7:0] a, input signed [7:0] b, input signed [7:0] c, input signed [2:0] d, output signed [7:0] e);
# wire [7:0] inst0_O;
# wire [7:0] inst1_O;
# wire [7:0] inst2_O;
# wire [7:0] inst3_O;
# wire [7:0] inst4_O;
# wire [7:0] inst5_O;
# wire [7:0] inst6_O;
# wire [7:0] inst7_O;
# And8 inst0 (.I0(a), .I1(b), .O(inst0_O));
# Invert8 inst1 (.I(c), .O(inst1_O));
# Xor8 inst2 (.I0(b), .I1(inst1_O), .O(inst2_O));
# ShiftRight8_3 inst3 (.I(inst2_O), .O(inst3_O));
# DynamicShiftRight8 inst4 (.I0(inst3_O), .I1(d), .O(inst4_O));
# ShiftLeft8_3 inst5 (.I(inst4_O), .O(inst5_O));
# DynamicShiftLeft8 inst6 (.I0(inst5_O), .I1(d), .O(inst6_O));
# Or8 inst7 (.I0(inst0_O), .I1(inst6_O), .O(inst7_O));
# assign e = inst7_O;
# endmodule
# 
# """.lstrip()
# 
# 
# def test_sint_arithmetic():
#     class TestCircuit(Circuit):
#         name = "test_circuit"
#         IO = ["in0", In(SInt(8)), "in1", In(SInt(8)), "out", Out(Bit)]
#         @classmethod
#         def definition(circuit):
#             a = circuit.in0 + circuit.in1
#             b = a - circuit.in1
#             c = a * circuit.in0
#             d = b / c > circuit.in0
#             e = b * c < int2seq(1, 8)
#             f = a - c >= circuit.in0
#             g = b + c <= int2seq(1, 8)
#             wire(g, circuit.out)
#     assert verilog.compile(TestCircuit) == """
# module test_circuit (input signed [7:0] in0, input signed [7:0] in1, output  out);
# wire signed [7:0] inst0_O;
# wire signed [7:0] inst1_O;
# wire signed [7:0] inst2_O;
# wire signed [7:0] inst3_O;
# wire  inst4_O;
# wire signed [7:0] inst5_O;
# wire  inst6_O;
# wire signed [7:0] inst7_O;
# wire  inst8_O;
# wire signed [7:0] inst9_O;
# wire  inst10_O;
# SignedAdd8 inst0 (.I0(in0), .I1(in1), .O(inst0_O));
# SignedSub8 inst1 (.I0(inst0_O), .I1(in1), .O(inst1_O));
# SignedMul8 inst2 (.I0(inst0_O), .I1(in0), .O(inst2_O));
# SignedDiv8 inst3 (.I0(inst1_O), .I1(inst2_O), .O(inst3_O));
# SignedGt8 inst4 (.I0(inst3_O), .I1(in0), .O(inst4_O));
# SignedMul8 inst5 (.I0(inst1_O), .I1(inst2_O), .O(inst5_O));
# SignedLt8 inst6 (.I0(inst5_O), .I1({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b1}), .O(inst6_O));
# SignedSub8 inst7 (.I0(inst0_O), .I1(inst2_O), .O(inst7_O));
# SignedGtE8 inst8 (.I0(inst7_O), .I1(in0), .O(inst8_O));
# SignedAdd8 inst9 (.I0(inst1_O), .I1(inst2_O), .O(inst9_O));
# SignedLtE8 inst10 (.I0(inst9_O), .I1({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b1}), .O(inst10_O));
# assign out = inst10_O;
# endmodule
# 
# """.lstrip()
