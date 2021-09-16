import magma as m
import timeit
import pygal


def simple_array_slice(n=128):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Array[n, m.Bit]), O=m.Out(m.Array[n, m.Bit]))
        i = n // 2
        io.O[:i] @= io.I[i:]
        io.O[i:] @= io.I[:i]


data = {
    "frontend": {},
    "backend": {}
}

ns = [128, 256, 512, 1024, 2048]

for n in ns:
    num_trials = 5
    t = 0
    for _ in range(num_trials):
        t += timeit.Timer(lambda: simple_array_slice(n)).timeit(number=2)
    data["frontend"][n] = t / num_trials

print(data)

bar = pygal.Bar()
bar.x_labels = ns
bar.add('frontend', list(data["frontend"].values()))
bar.render_to_file("slice.svg")
