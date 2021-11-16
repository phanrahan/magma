import difflib
import functools
import glob
import importlib
import io
import os
import pathlib
import sys
from typing import Any, List, Optional

import magma as m

from compile_to_mlir import compile_to_mlir
import examples
import magma_examples
from mlir_to_verilog import mlir_to_verilog


_CMP_BUFSIZE = 8 * 1024
_MAGMA_EXAMPLES_TO_SKIP = (
    "risc",
)


def _maybe_get_env(value: Any, key: str, default: Any) -> Any:
    if value is not None:
        return value
    typ = type(default)
    return typ(os.environ.get(key, default))


def _compile_to_mlir(
        ckt: m.DefineCircuitKind, write_output_files: bool) -> io.TextIOBase:
    if not write_output_files:
        mlir_out = io.TextIOWrapper(io.BytesIO())
        compile_to_mlir(ckt, mlir_out)
        return mlir_out
    filename = f"{ckt.name}.mlir"
    with open(filename, "w") as mlir_out:
        compile_to_mlir(ckt, mlir_out)
    mlir_out = open(filename, "rb")
    return io.TextIOWrapper(mlir_out)


def _compile_to_verilog(
        ckt: m.DefineCircuitKind,
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
        ckt: m.DefineCircuitKind,
        check_verilog: Optional[bool] = None,
        write_output_files: Optional[bool] = None):
    check_verilog = _maybe_get_env(check_verilog, "CHECK_VERILOG", 0)
    write_output_files = _maybe_get_env(
        write_output_files, "WRITE_OUTPUT_FILES", 0)
    m.passes.clock.WireClockPass(ckt).run()
    mlir_out = _compile_to_mlir(ckt, write_output_files)
    mlir_out.seek(0)
    with open(f"golds/{ckt.name}.mlir", "rb") as mlir_gold:
        assert check_streams_equal(mlir_out.buffer, mlir_gold, "out", "gold")
    if check_verilog:
        with open(f"golds/{ckt.name}.v", "rb") as verilog_gold:
            mlir_out.seek(0)
            verilog_out = _compile_to_verilog(
                ckt, mlir_out.buffer, write_output_files)
            verilog_out.seek(0)
            assert check_streams_equal(verilog_out, verilog_gold, "out", "gold")
        verilog_out.close
    mlir_out.close()


@functools.lru_cache()
def get_local_examples() -> List[m.DefineCircuitKind]:
    return [
        examples.simple_comb,
        examples.simple_hierarchy,
        examples.simple_aggregates_bits,
        examples.simple_aggregates_array,
        examples.simple_aggregates_nested_array,
        examples.complex_aggregates_nested_array,
        examples.simple_aggregates_tuple,
        examples.simple_constant,
        examples.aggregate_constant,
        examples.simple_mux_wrapper,
        examples.aggregate_mux_wrapper,
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
    ]


@functools.lru_cache()
def get_magma_examples(
        skips=_MAGMA_EXAMPLES_TO_SKIP) -> List[m.DefineCircuitKind]:
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
            lambda v: isinstance(v, m.DefineCircuitKind),
            (getattr(py_module, k) for k in dir(py_module))))
    return ckts
