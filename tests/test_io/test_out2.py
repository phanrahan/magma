from magma import *
from magma.testing import check_files_equal


def test():
    class main(Circuit):
        name = "main"
        io = IO(O=Out(Bits[2]))
        wire(array([0,1]), io.O)

    compile("build/out2", main, output="verilog")
    assert check_files_equal(__file__, "build/out2.v", "gold/out2.v")
