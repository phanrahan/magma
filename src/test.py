import pytest

from magma.testing import check_files_equal

from compile_to_mlir import compile_to_mlir
from examples import *
from test_utils import get_magma_examples


_ckts = [
    simple_comb,
    simple_hierarchy,
    simple_aggregates_bits,
    simple_aggregates_array,
    simple_aggregates_nested_array,
    complex_aggregates_nested_array,
    simple_aggregates_tuple,
    simple_constant,
    aggregate_constant,
    simple_mux_wrapper,
    aggregate_mux_wrapper,
    simple_register_wrapper,
    complex_register_wrapper,
    counter,
    twizzle,
    simple_unused_output,
    feedthrough,
    no_outputs,
    simple_mixed_direction_ports,
    complex_mixed_direction_ports,
    complex_mixed_direction_ports2,
]
_ckts += get_magma_examples()


@pytest.mark.parametrize("ckt", _ckts)
def test_compile_to_mlir(ckt):
    m.passes.clock.WireClockPass(ckt).run()
    filename = f"{ckt.name}.mlir"
    with open(filename, "w") as f:
        compile_to_mlir(ckt, f)
    assert check_files_equal(__file__, filename, f"golds/{filename}")
