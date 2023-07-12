from riscv_mini.core import Core
import magma as m
from magma.config import config as magma_config
from magma.testing.utils import check_gold


def test_riscv_mini_unflattened_tuples():
    magma_config.compile_dir = 'callee_file_dir'
    core = Core(32)
    m.compile("build/test_riscv_mini_unflattened_tuples", core,
              output="mlir-verilog", disallow_local_variables=True)
    assert check_gold(__file__,
                      "test_riscv_mini_unflattened_tuples.v")
