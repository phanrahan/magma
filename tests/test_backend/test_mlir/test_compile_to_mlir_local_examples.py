import pytest

from examples import simple_aggregates_product
from test_utils import get_local_examples, run_test_compile_to_mlir


@pytest.mark.parametrize("ckt", get_local_examples())
def test_compile_to_mlir(ckt):
    run_test_compile_to_mlir(ckt)


def test_compile_to_mlir_flatten_all_tuples():
    run_test_compile_to_mlir(
        simple_aggregates_product, flatten_all_tuples=True,
        gold_name="simple_aggregates_product_flattened_tuples")
