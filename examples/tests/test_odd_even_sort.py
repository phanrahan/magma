import pytest
import tempfile
import itertools
import fault as f
from ..odd_even_sort import (
    Swap, OddEvenSwaps, Permute, riffle, unriffle, OddEvenSorter
)
from hwtypes import BitVector


def test_swap():
    tester = f.Tester(Swap)
    for bits in itertools.product(range(2), repeat=2):
        tester.circuit.I = BitVector[2](bits)
        tester.eval()
        tester.circuit.O.expect(BitVector[2](list(sorted(bits))))
    with tempfile.TemporaryDirectory() as dir:
        tester.compile_and_run('verilator', magma_output="mlir-verilog",
                               directory=dir)


@pytest.mark.parametrize('n', [4, 8, 16])
def test_even_odd_swap(n):
    tester = f.Tester(OddEvenSwaps(n))
    for _ in range(16):
        tester.circuit.I = I = BitVector.random(n)
        tester.eval()
        expected = []
        for i in range(n // 2):
            expected.extend(list(sorted(I.bits()[i * 2:i * 2 + 2])))
        tester.circuit.O.expect(BitVector[n](expected))
    with tempfile.TemporaryDirectory() as dir:
        tester.compile_and_run('verilator', magma_output="mlir-verilog",
                               directory=dir)


@pytest.mark.parametrize('n', [4, 8, 16])
@pytest.mark.parametrize('fn', [riffle, unriffle])
def test_permute(n, fn):
    permutation = fn(n)
    tester = f.Tester(Permute(permutation))
    for i in range(4):
        tester.circuit.I = I = BitVector.random(n)
        tester.eval()
        tester.circuit.O.expect(BitVector[n]([I[i] for i in permutation]))
    with tempfile.TemporaryDirectory() as dir:
        tester.compile_and_run('verilator', magma_output="mlir-verilog",
                               directory=dir)


@pytest.mark.parametrize('n', [4, 8, 16])
def test_even_odd_sorter(n):
    tester = f.Tester(OddEvenSorter(n))
    for _ in range(16):
        tester.circuit.I = I = BitVector.random(n)
        tester.print("I=%x\n", tester.circuit.I)
        tester.eval()
        tester.circuit.O.expect(BitVector[n](list(sorted(I.bits()))))
    with tempfile.TemporaryDirectory() as dir:
        tester.compile_and_run('verilator', magma_output="mlir-verilog",
                               directory=dir)
