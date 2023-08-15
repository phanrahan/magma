import os

import magma as m
from magma.config import config as magma_config
from magma.testing.utils import check_gold

from riscv_mini.tile import Tile


def test_riscv_mini_unflattened_tuples():
    magma_config.compile_dir = 'callee_file_dir'
    tile = Tile(32)
    m.compile("build/test_riscv_mini_unflattened_tuples", tile,
              output="mlir-verilog", disallow_local_variables=True,
              disallow_packed_struct_assignments=True)
    assert check_gold(__file__,
                      "test_riscv_mini_unflattened_tuples.v")
    dirname = os.path.dirname(__file__)
    path = f"{dirname}/build/test_riscv_mini_unflattened_tuples.v"
