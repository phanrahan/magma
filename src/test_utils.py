import functools
import glob
import importlib
from typing import List

import magma as m
import magma_examples


_SKIPS = (
    "risc",
)


@functools.lru_cache()
def get_magma_examples() -> List[m.DefineCircuitKind]:
    path = magma_examples.__path__
    py_filenames = glob.glob(f"{path._path[0]}/*.py")
    ckts = []
    for py_filename in py_filenames:
        py_module_name = py_filename.split("/")[-1].split(".")[0]
        if py_module_name in _SKIPS:
            continue
        full_name = f"magma_examples.{py_module_name}"
        py_module = importlib.import_module(full_name)
        ckts += list(filter(
            lambda v: isinstance(v, m.DefineCircuitKind),
            (getattr(py_module, k) for k in dir(py_module))))
    return ckts
