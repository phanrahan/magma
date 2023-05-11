import magma as m
from riscv_mini.alu import ALUSimple


alu = ALUSimple(32)
m.compile("build/ALU", alu, output="mlir-verilog", flatten_all_tuples=True)
