import magma as m
import timeit
import pygal


def simple_array(n=128, compile=False):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Array[n, m.Bit]), O=m.Out(m.Array[n, m.Bit]))
        io.O @= io.I
    if compile:
        m.compile("build/Foo", Foo)


data = {
    "frontend": {},
    "backend": {}
}

ns = [128, 256, 512, 1024, 2048]

for n in ns:
    no_compile = timeit.Timer(lambda: simple_array(n)).timeit(number=2)
    with_compile = timeit.Timer(lambda: simple_array(n, True)).timeit(number=2)
    data["frontend"][n] = no_compile
    data["backend"][n] = with_compile - no_compile

print(data)

bar = pygal.Bar()
bar.x_labels = ns
bar.add('frontend', list(data["frontend"].values()))
bar.add('backend', list(data["backend"].values()))
bar.render_to_file("chart.svg")