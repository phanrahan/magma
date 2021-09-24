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
