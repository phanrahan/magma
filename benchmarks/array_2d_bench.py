import magma as m
import timeit
import pygal


def array_2d(i=128, j=128, compile=False):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Array[i, m.Array[j, m.Bit]]), O=m.Out(m.Array[i, m.Array[j, m.Bit]]))
        io.O @= io.I
    if compile:
        m.compile("build/Foo", Foo)


data = {
    "frontend": {},
    "backend": {}
}

values = [128, 256, 512]

for i in values:
    for j in values:
        no_compile = timeit.Timer(lambda: array_2d(i, j)).timeit(number=2)
        with_compile = timeit.Timer(lambda: array_2d(i, j, True)).timeit(number=2)
        data["frontend"][(i, j)] = no_compile
        data["backend"][(i, j)] = with_compile - no_compile

print(data)

bar = pygal.Bar()
bar.x_labels = [(i, j) for i in values for j in values]
bar.add('frontend', list(data["frontend"].values()))
bar.add('backend', list(data["backend"].values()))
bar.render_to_file("array_2d_bench.svg")
