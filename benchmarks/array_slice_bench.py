import magma as m
import timeit
import pygal


def simple_array_slice(T, n=128):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(T[n, m.Bit]), O=m.Out(T[n, m.Bit]))
        i = n // 2
        io.O[:i] @= io.I[i:]
        io.O[i:] @= io.I[:i]


data = {
    "frontend_orig": {},
    "frontend_new": {},
    # "backend": {}
}

ns = [128, 256, 512, 1024, 2048]

for n in ns:
    num_trials = 5
    t = 0
    for _ in range(num_trials):
        t += timeit.Timer(lambda: simple_array_slice(m.Array, n)).timeit(number=2)
    data["frontend_orig"][n] = t / num_trials
    t = 0
    for _ in range(num_trials):
        t += timeit.Timer(lambda: simple_array_slice(m.Array2, n)).timeit(number=2)
    data["frontend_new"][n] = t / num_trials

print(data)

bar = pygal.Bar()
bar.x_labels = ns
bar.add('frontend_orig', list(data["frontend_orig"].values()))
bar.add('frontend_new', list(data["frontend_new"].values()))
bar.render_to_file("slice.svg")
