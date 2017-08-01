import magma
from magma import In, Out, Bit, UInt, Circuit
from magma.primitives import DefineRegister
from magma.bit_vector import BitVector
from magma.verilator.verilator import compile as compileverilator
from magma.verilator.verilator import run_verilator_test

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
            magma.wire(reg.D, reg.Q + magma.int2seq(1, N))
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

def test_register_clock_enable():
    N = 4
    Register4 = DefineRegister(N, clock_enable=True, T=UInt)
    class TestCircuit(Circuit):
        name = "test_register"
        IO = ["CLK", In(Bit), "CE", In(Bit), "out", Out(UInt(N))]
        @classmethod
        def definition(circuit):
            reg = Register4()
            magma.wire(reg.Q, circuit.out)
            magma.wire(reg.D, reg.Q + magma.int2seq(1, N))
            magma.wire(circuit.CLK, reg.clk)
            magma.wire(circuit.CE, reg.en)

    magma.compile("build/test_register", TestCircuit)
    expected_sequence = [BitVector(x, num_bits=N) for x in range(1, 1 << N)]
    test_vectors = [[BitVector(0, num_bits=1), BitVector(1, num_bits=1), BitVector(0, num_bits=N)]]  # We hardcode the first ouput
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(1, num_bits=1), output])
        # Should not advance with clock enable low
        test_vectors.append([BitVector(1, num_bits=1), BitVector(0, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(0, num_bits=1), output])

    compileverilator('build/sim_test_register_main.cpp', TestCircuit, test_vectors)
    insert_coreir_stdlib_include("build/test_register.v")
    run_verilator_test('test_register', 'sim_test_register_main', 'test_register')
