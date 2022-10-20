import contextlib
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
    # NOTE(rsetaluri): This is a hack to skip the Tuple[] to verilog test since
    # MLIR does not allow leading integers in names (e.g. `!hw.struct<0:
    # ...>`). We should ultimately fix this by changing the IR code generation.
    if ckt.name == "simple_aggregates_tuple":
        kwargs["check_verilog"] = False
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


@pytest.mark.parametrize("disallow_duplicate_symbols", (False, True))
def test_compile_to_mlir_disallow_duplicate_symbols(
        disallow_duplicate_symbols: bool,
):

    class _Test(m.Circuit):
        name = "simple_duplicate_symbols"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bits[2]))
        for o in io.O:
            x = m.Bit(name="x")
            x @= io.I
            o @= x

    ckt = _Test
    m.backend.coreir.insert_coreir_wires.insert_coreir_wires(ckt)
    gold_name = f"{ckt.name}_disallow_duplicate_symbols"
    if disallow_duplicate_symbols:
        gold_name += "_disallow_duplicate_symbols"
    kwargs = {
        "disallow_duplicate_symbols": disallow_duplicate_symbols,
        "gold_name": gold_name,
    }
    if disallow_duplicate_symbols:
        ctx_mgr = pytest.raises(RuntimeError)
    else:
        ctx_mgr = contextlib.nullcontext()
    with ctx_mgr:
        run_test_compile_to_mlir(ckt, **kwargs)


@pytest.mark.parametrize(
    "ckt,location_info_style",
    itertools.product(
        (simple_comb,),
        ("plain", "wrapInAtSquareBracket", "none"),
    )
)
def test_compile_to_mlir_location_info_style(ckt, location_info_style: str):
    gold_name = f"{ckt.name}_location_info_style_{location_info_style}"
    kwargs = {
        "location_info_style": location_info_style,
        "gold_name": gold_name,
    }
    kwargs.update({"check_verilog": False})
    run_test_compile_to_mlir(ckt, **kwargs)


@pytest.mark.parametrize(
    "ckt,explicit_bitcast",
    itertools.product((simple_comb,), (False, True))
)
def test_compile_to_mlir_explicit_bitcast(ckt, explicit_bitcast: bool):
    gold_name = f"{ckt.name}_explicit_bitcast"
    if explicit_bitcast:
        gold_name += "_explicit_bitcast"
    kwargs = {
        "explicit_bitcast": explicit_bitcast,
        "gold_name": gold_name,
    }
    kwargs.update({"check_verilog": False})
    run_test_compile_to_mlir(ckt, **kwargs)


@pytest.mark.parametrize(
    "ckt,disallow_expression_inlining_in_ports",
    itertools.product((simple_comb,), (False, True))
)
def test_compile_to_mlir_disallow_expression_inlining_in_ports(
        ckt,
        disallow_expression_inlining_in_ports: bool
):
    gold_name = f"{ckt.name}_disallow_expression_inlining_in_ports"
    if disallow_expression_inlining_in_ports:
        gold_name += "_disallow_expression_inlining_in_ports"
    kwargs = {
        "disallow_expression_inlining_in_ports": disallow_expression_inlining_in_ports,
        "gold_name": gold_name,
    }
    kwargs.update({"check_verilog": False})
    run_test_compile_to_mlir(ckt, **kwargs)
