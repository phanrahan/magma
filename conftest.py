import pytest
from magma import clear_cachedFunctions
from magma.when import reset_context
import magma.config


@pytest.fixture(autouse=True)
def magma_test():
    # TODO: We should provide a top-level "reset_magma" API for testing
    magma.config.set_compile_dir('callee_file_dir')
    clear_cachedFunctions()
    magma.frontend.coreir_.ResetCoreIR()
    magma.generator.reset_generator_cache()
    magma.logging.flush_all()  # flush all staged logs
    reset_context()
