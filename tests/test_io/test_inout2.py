from magma import *
from magma.testing import check_files_equal


def test():
    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bits[2]))
        wire(io.I, io.O)

    compile("build/inout2", main)
    assert check_files_equal(__file__, "build/inout2.v", "gold/inout2.v")
