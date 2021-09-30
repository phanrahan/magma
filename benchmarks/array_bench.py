import magma as m
import timeit
import pygal


def simple_array(T, n=128, compile=False):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(T[n, m.Bit]), O=m.Out(T[n, m.Bit]))
        io.O @= io.I
    if compile:
        m.compile("build/Foo", Foo)


data = {
    "frontend_orig": {},
    "backend_orig": {},
    "frontend_new": {},
    "backend_new": {}
}

ns = [128, 256, 512, 1024, 2048]

for n in ns:
    no_compile = timeit.Timer(lambda: simple_array(m.Array, n)).timeit(number=2)
    with_compile = timeit.Timer(lambda: simple_array(m.Array, n, True)).timeit(number=2)
    data["frontend_orig"][n] = no_compile
    data["backend_orig"][n] = with_compile - no_compile

    no_compile = timeit.Timer(lambda: simple_array(m.Array2, n)).timeit(number=2)
    with_compile = timeit.Timer(lambda: simple_array(m.Array2, n, True)).timeit(number=2)
    data["frontend_new"][n] = no_compile
    data["backend_new"][n] = with_compile - no_compile

print(data)

bar = pygal.Bar()
bar.x_labels = ns
bar.add('frontend_orig', list(data["frontend_orig"].values()))
bar.add('frontend_new', list(data["frontend_new"].values()))
bar.render_to_file("array_bench.svg")

bar = pygal.Bar()
bar.x_labels = ns
bar.add('backend_orig', list(data["backend_orig"].values()))
bar.add('backend_new', list(data["backend_new"].values()))
bar.render_to_file("array_bench_backend.svg")
