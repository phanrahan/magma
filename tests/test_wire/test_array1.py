import sys
from magma import *

def test():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Array(n, Bit)), "output O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "O", Out(Bit))

    a = AndN(2)

    wire(array([0,1]), a.I)
    wire(a.O, main.O)

    compile("build/array1", main)
    assert magma_check_files_equal(__file__, "build/array1.v", "gold/array1.v")
