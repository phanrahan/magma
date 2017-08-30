from magma import *
from magma.testing import check_files_equal


def test():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Bits(n)), "O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = AndN(2)

    wire(main.I, a.I)
    wire(a.O, main.O)

    compile("build/array3", main)
    assert check_files_equal(__file__, "build/array3.v", "gold/array3.v")
