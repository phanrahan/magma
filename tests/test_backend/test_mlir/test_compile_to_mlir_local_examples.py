import contextlib
import itertools
import pathlib
import pytest

import magma as m
from magma.config import config
from magma.debug import debug_info
from magma.passes.finalize_whens import finalize_whens
from magma.primitives.mux import CoreIRCommonLibMuxN
from magma.uniquification import uniquification_pass, reset_names

from examples import (
    simple_aggregates_product,
    aggregate_mux_wrapper,
    non_power_of_two_mux_wrapper,
    complex_register_wrapper,
    complex_bind,
    simple_comb,
    simple_hierarchy,
    simple_register_wrapper,
)
from test_utils import (
    get_local_examples,
    run_test_compile_to_mlir,
    check_streams_equal,
)


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
    "location_info_style",
    ("plain", "wrapInAtSquareBracket", "none"),
)
def test_compile_to_mlir_location_info_style(location_info_style: str):

    class _top(m.Circuit):
        name = "simple_structural"
        T = m.Bits[16]
        io = m.IO(a=m.In(T), b=m.In(T), c=m.In(T), y=m.Out(T), z=m.Out(T))
        io += m.ClockIO()
        a_reg = m.Register(T)(name="a_reg")
        a_reg.I @= io.a
        a = a_reg.O
        io.y @= a & io.c
        io.z @= a | io.b

    ckt = _top
    gold_name = f"{ckt.name}_location_info_style_{location_info_style}"
    kwargs = {
        "location_info_style": location_info_style,
        "gold_name": gold_name,
    }
    kwargs.update({"check_verilog": False})
    # Attach dummy debug info to ckt.
    ckt.debug_info = debug_info("file.py", 100, "")
    for i, inst in enumerate(ckt.instances):
        inst.debug_info = debug_info("file.py", 100 + i, "")
    ckt.a_reg.I.debug_info = debug_info("file.py", 200, "")
    ckt.a_reg.O.debug_info = debug_info("file.py", 201, "")
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


@pytest.mark.parametrize("disallow_local_variables", (False, True))
def test_compile_to_mlir_disallow_local_variables(disallow_local_variables: bool):

    class _Test(m.Circuit):
        name = "simple_disallow_local_variables"
        T = m.Bits[2]
        io = m.IO(x=m.In(T), s=m.In(m.Bit), O=m.Out(T))
        x0 = T()
        with m.when(io.s):
            x0 @= ~io.x
        with m.otherwise():
            x0 @= io.x
        with m.when(~io.s):
            io.O @= m.bits(list(reversed(x0)))
        with m.otherwise():
            io.O @= x0

    ckt = _Test
    finalize_whens(ckt)

    gold_name = ckt.name
    if disallow_local_variables:
        gold_name += "_disallow_local_variables"
    kwargs = {
        "disallow_local_variables": disallow_local_variables,
        "gold_name": gold_name,
    }
    run_test_compile_to_mlir(ckt, **kwargs)


@pytest.mark.parametrize("ckt", (simple_hierarchy,))
def test_compile_to_mlir_split_verilog(ckt):
    dirname = pathlib.Path("tests/test_backend/test_mlir/")
    basename = dirname / "build" / ckt.name
    gold_name = ckt.name + "_split_verilog"
    kwargs = {
        "split_verilog": True,
        "gold_name": gold_name,
        "basename": basename,
        "suffix": "v",
    }
    run_test_compile_to_mlir(ckt, **kwargs)
    if config.test_mlir_check_verilog:
        with open(f"{basename}.v", "rb") as verilog_out:
            with open(f"{dirname}/golds/{gold_name}_real.v", "rb") as verilog_gold:
                assert check_streams_equal(verilog_out, verilog_gold, "out", "gold")
