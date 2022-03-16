import pytest

import magma as m
from magma.primitives.mux import CoreIRCommonLibMuxN

from examples import (
    simple_aggregates_product, aggregate_mux_wrapper, complex_register_wrapper,
)
from test_utils import get_local_examples, run_test_compile_to_mlir


class _simple_coreir_common_lib_mux_n_wrapper(m.Circuit):
    name = "simple_coreir_common_lib_mux_n_wrapper"
    T = m.Product.from_fields(
        "anon", dict(data=m.Array[8, m.Bits[6]], sel=m.Bits[3])
    )
    io = m.IO(I=m.In(T), O=m.Out(m.Bits[6]))
    io.O @= CoreIRCommonLibMuxN(8, 6)()(io.I)


@pytest.mark.parametrize("ckt", get_local_examples())
def test_compile_to_mlir(ckt):
    run_test_compile_to_mlir(ckt)


@pytest.mark.parametrize(
    "ckt",
    [
        simple_aggregates_product,
        aggregate_mux_wrapper,
        _simple_coreir_common_lib_mux_n_wrapper,
        complex_register_wrapper,
    ]
)
def test_compile_to_mlir_flatten_all_tuples(ckt):
    kwargs = {
        "flatten_all_tuples": True,
        "gold_name": f"{ckt.name}_flatten_all_tuples",
    }
    run_test_compile_to_mlir(ckt, **kwargs)
