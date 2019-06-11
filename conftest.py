import pytest
from magma import clear_cachedFunctions
import magma.backend.coreir_


@pytest.fixture(autouse=True)
def magma_test():
    import magma.config
    magma.config.set_compile_dir('callee_file_dir')
    clear_cachedFunctions()
    magma.backend.coreir_.CoreIRContextSingleton().reset_instance()
