import pytest
from magma.circuit import magma_clear_circuit_cache


@pytest.fixture(autouse=True)
def magma_test():
    import magma.config
    magma.config.set_compile_dir('callee_file_dir')
    magma_clear_circuit_cache()
