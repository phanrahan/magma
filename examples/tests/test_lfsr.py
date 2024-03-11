from ..lfsr import LFSR
import fault as f
import magma as m
from pylfsr import LFSR as PYLFSR


def test_lfsr():
    py_lfsr = PYLFSR(fpoly=[5, 3], initstate=[0, 0, 0, 1, 0])
    tester = f.SynchronousTester(LFSR(5, init=tuple(py_lfsr.state)))
    for i in range(2 ** 5):
        tester.advance_cycle()
        py_lfsr.next()
        tester.circuit.O.expect(m.bitutils.seq2int(tuple(py_lfsr.state)))
    tester.compile_and_run('verilator', magma_output="mlir-verilog")
