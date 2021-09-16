import magma as m
import timeit
import pygal


def array_2d(i=128, j=128):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Array[i, m.Array[j, m.Bit]]), O=m.Out(m.Array[i, m.Array[j, m.Bit]]))
        k = i // 2
        io.O[:k] @= io.I[k:]
        io.O[k:] @= io.I[:k]


data = {
    "frontend": {},
    "backend": {}
}

values = [128, 256, 512]

for i in values:
    for j in values:
        print(f"Running {i}, {j}")
        num_trials = 1
        t = 0
        for _ in range(num_trials):
            t += timeit.Timer(lambda: array_2d(i, j)).timeit(number=2)
        data["frontend"][(i, j)] = t / num_trials

print(data)

bar = pygal.Bar()
bar.x_labels = [(i, j) for i in values for j in values]
bar.add('frontend', list(data["frontend"].values()))
bar.render_to_file("slice2d.svg")
