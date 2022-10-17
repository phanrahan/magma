import difflib
import functools
import glob
import importlib
import io
import os
import sys
from typing import Any, Dict, List, Optional

from magma.backend.mlir.compile_to_mlir import (
    compile_to_mlir, CompileToMlirOpts
)
from magma.backend.mlir.mlir_to_verilog import mlir_to_verilog
from magma.circuit import DefineCircuitKind
from magma.common import slice_opts
from magma.config import config, EnvConfig
from magma.passes.clock import WireClockPass

import examples


config._register(
    test_mlir_check_verilog=EnvConfig(
        "TEST_MLIR_CHECK_VERILOG", False, bool))
config._register(
    test_mlir_write_output_files=EnvConfig(
        "TEST_MLIR_WRITE_OUTPUT_FILES", False, bool))

_CMP_BUFSIZE = 8 * 1024
_MAGMA_EXAMPLES_TO_SKIP = (
    "risc",
)


def _maybe_get_config(value: Any, key: str) -> Any:
    if value is not None:
        return value
    return getattr(config, key)


def _compile_to_mlir(
        ckt: DefineCircuitKind,
        write_output_files: bool,
        opts: CompileToMlirOpts) -> io.TextIOBase:
    if not write_output_files:
        mlir_out = io.TextIOWrapper(io.BytesIO())
        compile_to_mlir(ckt, mlir_out, opts)
        return mlir_out
    filename = f"{ckt.name}.mlir"
    with open(filename, "w") as mlir_out:
        compile_to_mlir(ckt, mlir_out, opts)
    mlir_out = open(filename, "rb")
    return io.TextIOWrapper(mlir_out)


def _compile_to_verilog(
        ckt: DefineCircuitKind,
        mlir_out: io.RawIOBase,
        write_output_files: bool) -> io.RawIOBase:
    if not write_output_files:
        verilog_out = io.BytesIO()
        mlir_to_verilog(mlir_out, verilog_out)
        return verilog_out
    filename = f"{ckt.name}.v"
    with open(filename, "wb") as verilog_out:
        mlir_to_verilog(mlir_out, verilog_out)
    return open(filename, "rb")


def cmp_streams(
        s1: io.RawIOBase,
        s2: io.RawIOBase,
        bufsize: int = _CMP_BUFSIZE) -> bool:
    while True:
        b1 = s1.read(bufsize)
        b2 = s2.read(bufsize)
        if b1 != b2:
            return False
        if not b1:
            return True
    raise RuntimeError("Should not reach here")


def check_streams_equal(
        s1: io.RawIOBase,
        s2: io.RawIOBase,
        from_label: str = "",
        to_label: str = "",
        writer: io.TextIOBase = sys.stderr):
    cmp = cmp_streams(s1, s2)
    if cmp:
        return True
    s1.seek(0)
    s2.seek(0)
    ts1 = io.TextIOWrapper(s1)
    ts2 = io.TextIOWrapper(s2)
    diff = difflib.unified_diff(
        ts1.readlines(), ts2.readlines(), from_label, to_label)
    writer.writelines(diff)
    return False


def run_test_compile_to_mlir(
        ckt: DefineCircuitKind,
        check_verilog: Optional[bool] = None,
        write_output_files: Optional[bool] = None,
        gold_name: Optional[str] = None,
        **kwargs):
    golds_dir = f"{os.path.dirname(__file__)}/golds"
    write_output_files = _maybe_get_config(
        write_output_files, "test_mlir_write_output_files")
    WireClockPass(ckt).run()
    opts = slice_opts(kwargs, CompileToMlirOpts)
    mlir_out = _compile_to_mlir(ckt, write_output_files, opts)
    mlir_out.seek(0)
    gold_name = gold_name if gold_name is not None else ckt.name
    with open(f"{golds_dir}/{gold_name}.mlir", "rb") as mlir_gold:
        assert check_streams_equal(mlir_out.buffer, mlir_gold, "out", "gold")
    check_verilog = _maybe_get_config(check_verilog, "test_mlir_check_verilog")
    if check_verilog:
        mlir_out.seek(0)
        verilog_out = _compile_to_verilog(
            ckt, mlir_out.buffer, write_output_files)
        verilog_out.seek(0)
        with open(f"{golds_dir}/{gold_name}.v", "rb") as verilog_gold:
            assert check_streams_equal(verilog_out, verilog_gold, "out", "gold")
        verilog_out.close
    mlir_out.close()


@functools.lru_cache()
def get_local_examples() -> List[DefineCircuitKind]:
    return [
        examples.simple_comb,
        examples.simple_hierarchy,
        examples.simple_aggregates_bits,
        examples.simple_aggregates_array,
        examples.simple_aggregates_nested_array,
        examples.complex_aggregates_nested_array,
        examples.simple_aggregates_product,
        examples.simple_aggregates_tuple,
        examples.simple_constant,
        examples.aggregate_constant,
        examples.simple_mux_wrapper,
        examples.aggregate_mux_wrapper,
        examples.non_power_of_two_mux_wrapper,
        examples.simple_register_wrapper,
        examples.complex_register_wrapper,
        examples.counter,
        examples.twizzle,
        examples.simple_unused_output,
        examples.feedthrough,
        examples.no_outputs,
        examples.simple_mixed_direction_ports,
        examples.complex_mixed_direction_ports,
        examples.complex_mixed_direction_ports2,
        examples.simple_decl_external,
        examples.simple_verilog_defn_wrapper,
        examples.simple_length_one_array,
        examples.simple_length_one_bits,
        examples.simple_array_of_bit,
        examples.simple_reduction,
        examples.simple_shifts,
        examples.simple_wire,
        examples.complex_wire,
        examples.simple_wrap_cast,
        examples.simple_redefinition,
        examples.simple_lut,
        examples.complex_lut,
        examples.simple_side_effect_instance,
        examples.simple_inline_verilog,
        examples.complex_inline_verilog,
        examples.simple_bind,
        examples.complex_bind,
        examples.xmr_bind,
        examples.simple_compile_guard,
        examples.simple_custom_verilog_name,
        examples.simple_module_params_instance,
        examples.simple_undriven,
        examples.complex_undriven,
        examples.simple_memory_wrapper,
        examples.simple_undriven_instances,
        examples.simple_neg,
        examples.simple_array_slice,
        examples.simple_magma_protocol,
        examples.simple_smart_bits,
        examples.complex_magma_protocol,
    ]


@functools.lru_cache()
def get_magma_examples(
        skips=_MAGMA_EXAMPLES_TO_SKIP) -> List[DefineCircuitKind]:
    try:
        import magma_examples
    except Exception as e:
        return []
    path = magma_examples.__path__
    py_filenames = glob.glob(f"{path._path[0]}/*.py")
    ckts = []
    for py_filename in py_filenames:
        py_module_name = py_filename.split("/")[-1].split(".")[0]
        if py_module_name in skips:
            continue
        full_name = f"magma_examples.{py_module_name}"
        py_module = importlib.import_module(full_name)
        ckts += list(filter(
            lambda v: isinstance(v, DefineCircuitKind),
            (getattr(py_module, k) for k in dir(py_module))))
    return ckts
