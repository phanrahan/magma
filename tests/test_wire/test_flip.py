from magma import *
from magma.testing import check_files_equal

def test_flip():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(O=Out(Bit))
        buf = Buf()

        # flip inputs and outputs
        wire(buf.I, bit(1))
        wire(io.O, buf.O)

    compile("build/flip", main, output="verilog")
    assert check_files_equal(__file__, "build/flip.v", "gold/flip.v")
