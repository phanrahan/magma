from magma import *
from magma.testing import check_files_equal

def test_arg1():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.I, buf.I)
    wire(buf.O, main.O)

    compile("build/arg1", main)
    assert check_files_equal(__file__, "build/arg1.v", "gold/arg1.v")


def test_arg2():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits[2]), "O", Out(Bit))

    a = And2()

    wire( main.I[0], a.I0 )
    wire( main.I[1], a.I1 )
    wire(a.O, main.O)

    compile("build/arg2", main)
    assert check_files_equal(__file__, "build/arg2.v", "gold/arg2.v")

def test_pos():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.I, buf[0])
    wire(buf[1], main.O)

    compile("build/pos", main)
    assert check_files_equal(__file__, "build/pos.v", "gold/pos.v")

def test_arg_array1():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Bits[n]), "O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "O", Out(Bit))

    a = AndN(2)

    wire(array([0,1]), a.I)
    wire(a.O, main.O)

    compile("build/array1", main)
    assert check_files_equal(__file__, "build/array1.v", "gold/array1.v")


def test_arg_array2():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Bits[n]), "O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = AndN(2)

    wire(array([main.I, 1]), a.I)
    wire(a.O, main.O)

    compile("build/array2", main)
    assert check_files_equal(__file__, "build/array2.v", "gold/array2.v")


def test_arg_array3():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Bits[n]), "O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "I", In(Bits[2]), "O", Out(Bit))

    a = AndN(2)

    wire(main.I, a.I)
    wire(a.O, main.O)

    compile("build/array3", main)
    assert check_files_equal(__file__, "build/array3.v", "gold/array3.v")
