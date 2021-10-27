import pstats
from pstats import SortKey
import cProfile
import magma as m
import timeit
import pygal
from magma.primitives.array2 import Slices


def linear(T, n=128, compile=False):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(T[n, m.Bits[8]]), O=m.Out(T[n, m.Bits[8]]))
        if T is m.Array2:
            slices = tuple((i + 1, i) for i in range(n - 1, -1, -1))
            io.O @= m.concat2(*Slices(T[n, m.Bit], slices)()(io.I))
        # O = []
        # for i in range(n):
        #     O.insert(0, io.I[i:i + 1])
        # io.O @= m.concat2(*O)
        else:
            for i in range(n):
                io.O[(n - 1) - i] @= io.I[i]
    if compile:
        m.clear_cachedFunctions()
        m.frontend.coreir_.ResetCoreIR()
        m.generator.reset_generator_cache()
        m.compile("build/Foo", Foo)


cProfile.run('linear(m.Array, 128, False)', 'linearstats')

p = pstats.Stats('linearstats')
p = p.strip_dirs()
p.sort_stats(SortKey.CUMULATIVE).print_stats(40)


# cProfile.run('linear(m.Array, 128, True)', 'linearoldstats')

# p = pstats.Stats('linearoldstats')
# p = p.strip_dirs()
# p.sort_stats(SortKey.CUMULATIVE).print_stats(20)
