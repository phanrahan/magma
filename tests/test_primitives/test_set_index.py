import os
import pytest

from hwtypes import BitVector, Bit
import fault

import magma as m
from magma.config import config as magma_config


@pytest.fixture(autouse=True)
def test_dir():
    magma_config.compile_dir = 'normal'
    yield
    magma_config.compile_dir = 'callee_file_dir'


def test_set_index():
    class test_set_index(m.Circuit):
        io = m.IO(I=m.In(m.Bits[4]),
                  val=m.In(m.Bit),
                  idx=m.In(m.UInt[2]),
                  O=m.Out(m.Bits[4]))
        io.O @= m.set_index(io.I, io.val, io.idx)

    tester = fault.Tester(test_set_index)
    for i in range(5):
        tester.circuit.I = I = BitVector.random(4)
        tester.circuit.val = val = Bit.random()
        tester.circuit.idx = idx = BitVector.random(2)
        tester.eval()
        I[int(idx)] = val
        tester.circuit.O.expect(I)

    tester.compile_and_run("verilator", tmp_dir=True, flags=["-Wno-unused"])


def test_set_index_array():
    class test_set_index_array(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bits[4]]),
                  val=m.In(m.Bits[4]),
                  idx=m.In(m.UInt[1]),
                  O=m.Out(m.Array[2, m.Bits[4]]))
        io.O @= m.set_index(io.I, io.val, io.idx)

    tester = fault.Tester(test_set_index_array)
    for i in range(5):
        tester.circuit.I = I = [BitVector.random(4), BitVector.random(4)]
        tester.circuit.val = val = BitVector.random(4)
        tester.circuit.idx = idx = BitVector.random(1)
        tester.eval()
        I[int(idx)] = val
        tester.circuit.O.expect(I)

    tester.compile_and_run("verilator", tmp_dir=True, flags=["-Wno-unused"])


def test_set_ndindex_array():
    class test_set_ndindex_array(m.Circuit):
        io = m.IO(I=m.In(m.Array[(2, 4, 8), m.Bits[4]]),
            val=m.In(m.Bits[4]),
            idx_z=m.In(m.UInt[1]),
            idx_y=m.In(m.UInt[2]),
            idx_x=m.In(m.UInt[3]),
            O=m.Out(m.Array[(2, 4, 8), m.Bits[4]]))
        io.O @= m.set_index(io.I, io.val, [io.idx_z, io.idx_y, io.idx_x])

    tester = fault.Tester(test_set_ndindex_array)
    for i in range(5):
        tester.circuit.I = I = [
            [[BitVector.random(4) for _ in range(8)] for _ in range(4)]
            for _ in range(2)
        ]
        tester.circuit.val = val = BitVector.random(4)
        tester.circuit.idx_z = idx_z = BitVector.random(1)
        tester.circuit.idx_y = idx_y = BitVector.random(2)
        tester.circuit.idx_x = idx_x = BitVector.random(3)
        I[int(idx_z)][int(idx_y)][int(idx_x)] = val
        tester.eval()
        tester.circuit.O.expect(I)

    tester.compile_and_run("verilator", tmp_dir=True, flags=["-Wno-unused"])
