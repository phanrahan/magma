import magma as m
import timeit
import pygal


def array_2d(T, i=128, j=128):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(T[i, T[j, m.Bit]]), O=m.Out(T[i, T[j, m.Bit]]))
        k = i // 2
        io.O[:k] @= io.I[k:]
        io.O[k:] @= io.I[:k]


data = {
    "frontend_orig": {},
    "frontend_new": {},
    # "backend": {}
}

values = [128, 256, 512]

for i in values:
    for j in values:
        print(f"Running {i}, {j}")
        num_trials = 1
        t = 0
        for _ in range(num_trials):
            t += timeit.Timer(lambda: array_2d(m.Array, i, j)).timeit(number=2)
        data["frontend_orig"][(i, j)] = t / num_trials
        t = 0
        for _ in range(num_trials):
            t += timeit.Timer(lambda: array_2d(m.Array2, i, j)).timeit(number=2)
        data["frontend_new"][(i, j)] = t / num_trials

print(data)

bar = pygal.Bar()
bar.x_labels = [(i, j) for i in values for j in values]
bar.add('frontend_orig', list(data["frontend_orig"].values()))
bar.add('frontend_new', list(data["frontend_new"].values()))
bar.render_to_file("slice2d.svg")
