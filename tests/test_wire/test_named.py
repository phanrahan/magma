from magma import *
from magma.testing import check_files_equal


def test_named1():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        buf = Buf()
        buf(I=io.I)
        wire(buf.O, io.O)

    compile("build/named1", main, output="verilog")
    assert check_files_equal(__file__, "build/named1.v", "gold/named1.v")

def test_named2():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bit))
        a = And2()

        a(I0=io.I[0], I1=io.I[1])
        wire(a.O, io.O)

    compile("build/named2a", main, output="verilog")
    assert check_files_equal(__file__, "build/named2a.v", "gold/named2a.v")

def test_named3():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bit))
        a = And2()

        a(I0=io.I[0])
        a(I1=io.I[1])
        wire(a.O, io.O)

    compile("build/named2b", main, output="verilog")
    assert check_files_equal(__file__, "build/named2b.v", "gold/named2b.v")


def test_named4():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bit))
        a = And2()

        a(I1=io.I[1])
        a(I0=io.I[0])
        wire(a.O, io.O)

    compile("build/named2c", main, output="verilog")
    assert check_files_equal(__file__, "build/named2c.v", "gold/named2c.v")
