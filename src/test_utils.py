import functools
import glob
import importlib
import os
from typing import List, Optional

import magma as m
from magma.testing import check_files_equal
import magma_examples

from compile_to_mlir import compile_to_mlir
import examples


_MAGMA_EXAMPLES_TO_SKIP = (
    "risc",
)

_MLIR_TO_VERILOG_BIN = "./run.sh"


def get_check_verilog(default: bool) -> bool:
    return os.environ.get("CHECK_VERILOG", default)


def run_verilog_check(mlir_filename: str, verilog_filename: str):
    cmd = f"cat {mlir_filename} | {_MLIR_TO_VERILOG_BIN} > out.v"
    os.system(cmd)
    assert check_files_equal(__file__, "out.v", verilog_filename)


def run_test_compile_to_mlir(
        ckt: m.DefineCircuitKind, check_verilog: Optional[bool] = None):
    if check_verilog is None:
        check_verilog = get_check_verilog(False)
    m.passes.clock.WireClockPass(ckt).run()
    filename = f"{ckt.name}.mlir"
    with open(filename, "w") as f:
        compile_to_mlir(ckt, f)
    assert check_files_equal(__file__, filename, f"golds/{filename}")
    if check_verilog:
        run_verilog_check(filename, f"golds/{ckt.name}.v")


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
