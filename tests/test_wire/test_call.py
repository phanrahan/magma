from magma import *
from magma.testing import check_files_equal


def test_call1():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))
        a = And2()

        a( io.I0, io.I1 )
        wire(a, io.O)

    compile("build/call1", main, output="verilog")
    assert check_files_equal(__file__, "build/call1.v", "gold/call1.v")


def test_call2():
    def DefineAndN(n):
        name_ = 'AndN%d' % n

        class _Circuit(Circuit):
            name = name_
            io = IO(I=In(Bits[n]), O=Out(Bit))

        return _Circuit

    def AndN(n):
        return DefineAndN(n)()

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bit))
        a = AndN(2)

        a( io.I )
        wire(a, io.O)

    compile("build/call2", main, output="verilog")
    assert check_files_equal(__file__, "build/call2.v", "gold/call2.v")
