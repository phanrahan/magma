import pytest

from magma.config import config as magma_config
from magma.util import reset_global_context


@pytest.fixture(autouse=True)
def riscv_mini_test():
    magma_config.compile_dir = 'normal'
    reset_global_context()
