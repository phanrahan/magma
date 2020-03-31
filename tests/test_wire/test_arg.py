from magma import *
from magma.testing import check_files_equal


def DefineAndN(n):
    name_ = 'AndN%d' % n

    class _Circuit(Circuit):
        name = name_
        io = IO(I=In(Bits[n]), O=Out(Bit))

    return _Circuit


def AndN(n):
    return DefineAndN(n)()


def test_arg1():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        buf = Buf()
        wire(io.I, buf.I)
        wire(buf.O, io.O)

    compile("build/arg1", main, output="verilog")
    assert check_files_equal(__file__, "build/arg1.v", "gold/arg1.v")


def test_arg2():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bit))
        a = And2()

        wire( io.I[0], a.I0 )
        wire( io.I[1], a.I1 )
        wire(a.O, io.O)

    compile("build/arg2", main, output="verilog")
    assert check_files_equal(__file__, "build/arg2.v", "gold/arg2.v")


def test_pos():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        buf = Buf()
        wire(io.I, buf[0])
        wire(buf[1], io.O)

    compile("build/pos", main, output="verilog")
    assert check_files_equal(__file__, "build/pos.v", "gold/pos.v")


def test_pos_slice():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bits[2]))

    class main(Circuit):
        name = "main"
        io = IO(I=In(Array[2, Bit]), O=Out(Bit))
        buf = Buf()
        wire(array(buf[0:2]), io.I)
        wire(buf.O, io.O)

    compile("build/pos_slice", main, output="verilog")
    assert check_files_equal(__file__, "build/pos.v", "gold/pos.v")


def test_arg_array1():
    def AndN(n):
        return DefineAndN(n)()

    class main(Circuit):
        name = "main"
        io = IO(O=Out(Bit))
        a = AndN(2)

        wire(array([0,1]), a.I)
        wire(a.O, io.O)

    compile("build/array1", main, output="verilog")
    assert check_files_equal(__file__, "build/array1.v", "gold/array1.v")


def test_arg_array2():
    class main(Circuit):
        name = "main"
        io = IO(I=In(Bit), O=Out(Bit))
        a = AndN(2)

        wire(array([io.I, 1]), a.I)
        wire(a.O, io.O)

    compile("build/array2", main, output="verilog")
    assert check_files_equal(__file__, "build/array2.v", "gold/array2.v")


def test_arg_array3():
    class main(Circuit):
        name = "main"
        io = IO(I=In(Bits[2]), O=Out(Bit))
        a = AndN(2)

        wire(io.I, a.I)
        wire(a.O, io.O)

    compile("build/array3", main, output="verilog")
    assert check_files_equal(__file__, "build/array3.v", "gold/array3.v")
