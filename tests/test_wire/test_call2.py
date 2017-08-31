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

    a( main.I )
    wire(a, main.O)

    compile("build/call2", main)
    assert check_files_equal(__file__, "build/call2.v", "gold/call2.v")
