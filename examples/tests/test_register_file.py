import random
import pytest

from ..register_file import RegisterFile

import magma as m
import fault as f
from hwtypes import BitVector


@pytest.mark.parametrize('has_read_enable', [True, False])
def test_register_file(has_read_enable):
    tester = f.SynchronousTester(RegisterFile(4, m.Bits[4], has_read_enable))
    data = [BitVector.random(4) for _ in range(4)]
    for i in random.sample(range(4), 4):
        tester.circuit.waddr = i
        tester.circuit.wdata = data[i]
        tester.circuit.wen = 1
        tester.advance_cycle()
    tester.circuit.wen = 0
    for i in random.sample(range(4), 4):
        tester.circuit.raddr = i
        if has_read_enable:
            tester.circuit.ren = 1
        tester.advance_cycle()
        tester.circuit.rdata.expect(data[i])
    tester.compile_and_run("verilator", magma_output="mlir-verilog", flags=['-Wno-UNUSED'])
