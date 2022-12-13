import pytest
import magma.config
from magma.config import config
from magma.util import reset_global_context


@pytest.fixture(autouse=True)
def magma_test():
    config.use_namer_dict = True
    magma.config.set_compile_dir('callee_file_dir')
    reset_global_context()
