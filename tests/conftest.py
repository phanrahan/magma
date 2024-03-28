from magma.config import config as magma_config
import pytest


def pytest_configure(config):
    magma_config.compile_dir = 'callee_file_dir'
    # TODO(leonardt): Enable this globally for testing
    # Revert a3a2452168f2251277a14548d053a9ca7a45bff7 for golds.
    #
    # magma_config.use_namer_dict = True
    magma_config.use_uinspect = True


@pytest.fixture
def use_namer_dict():
    magma_config.use_namer_dict = True
    yield
    magma_config.use_namer_dict = False
