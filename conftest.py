from pathlib import Path
import pytest
from magma.config import config as magma_config
from magma.util import reset_global_context


def pytest_configure(config):
    magma_config.compile_dir = 'callee_file_dir'
    # TODO(leonardt): Enable this globally for testing
    # Revert a3a2452168f2251277a14548d053a9ca7a45bff7 for golds.
    #
    # magma_config.use_namer_dict = True
    magma_config.use_uinspect = True


@pytest.fixture(autouse=True)
def magma_test():
    reset_global_context()


def pytest_ignore_collect(path, config):
    try:
        import coreir
    except ImportError:
        here = Path.cwd().absolute()
        skip_fd = here / "tests/test_coreir/"
        skip_fd = here / "tests/test_syntax/"
        skip_fd = here / "tests/test_coroutine/"
        if skip_fd == path:
            return True
