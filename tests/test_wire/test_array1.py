from magma import *
from magma.testing import check_files_equal

def test():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Bits(n)), "O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "O", Out(Bit))

    a = AndN(2)

    wire(array([0,1]), a.I)
    wire(a.O, main.O)

    compile("build/array1", main)
    assert check_files_equal(__file__, "build/array1.v", "gold/array1.v")
