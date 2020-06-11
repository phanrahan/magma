import magma as m
from magma.testing import check_files_equal


def test_combinational2_basic_if():
    @m.combinational2
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            return I[0]
        else:
            return I[1]

    m.compile("build/test_combinational2_basic_if", basic_if)
    assert check_files_equal(__file__, f"build/test_combinational2_basic_if.v",
                             f"gold/test_combinational2_basic_if.v")
