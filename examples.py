import itertools

import magma as m


class comb(m.Circuit):
    T = m.Bits[16]
    io = m.IO(a=m.In(T), b=m.In(T), c=m.In(T), y=m.Out(T), z=m.Out(T))
    a = ~io.a
    o = io.a | a
    o = o | io.b
    io.y @= o
    io.z @= o


class simple_hierarchy(m.Circuit):
    T = m.Bits[16]
    io = m.IO(a=m.In(T), b=m.In(T), c=m.In(T), y=m.Out(T), z=m.Out(T))
    y, z = comb()(io.a, io.b, io.c)
    io.y @= y
    io.z @= z


class simple_aggregates_bits(m.Circuit):
    T = m.Bits[16]
    io = m.IO(a=m.In(T), y=m.Out(T))
    half = int(T.N / 2)
    io.y[:half] @= io.a[half:]
    io.y[half:] @= io.a[:half]


class simple_aggregates_array(m.Circuit):
    T = m.Array[8, m.Bits[16]]
    io = m.IO(a=m.In(T), y=m.Out(T))
    half = int(T.N / 2)
    io.y[:half] @= io.a[half:]
    io.y[half:] @= io.a[:half]


class simple_aggregates_nested_array(m.Circuit):
    T = m.Array[8, m.Array[4, m.Bits[16]]]
    io = m.IO(a=m.In(T), y=m.Out(T))
    half = int(T.N / 2)
    io.y[:half] @= io.a[half:]
    io.y[half:] @= io.a[:half]


class complex_aggregates_nested_array(m.Circuit):
    T = m.Array[2, m.Array[3, m.Bits[4]]]
    io = m.IO(a=m.In(T), y=m.Out(T))

    I, J, K = T.N, T.T.N, T.T.T.N
    for i, j, k in itertools.product(range(I), range(J), range(K)):
        i1, j1, k1 = I - i - 1, J - j - 1, K - k - 1
        a0 = io.a[i][j][k]
        a1 = io.a[i1][j1][k1]
        io.y[i][j][k] @= a0 | a1


class simple_aggregates_tuple(m.Circuit):
    S = m.Bits[8]
    T = m.Product.from_fields("anon", dict(x=S, y=S))
    io = m.IO(a=m.In(T), y=m.Out(T))
    io.y.x @= ~io.a.x
    io.y.y @= ~io.a.y


class simple_constant(m.Circuit):
    io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
    io.O @= io.I << 1


class aggregate_constant(m.Circuit):
    T = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bits[4]))
    io = m.IO(y=m.Out(T))
    y = T(m.Bits[8](0), m.Bits[4](0))
    io.y @= y


simple_mux = m.Mux(T=m.Bits[8], height=2)


_T_product = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bit))


aggregate_mux = m.Mux(T=_T_product, height=6)


simple_register = m.Register(T=m.Bits[8])
m.passes.clock.WireClockPass(simple_register).run()


_init = _T_product(m.Bits[8](6), m.Bit(1))
complex_register = m.Register(_T_product, init=_init)
m.passes.clock.WireClockPass(complex_register).run()


class counter(m.Circuit):
    T = m.UInt[16]
    io = m.IO(y=m.Out(T)) + m.ClockIO()
    O = T()
    reg = m.Register(T)()
    O @= reg.O
    reg.I @= O + 1
    io.y @= O


m.passes.clock.WireClockPass(counter).run()


class _twizzler(m.Circuit):
    name = "twizzler"
    io = m.IO(
        I0=m.In(m.Bit), I1=m.In(m.Bit), I2=m.In(m.Bit),
        O0=m.Out(m.Bit), O1=m.Out(m.Bit), O2=m.Out(m.Bit))
    io.O0 @= ~io.I1
    io.O1 @= ~io.I0
    io.O2 @= ~io.I2


class twizzle(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    t0 = _twizzler(name="t0")
    t1 = _twizzler(name="t1")
    t0.I0 @= io.I
    t0.I1 @= t1.O0
    t0.I2 @= t1.O1
    t1.I0 @= t0.O0
    t1.I1 @= t0.O1
    t1.I2 @= t0.O2
    io.O @= t1.O2


class simple_unused_output(m.Circuit):
    T = m.Bits[16]
    io = m.IO(a=m.In(T), b=m.In(T), c=m.In(T), y=m.Out(T))
    _, z = comb()(io.a, io.b, io.c)
    io.y @= z
