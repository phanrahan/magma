import magma as m
from magma import combinational2
from magma.testing import check_files_equal


def test_combinational2_basic_if():
    # TODO: ast_tools/ast_tools/passes/util.py:64: AssertionError
    # can't use 
    # @m.combinational2
    @combinational2
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            return I[0]
        else:
            return I[1]

    m.compile("build/test_combinational2_basic_if", basic_if)
    assert check_files_equal(__file__, f"build/test_combinational2_basic_if.v",
                             f"gold/test_combinational2_basic_if.v")
