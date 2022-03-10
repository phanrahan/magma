import pytest

from examples import simple_aggregates_product, aggregate_mux_wrapper
from test_utils import get_local_examples, run_test_compile_to_mlir


@pytest.mark.parametrize("ckt", get_local_examples())
def test_compile_to_mlir(ckt):
    run_test_compile_to_mlir(ckt)


@pytest.mark.parametrize(
    "ckt",
    [
        simple_aggregates_product,
        aggregate_mux_wrapper,
    ]
)
def test_compile_to_mlir_flatten_all_tuples(ckt):
    kwargs = {
        "flatten_all_tuples": True,
        "gold_name": f"{ckt.name}_flattened_tuples",
    }
    run_test_compile_to_mlir(ckt, **kwargs)
