import magma as m
import timeit
import pygal


def array_2d(T, i=128, j=128, compile=False):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(T[i, T[j, m.Bit]]), O=m.Out(T[i, T[j, m.Bit]]))
        io.O @= io.I
    if compile:
        m.compile("build/Foo", Foo)


data = {
    "frontend_orig": {},
    "frontend_new": {},
    "backend_orig": {},
    "backend_new": {},
}

values = [128, 256, 512]

for i in values:
    for j in values:
        no_compile = timeit.Timer(lambda: array_2d(m.Array, i, j)).timeit(number=2)
        with_compile = timeit.Timer(lambda: array_2d(m.Array, i, j, True)).timeit(number=2)
        data["frontend_orig"][(i, j)] = no_compile
        data["backend_orig"][(i, j)] = with_compile - no_compile
        no_compile = timeit.Timer(lambda: array_2d(m.Array2, i, j)).timeit(number=2)
        with_compile = timeit.Timer(lambda: array_2d(m.Array2, i, j, True)).timeit(number=2)
        data["frontend_new"][(i, j)] = no_compile
        data["backend_new"][(i, j)] = with_compile - no_compile

print(data)

bar = pygal.Bar()
bar.x_labels = [(i, j) for i in values for j in values]
bar.add('frontend_orig', list(data["frontend_orig"].values()))
bar.add('frontend_new', list(data["frontend_new"].values()))
bar.render_to_file("array_2d_bench.svg")

bar = pygal.Bar()
bar.x_labels = [(i, j) for i in values for j in values]
bar.add('backend_orig', list(data["backend_orig"].values()))
bar.add('backend_new', list(data["backend_new"].values()))
bar.render_to_file("array_2d_bench_backend.svg")
