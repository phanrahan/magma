import operator
from functools import reduce
import magma as m
from magma import In, Out, Bit, Clock, UInt, SInt, Circuit, Bits, uint, wire, compile
from magma.primitives import DefineRegister, DefineMux, DefineMemory

from magma.primitives import DefineAnd, And, and_
from magma.primitives import DefineOr, Or, or_
from magma.primitives import DefineXOr, XOr, xor
from magma.primitives import DefineInvert, Invert, invert
from magma.primitives import DefineEQ, EQ, eq

from magma.bit_vector import BitVector
#from magma.bitutils import int2seq
from magma.verilator.verilator import compile as compileverilator
from magma.verilator.verilator import run_verilator_test
from magma.verilator.function import testvectors
from magma.python_simulator import PythonSimulator
from magma.scope import Scope
from magma.verilator.function import testvectors


def check_unary_circuit(circ, circ_name, reference):
    compile("build/{}".format(circ_name), circ, include_coreir=True)

    test_vectors = testvectors(circ, reference)
    compileverilator('build/sim_{}_main.cpp'.format(circ_name), circ, test_vectors)

    run_verilator_test(circ_name, 'sim_{}_main'.format(circ_name), circ_name)
    simulator = PythonSimulator(circ)
    scope = Scope()
    for a, b, c, d in test_vectors:
        simulator.set_value(circ.a, scope, a)
        simulator.evaluate()
        assert simulator.get_value(circ.b, scope) == b
        assert simulator.get_value(circ.c, scope) == c
        assert simulator.get_value(circ.d, scope) == d


def check_circuit(circ, circ_name, reference):
    compile("build/{}".format(circ_name), circ, include_coreir=True)

    test_vectors = testvectors(circ, reference)
    compileverilator('build/sim_{}_main.cpp'.format(circ_name), circ, test_vectors)

    run_verilator_test(circ_name, 'sim_{}_main'.format(circ_name), circ_name)
    simulator = PythonSimulator(circ)
    scope = Scope()
    for a, b, c, d, e in test_vectors:
        simulator.set_value(circ.a, scope, a)
        simulator.set_value(circ.b, scope, b)
        simulator.evaluate()
        assert simulator.get_value(circ.c, scope) == c
        assert simulator.get_value(circ.d, scope) == d
        assert simulator.get_value(circ.e, scope) == e


def run_test(name, define_op, instance_op, op, python_op, types):

    def reference(a, b):
        val = python_op(a, b)
        return val, val, val

    def test(T, width):
        circ_name = "test_define_{}{}".format(name, width)
        circ = m.DefineCircuit(circ_name,
            *["a", In(T), "b", In(T), "c", Out(T),
              "d", Out(T), "e", Out(T)])
        wire(define_op(2, width)()(circ.a, circ.b), circ.c)
        wire(instance_op(2)(circ.a, circ.b), circ.d)
        wire(op(circ.a, circ.b), circ.e)
        m.EndDefine()

        check_circuit(circ, circ_name, reference)

    for type_ in types:
        if type_ == Bit:
            test(Bit, None)
        else:
            for width in range(1, 4):
                test(type_(width), width)


def run_compare_test(name, define_op, instance_op, op, python_op, types):
    def reference(a, b):
        val = python_op(a, b)
        return val, val, val

    def test(T, width):
        circ_name = "test_define_{}{}".format(name, width)
        circ = m.DefineCircuit(circ_name,
            *["a", In(T), "b", In(T), "c", Out(Bit),
              "d", Out(Bit), "e", Out(Bit)])
        wire(define_op(2, width)()(circ.a, circ.b), circ.c)
        wire(instance_op(2)(circ.a, circ.b), circ.d)
        wire(op(circ.a, circ.b), circ.e)
        m.EndDefine()

        check_circuit(circ, circ_name, reference)

    for type_ in types:
        if type_ == Bit:
            test(Bit, None)
        else:
            for width in range(1, 4):
                test(type_(width), width)


def test_and():
    run_test("and", DefineAnd, And, and_, operator.and_, [Bit, Bits])


def test_or():
    run_test("or", DefineOr, Or, or_, operator.or_, [Bit, Bits])


def test_xor():
    run_test("xor", DefineXOr, XOr, xor, operator.xor, [Bit, Bits])


def test_eq():
    run_compare_test("eq", DefineEQ, EQ, eq, operator.eq, [Bit, Bits])


