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
    counter,
    twizzle,
    simple_unused_output,
    feedthrough,
]


def _add_magma_examples():
    import glob
    import importlib
    import sys
    global _ckts
    PATH = "magma_examples/magma_examples"
    SKIPS = ("risc",)
    sys.path.append(PATH)
    py_filenames = glob.glob(f"{PATH}/*.py")
    for py_filename in py_filenames:
        py_module_name = py_filename.split("/")[-1].split(".")[0]
        if py_module_name in SKIPS:
            continue
        py_module = importlib.import_module(py_module_name)
        _ckts += list(filter(
            lambda v: isinstance(v, m.DefineCircuitKind),
            (getattr(py_module, k) for k in dir(py_module))))


_add_magma_examples()


@pytest.mark.parametrize("ckt", _ckts)
def test_compile_to_mlir(ckt):
    m.passes.clock.WireClockPass(ckt).run()
    filename = f"{ckt.name}.mlir"
    with open(filename, "w") as f:
        compile_to_mlir(ckt, f)
    assert check_files_equal(__file__, filename, f"golds/{filename}")
