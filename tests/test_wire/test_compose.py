import sys
from magma import *


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit)) 

    buf1 = Buf()
    buf2 = Buf()

    buf1(main.I)
    buf2(buf1)
    wire(buf2, main.O)

    compile("build/compose", main)
    assert magma_check_files_equal(__file__, "build/compose.v", "gold/compose.v")

