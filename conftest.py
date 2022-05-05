import pytest
from magma import clear_cachedFunctions
import magma
from magma.when import reset_context


@pytest.fixture(autouse=True)
def magma_test():
    import magma.config
    magma.config.set_compile_dir('callee_file_dir')
    clear_cachedFunctions()
    magma.frontend.coreir_.ResetCoreIR()
    magma.generator.reset_generator_cache()
    magma.logging.flush_all()  # flush all staged logs
    reset_context()
