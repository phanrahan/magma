from magma import *
from magma.testing import check_files_equal

def test():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))
        inst0 = And2()
        wire(io.I0, inst0.I0)
        wire(io.I1, inst0.I1)
        wire(inst0.O, io.O)

    compile("build/declaretest", main, output="verilog")
    assert check_files_equal(__file__, "build/declaretest.v", "gold/declaretest.v")
