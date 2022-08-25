import itertools
import pytest

import magma as m
from magma.primitives.mux import CoreIRCommonLibMuxN
from magma.uniquification import uniquification_pass, reset_names

from examples import (
    simple_aggregates_product,
    aggregate_mux_wrapper,
    non_power_of_two_mux_wrapper,
    complex_register_wrapper,
    complex_bind,
    simple_comb,
    simple_register_wrapper,
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
    kwargs = {
        "use_native_bind_processor": True,
        "basename": ckt.name,
    }
    run_test_compile_to_mlir(ckt, **kwargs)


@pytest.mark.parametrize(
    "ckt",
    [
        simple_aggregates_product,
        aggregate_mux_wrapper,
        _simple_coreir_common_lib_mux_n_wrapper,
        complex_register_wrapper,
        complex_bind,
    ]
)
def test_compile_to_mlir_flatten_all_tuples(ckt):
    kwargs = {
        "flatten_all_tuples": True,
        "use_native_bind_processor": True,
        "gold_name": f"{ckt.name}_flatten_all_tuples",
        "basename": ckt.name,
    }
    run_test_compile_to_mlir(ckt, **kwargs)


@pytest.mark.parametrize("ckt", [simple_comb])
def test_compile_to_mlir_verilog_prefix(ckt):
    kwargs = {
        "verilog_prefix": "proj_",
        "gold_name": f"{ckt.name}_verilog_prefix",
        "basename": ckt.name,
    }
    run_test_compile_to_mlir(ckt, **kwargs)


@pytest.mark.parametrize(
    "ckt",
    [
        simple_register_wrapper,
        complex_register_wrapper,
    ]
)
def test_compile_to_mlir_disable_initial_blocks(ckt):
    kwargs = {
        "disable_initial_blocks": True,
        "gold_name": f"{ckt.name}_disable_initial_blocks",
        "basename": ckt.name,
    }
    run_test_compile_to_mlir(ckt, **kwargs)


@pytest.mark.parametrize(
    "ckt",
    [
        simple_register_wrapper,
        complex_register_wrapper,
    ]
)
def test_compile_to_mlir_elaborate_magma_registers(ckt):
    kwargs = {
        "elaborate_magma_registers": True,
        "gold_name": f"{ckt.name}_elaborate_magma_registers",
        "basename": ckt.name,
    }
    names = uniquification_pass(ckt, "UNIQUIFY")
    run_test_compile_to_mlir(ckt, **kwargs)
    reset_names(names)


@pytest.mark.parametrize(
    "ckt,flatten_all_tuples",
    itertools.product(
        [aggregate_mux_wrapper, non_power_of_two_mux_wrapper],
        (True, False),
    )
)
def test_compile_to_mlir_extend_non_power_of_two_muxes(
        ckt, flatten_all_tuples: bool):
    gold_name = f"{ckt.name}_extend_non_power_of_two_muxes"
    if flatten_all_tuples:
        gold_name += "_flatten_all_tuples"
    kwargs = {
        "extend_non_power_of_two_muxes": True,
        "flatten_all_tuples": flatten_all_tuples,
        "gold_name": gold_name,
    }
    run_test_compile_to_mlir(ckt, **kwargs)
