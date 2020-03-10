from magma import *
from magma.testing import check_files_equal


def test():
    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        wire(io.I, io.O)

    compile("build/inout1", main, output="verilog")
    assert check_files_equal(__file__, "build/inout1.v", "gold/inout1.v")
