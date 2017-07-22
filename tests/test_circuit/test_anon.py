import sys
from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Array2), "O", Out(Bit))

    def AndN2():
        and2 = And2()
        return AnonymousCircuit("I", array(and2.I0, and2.I1), "O", and2.O)

    and2 = AndN2()

    wire(and2(main.I),main.O)

    compile("build/anon", main)
    assert magma_check_files_equal(__file__, "build/anon.v", "gold/anon.v")
