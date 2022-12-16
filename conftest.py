import pytest
from magma.config import config as magma_config
from magma.util import reset_global_context


def pytest_configure(config):
    magma_config.compile_dir = 'callee_file_dir'
    # TODO: Enable this globally for testing
    # revert a3a2452168f2251277a14548d053a9ca7a45bff7 for golds
    # magma_config.use_namer_dict = True


@pytest.fixture(autouse=True)
def magma_test():
    reset_global_context()
