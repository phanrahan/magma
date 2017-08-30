from magma import *
from magma.testing import check_files_equal


def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    a = And2()

    a( main.I0, main.I1 )
    wire(a, main.O)

    compile("build/call1", main)
    assert check_files_equal(__file__, "build/call1.v", "gold/call1.v")
