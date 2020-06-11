from hwtypes import BitVector, Bit

import magma as m
from magma.testing import check_files_equal


def test_combinational2_basic_if():
    @m.combinational2
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            return I[0]
        else:
            return I[1]

    class Main(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= basic_if(io.I, io.S)

    m.compile("build/test_combinational2_basic_if", Main)
    assert check_files_equal(__file__, f"build/test_combinational2_basic_if.v",
                             f"gold/test_combinational2_basic_if.v")

    # Test function call interface for python values
    assert basic_if(BitVector[2](2), Bit(0)) == 1
    assert basic_if(BitVector[2](2), Bit(1)) == 0
