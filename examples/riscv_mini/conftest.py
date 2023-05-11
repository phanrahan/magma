import pytest

from magma.util import reset_global_context


@pytest.fixture(autouse=True)
def magma_test():
    reset_global_context()
