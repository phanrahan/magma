from magma import In, Out, Bit, UInt, Circuit, Bits, wire, compile
from magma.primitives import DefineRegister, DefineMux
from magma.bit_vector import BitVector
from magma.bitutils import int2seq
from magma.verilator.verilator import compile as compileverilator
from magma.verilator.verilator import run_verilator_test
from magma.verilator.function import testvectors
from magma.python_simulator import PythonSimulator
from magma.scope import Scope
from magma.verilator.function import testvectors

from test_expressions import insert_coreir_include

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
            wire(getattr(reg, "in"), reg.out + int2seq(1, N))
            wire(circuit.CLK, reg.clk)

    compile("build/test_register", TestCircuit)
    expected_sequence = [BitVector(x, num_bits=N) for x in range(1, 1 << N)]
    test_vectors = [[BitVector(0, num_bits=1), BitVector(0, num_bits=N)]]  # We hardcode the first ouput
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), output])

    compileverilator('build/sim_test_register_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_register.v")
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
            wire(getattr(reg, "in"), reg.out + int2seq(1, N))
            wire(circuit.CLK, reg.clk)

    compile("build/test_register_ce", TestCircuit)
    expected_sequence = [BitVector(x, num_bits=N) for x in range(1, 1 << N)]
    test_vectors = [[BitVector(0, num_bits=1), BitVector(1, num_bits=1), BitVector(0, num_bits=N)]]  # We hardcode the first ouput
    for output in expected_sequence:
        test_vectors.append([BitVector(1, num_bits=1), BitVector(1, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(1, num_bits=1), output])
        # Should not advance with clock enable low
        test_vectors.append([BitVector(1, num_bits=1), BitVector(0, num_bits=1), output])
        test_vectors.append([BitVector(0, num_bits=1), BitVector(0, num_bits=1), output])

    compileverilator('build/sim_test_register_ce_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_register_ce.v")
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
            wire(getattr(reg, "in"), reg.out + int2seq(1, N))
            wire(circuit.CLK, reg.clk)

    compile("build/test_register_reset", TestCircuit)
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
    insert_coreir_include("build/test_register_reset.v")
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
            mux4 = DefineMux(4)()
            wire(mux4.in0, circuit.I0)
            wire(mux4.in1, circuit.I1)
            wire(mux4.sel, circuit.sel)
            wire(mux4.out, circuit.O)

    def reference(a, b, sel):
        return b if sel.as_int() else a

    test_vectors = testvectors(TestCircuit, reference)

    compile("build/test_mux", TestCircuit)
    compileverilator('build/sim_test_mux_main.cpp', TestCircuit, test_vectors)
    insert_coreir_include("build/test_mux.v")
    run_verilator_test('test_mux', 'sim_test_mux_main', 'test_mux')

    simulator = PythonSimulator(TestCircuit)
    scope = Scope()
    for I0, I1, sel, O in test_vectors:
        simulator.set_value(TestCircuit.I0, scope, I0)
        simulator.set_value(TestCircuit.I1, scope, I1)
        simulator.set_value(TestCircuit.sel, scope, sel)
        simulator.evaluate()
        assert simulator.get_value(TestCircuit.O, scope) == O