def run_unary_op_test(name, define_op, instance_op, op, python_op):
    width = 4

    def reference(a):
        val = python_op(a)
        return val, val, val

    circ_name = "test_define_{}".format(name, width)
    circ = m.DefineCircuit(circ_name,
        *["a", In(Bits(width)),
          "b", Out(Bits(width)), "c", Out(Bits(width)),
          "d", Out(Bits(width))])
    wire(define_op(width)()(circ.a), circ.b)
    wire(instance_op()(circ.a), circ.c)
    wire(op(circ.a), circ.d)
    m.EndDefine()

    check_unary_circuit(circ, circ_name, reference)

def test_invert():
    run_unary_op_test("invert", DefineInvert, Invert, invert, operator.invert)


def test_register():
    N = 4
    Register4 = DefineRegister(N, T=UInt)
    class TestCircuit(Circuit):
        name = "test_register"
        IO = ["CLK", In(Bit), "out", Out(UInt(N))]
        @classmethod
        def definition(circuit):
            reg = Register4()
            wire(reg.out, circuit.out)
            wire(getattr(reg, "in"), reg.out + uint(1, N))
            wire(circuit.CLK, reg.clk)

    compile("build/test_register", TestCircuit, include_coreir=True)
    expected_sequence = [BitVector(x, num_bits=N) for x in range(1, 1 << N)]
    test_vectors = [[BitVector(0, num_bits=1), BitVector(0, num_bits=N)]]  # We hardcode the first ouput
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), output])

    compileverilator('build/sim_test_register_main.cpp', TestCircuit, test_vectors)
    run_verilator_test('test_register', 'sim_test_register_main', 'test_register')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for clk, expected in test_vectors:
        simulator.set_value(TestCircuit.CLK, scope, clk)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.out, scope) == expected

def test_register_ce():
    N = 4
    Register4 = DefineRegister(N, has_ce=True, T=UInt)
    class TestCircuit(Circuit):
        name = "test_register_ce"
        IO = ["CLK", In(Bit), "CE", In(Bit), "out", Out(UInt(N))]
        @classmethod
        def definition(circuit):
            reg = Register4().when(circuit.CE)
            wire(reg.out, circuit.out)
            wire(getattr(reg, "in"), reg.out + uint(1, N))
            wire(circuit.CLK, reg.clk)

    compile("build/test_register_ce", TestCircuit, include_coreir=True)
    expected_sequence = [BitVector(x, num_bits=N) for x in range(1, 1 << N)]
    test_vectors = [[BitVector(0, num_bits=1), BitVector(1, num_bits=1), BitVector(0, num_bits=N)]]  # We hardcode the first ouput
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(1, num_bits=1), output])
        # Should not advance with clock enable low
        test_vectors.append([BitVector(1, num_bits=1), BitVector(0, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(0, num_bits=1), output])

    compileverilator('build/sim_test_register_ce_main.cpp', TestCircuit, test_vectors)
    run_verilator_test('test_register_ce', 'sim_test_register_ce_main', 'test_register_ce')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for clk, enable, expected in test_vectors:
        simulator.set_value(TestCircuit.CLK, scope, clk)
        simulator.set_value(TestCircuit.CE, scope, enable)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.out, scope) == expected

def test_register_reset():
    N = 4
    Register4 = DefineRegister(N, has_reset=True, T=UInt)
    class TestCircuit(Circuit):
        name = "test_register_reset"
        IO = ["CLK", In(Bit), "RESET", In(Bit), "out", Out(UInt(N))]
        @classmethod
        def definition(circuit):
            reg = Register4().reset(circuit.RESET)
            wire(reg.out, circuit.out)
            wire(getattr(reg, "in"), reg.out + uint(1, N))
            wire(circuit.CLK, reg.clk)

    compile("build/test_register_reset", TestCircuit, include_coreir=True)
    expected_sequence = [BitVector(x, num_bits=N) for x in range(1, (1 << N) - 4)]
    test_vectors = [[BitVector(0, num_bits=1), BitVector(1, num_bits=1), BitVector(0, num_bits=N)]]  # We hardcode the first ouput
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(1, num_bits=1), output])
    test_vectors.append([BitVector(1, num_bits=1), BitVector(0, num_bits=1), BitVector(0, num_bits=N)])
    test_vectors.append([BitVector(0, num_bits=1), BitVector(1, num_bits=1), BitVector(0, num_bits=N)])

    # We hardcode the first ouput again
    test_vectors.append([BitVector(0, num_bits=1), BitVector(1, num_bits=1), BitVector(0, num_bits=N)])
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(1, num_bits=1), output])

    compileverilator('build/sim_test_register_reset_main.cpp', TestCircuit, test_vectors)
    run_verilator_test('test_register_reset', 'sim_test_register_reset_main', 'test_register_reset')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for clk, reset, expected in test_vectors:
        simulator.set_value(TestCircuit.CLK, scope, clk)
        simulator.set_value(TestCircuit.RESET, scope, reset)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.out, scope) == expected

