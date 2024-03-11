from ..full_adder import FullAdder
import fault as f


def test_full_adder():
    tester = f.Tester(FullAdder)
    for a in range(2):
        for b in range(2):
            for cin in range(2):
                tester.circuit.a = a
                tester.circuit.b = b
                tester.circuit.cin = cin
                tester.eval()
                tester.circuit.sum_.expect((a + b + cin) % 2)
                tester.circuit.cout.expect((a + b + cin) >= 2)

    tester.compile_and_run("verilator", magma_output="mlir-verilog")
