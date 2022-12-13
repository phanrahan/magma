import pytest
from magma.config import config as magma_config
from magma.util import reset_global_context


def pytest_configure(config):
    magma_config.compile_dir = 'callee_file_dir'
    magma_config.use_namer_dict = True
    config.use_generator_debug_rewriter = True


@pytest.fixture(autouse=True)
def magma_test():
    reset_global_context()
