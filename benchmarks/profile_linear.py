import pstats
from pstats import SortKey
import cProfile
import magma as m
import timeit
import pygal


def linear(T, n=128, compile=False):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(T[n, m.Bit]), O=m.Out(T[n, m.Bit]))
        for i in range(n):
            io.O[(n - 1) - i] @= io.I[i]
    if compile:
        m.clear_cachedFunctions()
        m.frontend.coreir_.ResetCoreIR()
        m.generator.reset_generator_cache()
        m.compile("build/Foo", Foo)


cProfile.run('linear(m.Array2, 128, True)', 'linearstats')

p = pstats.Stats('linearstats')
p = p.strip_dirs()
p.sort_stats(SortKey.CUMULATIVE).print_stats(20)
