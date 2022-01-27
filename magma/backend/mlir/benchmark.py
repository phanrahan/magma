import contextlib
import cProfile
import pstats
from typing import Optional

import magma as m

from compile_to_mlir import compile_to_mlir


@contextlib.contextmanager
def profiler():
    profile = cProfile.Profile()
    profile.enable()
    try:
        yield profile
    finally:
        profile.disable()


def benchmark(defn: m.DefineCircuitKind, tag: Optional[str] = None):
    m.passes.clock.WireClockPass(defn).run()
    basename = defn.name
    if tag:
        basename = f"{basename}.{tag}"
    with open(f"{basename}.mlir", "w") as f:
        with profiler() as pr:
            compile_to_mlir(defn, f)
    pstats.Stats(pr).dump_stats(f"{basename}.mlir.pstats")
    with profiler() as pr:
        m.compile(basename, defn, output="coreir")
    pstats.Stats(pr).dump_stats(f"{basename}.coreir.pstats")