def test_mux():
    class TestCircuit(Circuit):
        name = "test_mux"
        IO = ["I0", In(Bits(4)), "I1", In(Bits(4)), "sel", In(Bit), "O", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            mux4 = DefineMux(width=4)()
            wire(mux4.in0, circuit.I0)
            wire(mux4.in1, circuit.I1)
            wire(mux4.sel, circuit.sel)
            wire(mux4.out, circuit.O)

    def reference(a, b, sel):
        return b if sel.as_int() else a

    test_vectors = testvectors(TestCircuit, reference)

    compile("build/test_mux", TestCircuit, include_coreir=True)
    compileverilator('build/sim_test_mux_main.cpp', TestCircuit, test_vectors)
    run_verilator_test('test_mux', 'sim_test_mux_main', 'test_mux')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for I0, I1, sel, O in test_vectors:
        simulator.set_value(TestCircuit.I0, scope, I0)
        simulator.set_value(TestCircuit.I1, scope, I1)
        simulator.set_value(TestCircuit.sel, scope, sel)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.O, scope) == O

def test_memory():
    class TestCircuit(Circuit):
        name = "test_mem"
        IO = ["raddr", In(Bits(2)), 
              "waddr", In(Bits(2)), 
              "wdata", In(Bits(4)), 
              "rclk", In(Bit), 
              "ren", In(Bit), 
              "wclk", In(Bit), 
              "wen", In(Bit), 
              "rdata", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            mem = DefineMemory(height=4, width=4)()
            wire(mem.raddr, circuit.raddr)
            wire(mem.rdata, circuit.rdata)
            wire(mem.rclk, circuit.rclk)
            wire(mem.ren, circuit.ren)
            wire(mem.waddr, circuit.waddr)
            wire(mem.wdata, circuit.wdata)
            wire(mem.wclk, circuit.wclk)
            wire(mem.wen, circuit.wen)

    def write_value(value, addr):
        test_vectors = []
        for wclk in [0, 1]:
            test_vectors.append([
                BitVector(0, num_bits=2), # raddr
                BitVector(addr, num_bits=2), # waddr
                BitVector(value, num_bits=4), # wdata
                BitVector(0, num_bits=1), # rclk
                BitVector(0, num_bits=1), # ren
                BitVector(wclk, num_bits=1), # wclk
                BitVector(1, num_bits=1), # wen
                BitVector(0, num_bits=4), # rdata
            ])
        for rclk in [0, 1]:
            test_vectors.append([
                BitVector(addr, num_bits=2), # raddr
                BitVector(0, num_bits=2), # waddr
                BitVector(0, num_bits=4), # wdata
                BitVector(rclk, num_bits=1), # rclk
                BitVector(1, num_bits=1), # ren
                BitVector(0, num_bits=1), # wclk
                BitVector(0, num_bits=1), # wen
                BitVector(value if rclk else 0, num_bits=4), # rdata
            ])
        return test_vectors
    test_vectors = []
    test_vectors.extend(write_value(7, 3))

    compile("build/test_mem", TestCircuit, include_coreir=True)
    compileverilator('build/sim_test_mem_main.cpp', TestCircuit, test_vectors)
    run_verilator_test('test_mem', 'sim_test_mem_main', 'test_mem')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for raddr, waddr, wdata, rclk, ren, wclk, wen, rdata in test_vectors:
        simulator.set_value(TestCircuit.raddr, scope, raddr)
        simulator.set_value(TestCircuit.waddr, scope, waddr)
        simulator.set_value(TestCircuit.wdata, scope, wdata)
        simulator.set_value(TestCircuit.rclk, scope, rclk)
        simulator.set_value(TestCircuit.ren, scope, ren)
        simulator.set_value(TestCircuit.wclk, scope, wclk)
        simulator.set_value(TestCircuit.wen, scope, wen)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.rdata, scope) == rdata


