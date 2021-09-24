import pytest

from magma.testing import check_files_equal

from compile_to_mlir import compile_to_mlir
from examples import *


_ckts = [
    comb,
    simple_hierarchy,
    simple_aggregates_bits,
    simple_aggregates_array,
    simple_aggregates_nested_array,
    complex_aggregates_nested_array,
    simple_aggregates_tuple,
    simple_constant,
    aggregate_constant,
    simple_mux,
    aggregate_mux,
    #simple_register,
    complex_register,
]


@pytest.mark.parametrize("ckt", _ckts)
def test_compile_to_mlir(ckt):
    filename = f"{ckt.name}.mlir"
    with open(filename, "w") as f:
        compile_to_mlir(ckt, f)
    assert check_files_equal(__file__, filename, f"golds/{filename}")
