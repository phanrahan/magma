"""
Benchmark for compilation of named temporary values.

Results tracked in benchmarks/name.csv.
"""
import magma as m

from benchmarks.benchmark_utils import (
    get_platform,
    get_processor_info,
    get_git_commit,
    get_average_time,
)


def name_bench(name: bool = False):

    class Foo(m.Circuit):
        T = m.Array[8, m.Tuple[m.Bit, m.Bits[8]]]
        io = m.IO(I=m.In(T), O=m.Out(T))
        if name:
            x = T(name="x")
            x @= io.I
        else:
            x = io.I
        io.O @= x

    opts = {
        "flatten_all_tuples": True,
    }
    m.compile("benchmarks/build/Foo", Foo, output="mlir-verilog", **opts)


def _main() -> int:
    NUM_RUNS = 100
    no_name = get_average_time(lambda: name_bench(), NUM_RUNS)
    with_name = get_average_time(lambda: name_bench(name=True), NUM_RUNS)
    data = {
        "no_name": no_name,
        "with_name": with_name,
        "commit": get_git_commit(),
        "platform": get_platform(),
        "cpu": get_processor_info(),
    }
    print (",".join(data.keys()))
    print (",".join(map(str, data.values())))
    return 0


if __name__ == "__main__":
    exit(_main())
