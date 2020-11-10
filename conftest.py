import pytest
from magma import clear_cachedFunctions
import magma


@pytest.fixture(autouse=True)
def magma_test():
    import magma.config
    magma.config.set_compile_dir('callee_file_dir')
    clear_cachedFunctions()
    magma.frontend.coreir_.ResetCoreIR()
    magma.generator.reset_generator_cache()
