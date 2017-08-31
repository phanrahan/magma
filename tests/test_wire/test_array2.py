from magma import *
from magma.testing import check_files_equal


def test():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Bits(n)), "O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    a = AndN(2)

    wire(array([main.I, 1]), a.I)
    wire(a.O, main.O)

    compile("build/array2", main)
    assert check_files_equal(__file__, "build/array2.v", "gold/array2.v")
