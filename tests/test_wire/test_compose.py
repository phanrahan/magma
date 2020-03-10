from magma import *
from magma.testing import check_files_equal


def test():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        buf1 = Buf()
        buf2 = Buf()

        buf1(io.I)
        buf2(buf1)
        wire(buf2, io.O)

    compile("build/compose", main, output="verilog")
    assert check_files_equal(__file__, "build/compose.v", "gold/compose.v")

