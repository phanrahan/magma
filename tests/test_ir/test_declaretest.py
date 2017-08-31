from magma import *
from magma.testing import check_files_equal

def test():
    # Clear the circuit cache from any other test cases
    import magma.circuit
    magma.circuit.__magma_clear_circuit_cache()
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit)) 

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    inst0 = And2()
    wire(main.I0, inst0.I0)
    wire(main.I1, inst0.I1)
    wire(inst0.O, main.O)
    EndCircuit()

    compile("build/declaretest", main)
    assert check_files_equal(__file__, "build/declaretest.v", "gold/declaretest.v")
