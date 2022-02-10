import magma as m
import timeit
import pygal


def combined(T, n=128, compile=False):
    class add(m.Circuit):
        io = m.IO(I0=m.In(T[n, m.Bit]), I1=m.In(T[n, m.Bit]),
                  O=m.Out(T[n, m.Bit]))

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T[n, m.Bit]), O=m.Out(T[n, m.Bit]),
                  O2=m.Out(T[n, m.Bit]),
                  O3=m.Out(T[n, m.Bit]),
                  I4=m.In(T[n, m.Bits[8]]),
                  O4=m.Out(T[n, m.Bits[8]]),
                  O5=m.Out(T[n, m.Bit]),
                  )
        for i in range(n):
            io.O[(n - 1) - i] @= io.I[i]
        io.O2[:n // 2] @= io.I[n // 2:]
        io.O2[n // 2:] @= io.I[:n // 2]
        io.O3 @= io.I
        io.O4 @= io.I4
        io.O5 @= add()(io.I, io.I)

    if compile:
        m.clear_cachedFunctions()
        m.frontend.coreir_.ResetCoreIR()
        m.generator.reset_generator_cache()
        m.compile("build/Foo", Foo)


data = {
    "frontend_orig": {},
    "frontend_new": {},
    "backend_orig": {},
    "backend_new": {},
}

ns = [128, 256, 512]

for n in ns:
    no_compile = timeit.Timer(lambda: combined(m.Array, n)).timeit(number=2)
    with_compile = timeit.Timer(
        lambda: combined(m.Array, n, True)
    ).timeit(number=2)

    data["frontend_orig"][n] = no_compile
    data["backend_orig"][n] = with_compile - no_compile

    no_compile = timeit.Timer(lambda: combined(m.Array, n)).timeit(number=2)
    with_compile = timeit.Timer(
        lambda: combined(m.Array, n, True)
    ).timeit(number=2)

    data["frontend_new"][n] = no_compile
    data["backend_new"][n] = with_compile - no_compile

print(data)

bar = pygal.Bar()
bar.x_labels = ns
bar.add('frontend_orig', list(data["frontend_orig"].values()))
bar.add('frontend_new', list(data["frontend_new"].values()))
bar.render_to_file("combined.svg")

bar = pygal.Bar()
bar.x_labels = ns
bar.add('backend_orig', list(data["backend_orig"].values()))
bar.add('backend_new', list(data["backend_new"].values()))
bar.render_to_file("combined_backend.svg")
