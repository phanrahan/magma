import sys
from magma import *


def test():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Array(n, Bit)), "O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "I", In(Array2), "O", Out(Bit))

    a = AndN(2)

    wire(main.I, a.I)
    wire(a.O, main.O)

    compile("build/array3", main)
    assert magma_check_files_equal(__file__, "build/array3.v", "gold/array3.v")
