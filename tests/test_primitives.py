import magma
from magma import In, Out, Bit, UInt, Circuit
from magma.primitives import DefineRegister
from magma.bit_vector import BitVector
from magma.bitutils import int2seq
from magma.verilator.verilator import compile as compileverilator
from magma.verilator.verilator import run_verilator_test
from magma.python_simulator import PythonSimulator
from magma.scope import Scope

from test_expressions import insert_coreir_stdlib_include

def test_register():
    N = 4
    Register4 = DefineRegister(N, T=UInt)
    class TestCircuit(Circuit):
        name = "test_register"
        IO = ["CLK", In(Bit), "out", Out(UInt(N))]
        @classmethod
        def definition(circuit):
            reg = Register4()
            magma.wire(reg.Q, circuit.out)
            magma.wire(reg.D, reg.Q + int2seq(1, N))
            magma.wire(circuit.CLK, reg.clk)

    magma.compile("build/test_register", TestCircuit)
    expected_sequence = [BitVector(x, num_bits=N) for x in range(1, 1 << N)]
    test_vectors = [[BitVector(0, num_bits=1), BitVector(0, num_bits=N)]]  # We hardcode the first ouput
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), output])

    compileverilator('build/sim_test_register_main.cpp', TestCircuit, test_vectors)
    insert_coreir_stdlib_include("build/test_register.v")
    run_verilator_test('test_register', 'sim_test_register_main', 'test_register')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for clk, expected in test_vectors:
        simulator.set_value(TestCircuit.CLK, scope, clk.as_bool_list()[0])
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.out, scope) == expected.as_bool_list()

def test_register_ce():
    N = 4
    Register4 = DefineRegister(N, has_ce=True, T=UInt)
    class TestCircuit(Circuit):
        name = "test_register_ce"
        IO = ["CLK", In(Bit), "CE", In(Bit), "out", Out(UInt(N))]
        @classmethod
        def definition(circuit):
            reg = Register4().when(circuit.CE)
            magma.wire(reg.Q, circuit.out)
            magma.wire(reg.D, reg.Q + int2seq(1, N))
            magma.wire(circuit.CLK, reg.clk)

    magma.compile("build/test_register_ce", TestCircuit)
    expected_sequence = [BitVector(x, num_bits=N) for x in range(1, 1 << N)]
    test_vectors = [[BitVector(0, num_bits=1), BitVector(1, num_bits=1), BitVector(0, num_bits=N)]]  # We hardcode the first ouput
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(1, num_bits=1), output])
        # Should not advance with clock enable low
        test_vectors.append([BitVector(1, num_bits=1), BitVector(0, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(0, num_bits=1), output])

    compileverilator('build/sim_test_register_ce_main.cpp', TestCircuit, test_vectors)
    insert_coreir_stdlib_include("build/test_register_ce.v")
    run_verilator_test('test_register_ce', 'sim_test_register_ce_main', 'test_register_ce')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for clk, enable, expected in test_vectors:
        simulator.set_value(TestCircuit.CLK, scope, clk.as_bool_list()[0])
        simulator.set_value(TestCircuit.CE, scope, enable.as_bool_list()[0])
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.out, scope) == expected.as_bool_list()

def test_register_reset():
    N = 4
    Register4 = DefineRegister(N, has_reset=True, T=UInt)
    class TestCircuit(Circuit):
        name = "test_register_reset"
        IO = ["CLK", In(Bit), "RESET", In(Bit), "out", Out(UInt(N))]
        @classmethod
        def definition(circuit):
            reg = Register4().reset(circuit.RESET)
            magma.wire(reg.Q, circuit.out)
            magma.wire(reg.D, reg.Q + int2seq(1, N))
            magma.wire(circuit.CLK, reg.clk)

    magma.compile("build/test_register_reset", TestCircuit)
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
    insert_coreir_stdlib_include("build/test_register_reset.v")
    run_verilator_test('test_register_reset', 'sim_test_register_reset_main', 'test_register_reset')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for clk, reset, expected in test_vectors:
        simulator.set_value(TestCircuit.CLK, scope, clk.as_bool_list()[0])
        simulator.set_value(TestCircuit.RESET, scope, reset.as_bool_list()[0])
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.out, scope) == expected.as_bool_list()
