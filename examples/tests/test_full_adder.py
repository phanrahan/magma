from full_adder import FullAdder
import fault as f
from hwtypes import BitVector


def test_full_adder():
    tester = f.Tester(FullAdder)
    for _ in range(4):
        tester.circuit.a = a = BitVector.random(1)
        tester.circuit.b = b = BitVector.random(1)

        tester.circuit.cin = cin = BitVector.random(1)
        tester.eval()
        tester.circuit.sum_.expect(a ^ b ^ cin)
        tester.circuit.cout.expect((a & b) | (b & cin) | (a & cin))

    tester.compile_and_run("verilator", magma_output="mlir-verilog")
