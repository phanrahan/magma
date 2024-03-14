import pytest
import tempfile
import itertools
import fault as f
from ..even_odd_sort import Swap, EvenOddSwaps, Permute, riffle, unriffle
from hwtypes import BitVector


def test_swap():
    tester = f.Tester(Swap)
    for bits in itertools.product(range(2), repeat=2):
        tester.circuit.I = I = BitVector[2](bits)
        tester.eval()
        tester.circuit.O.expect(BitVector[2](list(sorted(bits))))
    with tempfile.TemporaryDirectory() as dir:
        tester.compile_and_run('verilator', magma_output="mlir-verilog",
                               directory=dir)


@pytest.mark.parametrize('n', [4, 8, 16])
def test_even_odd_swap(n):
    tester = f.Tester(EvenOddSwaps(n))
    for bits in itertools.islice(itertools.product(range(2), repeat=n), 16):
        tester.circuit.I = I = BitVector[n](bits)
        tester.eval()
        expected = []
        for i in range(n // 2):
            expected.extend(list(sorted(bits[i * 2:i * 2 + 2])))
        tester.circuit.O.expect(BitVector[n](expected))
    with tempfile.TemporaryDirectory() as dir:
        tester.compile_and_run('verilator', magma_output="mlir-verilog",
                               directory=dir)


@pytest.mark.parametrize('n', [4, 8, 16])
@pytest.mark.parametrize('fn', [riffle, unriffle])
def test_permute(n, fn):
    permutation = fn(n)
    tester = f.Tester(Permute(tuple(permutation)))
    for i in range(4):
        tester.circuit.I = I = BitVector.random(n)
        tester.eval()
        tester.circuit.O.expect(BitVector[n]([I[i] for i in permutation]))
    with tempfile.TemporaryDirectory() as dir:
        tester.compile_and_run('verilator', magma_output="mlir-verilog",
                               directory=dir)
