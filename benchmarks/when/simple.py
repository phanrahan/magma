import timeit
import magma as m


def define_foo():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bits[8]]), S=m.In(m.Bit), O=m.Out(m.Bits[8]))
        io.O @= io.I[io.S]



def define_bar():
    class Bar(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bits[8]]), S=m.In(m.Bit), O=m.Out(m.Bits[8]))

        @m.inline_combinational()
        def logic():
            if io.S:
                io.O @= io.I[1]
            else:
                io.O @= io.I[0]

foo_time = timeit.Timer(define_foo).timeit(number=2)
bar_time = timeit.Timer(define_bar).timeit(number=2)
print(f"Foo={foo_time}")
print(f"Bar={bar_time}")
print(f"Speedup={bar_time/foo_time}")
