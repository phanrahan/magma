import magma as m

import sys
import os

TEST_SYNTAX_PATH = os.path.join(os.path.dirname(__file__), '../test_syntax')

sys.path.append(TEST_SYNTAX_PATH)

from test_combinational import compile_and_check


def test_562():
    BV1 = m.Bits[1]

    @m.sequential2()
    class A:
        def __call__(self, a: m.Bit, b: m.Bits[2]) -> m.Bits[1]:
            return a.ite(BV1(a), b[0:1])
    compile_and_check("test_562", A, "coreir-verilog")
