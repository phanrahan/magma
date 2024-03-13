import fault as f
from ..even_odd_sort import Swap
from hwtypes import BitVector


def swap(I: BitVector[2]):
    return BitVector[2]([I[0] & I[1], I[0] | I[1]])


def test_swap():
    tester = f.Tester(Swap)
    for i in range(2):
        for j in range(2):
            tester.circuit.I = I = BitVector[2]([i, j])
            tester.eval()
            tester.circuit.O.expect(swap(I))
    tester.compile_and_run('verilator', magma_output="mlir-verilog")
