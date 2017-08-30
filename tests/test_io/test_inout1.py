from magma import *
from magma.testing import check_files_equal


def test():
    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    wire(main.I, main.O)

    compile("build/inout1", main)
    assert check_files_equal(__file__, "build/inout1.v", "gold/inout1.v")
