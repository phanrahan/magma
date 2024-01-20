import random
import pytest

import fault as f
from hwtypes import BitVector


from ..adder import Adder


@pytest.mark.parametrize("N", [random.randint(1, 16) for _ in range(4)])
def test_adder(N):

    tester = f.Tester(Adder(N))
    tester.circuit.A = A = BitVector.random(N)
    tester.circuit.B = B = BitVector.random(N)
    tester.circuit.CIN = CIN = BitVector.random(1)

    tester.eval()
    tester.circuit.SUM.expect(A + B + CIN.zext(N - 1))
    tester.circuit.COUT.expect((A.zext(1) + B.zext(1) +
                                CIN.zext(N))[-1])
    tester.compile_and_run("verilator", magma_output="mlir-verilog")
