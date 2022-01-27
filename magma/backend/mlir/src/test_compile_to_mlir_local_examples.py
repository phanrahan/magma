import pytest

from test_utils import get_local_examples, run_test_compile_to_mlir


@pytest.mark.parametrize("ckt", get_local_examples())
def test_compile_to_mlir(ckt):
    run_test_compile_to_mlir(ckt)
