"""
Lenny's results:
    no_name 0.5316979909999999
    with_name 1.0124146129999998
"""
import magma as m
import timeit


def name_bench(name=False):
    class Foo(m.Circuit):
        T = m.Array[8, m.Tuple[m.Bit, m.Bits[8]]]
        io = m.IO(I=m.In(T), O=m.Out(T))
        if name:
            x = T(name="x")
            x @= io.I
        else:
            x = io.I
        io.O @= x

    m.compile("build/Foo", Foo, output="mlir-verilog",
              flatten_all_tuples=True)


no_name = timeit.Timer(lambda: name_bench()).timeit(number=10)
with_name = timeit.Timer(lambda: name_bench(True)).timeit(number=10)
print("no_name", no_name)
print("with_name", with_name)
