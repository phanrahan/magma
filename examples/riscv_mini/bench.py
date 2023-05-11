"""
when:
Benchmark 1: python bench.py
  Time (mean ± σ):      4.100 s ±  0.233 s    [User: 3.753 s, System: 0.212 s]
  Range (min … max):    3.822 s …  4.365 s    10 runs

master:
Benchmark 1: python bench.py
  Time (mean ± σ):     15.013 s ±  0.926 s    [User: 14.841 s, System: 0.538 s]
  Range (min … max):   13.907 s … 16.696 s    10 runs
"""
import magma as m
from riscv_mini.core import Core


core = Core(32)
m.compile("build/Core", core, output="mlir-verilog", flatten_all_tuples=True)
