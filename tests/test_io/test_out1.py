from magma import *
from magma.testing import check_files_equal


def test():
    main = DefineCircuit("main", "O", Out(Bit))

    wire(1, main.O)

    compile("build/out1", main, output="verilog")
    assert check_files_equal(__file__, "build/out1.v", "gold/out1.v")
