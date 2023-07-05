import pytest

import fault
from hwtypes import BitVector, SIntVector

from riscv_mini.alu import ALUSimple, ALUArea, ALUOP


OP_MAP = {
    ALUOP.ADD: lambda x, y: x + y,
    ALUOP.SUB: lambda x, y: x - y,
    ALUOP.AND: lambda x, y: x & y,
    ALUOP.OR: lambda x, y: x | y,
    ALUOP.XOR: lambda x, y: x ^ y,
    ALUOP.SLT: lambda x, y: SIntVector[len(x)](x) < SIntVector[len(x)](y),
    ALUOP.SLL: lambda x, y: x << y,
    ALUOP.SLTU: lambda x, y: x < y,
    ALUOP.SRL: lambda x, y: x >> y,
    ALUOP.SRA: lambda x, y: SIntVector[len(x)](x) >> y,
    ALUOP.COPY_A: lambda x, y: x,
    ALUOP.COPY_B: lambda x, y: y
}


@pytest.mark.parametrize("alu", [ALUSimple, ALUArea])
def test_alu_basic(alu):
    tester = fault.Tester(alu(16))
    for i, (alu_op, py_op) in enumerate(OP_MAP.items()):
        A, B = BitVector.random(16), BitVector.random(16)
        tester.circuit.A = A
        tester.circuit.B = B
        tester.circuit.op = alu_op
        tester.eval()
        tester.circuit.O.expect(py_op(A, B))

    tester.compile_and_run("verilator", flags=["-Wno-unused"],
                           magma_opts={"disallow_local_variables": True,
                                       "check_circt_opt_version": False},
                           magma_output="mlir-verilog")
