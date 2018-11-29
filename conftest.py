import pytest
from magma.circuit import magma_clear_circuit_database
from magma import clear_cachedFunctions
import magma.backend.coreir_


@pytest.fixture(autouse=True)
def magma_test():
    import magma.config
    magma.config.set_compile_dir('callee_file_dir')
    magma_clear_circuit_database()
    clear_cachedFunctions()
    magma.backend.coreir_.__reset_context()
