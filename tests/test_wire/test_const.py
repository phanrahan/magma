from magma import *
from magma.testing import check_files_equal
import pytest


def test_const0():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(O=Out(Bit))
        buf = Buf()

        wire(0, buf.I)
        wire(buf.O, io.O)

    compile("build/const0", main)
    assert check_files_equal(__file__, "build/const0.v", "gold/const0.v")


def test_const1():
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(Bit), O=Out(Bit))

    class main(Circuit):
        name = "main"
        io = IO(O=Out(Bit))
        buf = Buf()

        wire(1, buf.I)
        wire(buf.O, io.O)

    compile("build/const1", main)
    assert check_files_equal(__file__, "build/const1.v", "gold/const1.v")




@pytest.mark.parametrize('T', [Bits, UInt, SInt])
@pytest.mark.parametrize('N', range(1, 4))
def test_const_bits(T, N):
    class Buf(Circuit):
        name = "Buf"
        io = IO(I=In(T[N]), O=Out(T[N]))

    class main(Circuit):
        name = "main"
        io = IO(O=Out(T[N]))
        buf = Buf()

        wire(1, buf.I)
        wire(buf.O, io.O)

    compile(f"build/const_bits_{T.__name__}_{N}", main)
    assert check_files_equal(__file__, f"build/const_bits_{T.__name__}_{N}.v",
                             f"gold/const_bits_{T.__name__}_{N}.v")
