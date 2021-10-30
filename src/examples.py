import itertools

import magma as m


class simple_comb(m.Circuit):
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
    y, z = simple_comb()(io.a, io.b, io.c)
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


class simple_mux_wrapper(m.Circuit):
    T = m.Bits[8]
    io = m.IO(a=m.In(T), s=m.In(m.Bit), y=m.Out(T))
    io.y @= m.mux([io.a, ~io.a], io.s)


class aggregate_mux_wrapper(m.Circuit):
    T = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bit))
    io = m.IO(a=m.In(T), s=m.In(m.Bit), y=m.Out(T))
    not_a = T(*map(lambda x: ~x, io.a))
    io.y @= m.mux([io.a, not_a], io.s)


class simple_register_wrapper(m.Circuit):
    T = m.Bits[8]
    io = m.IO(a=m.In(T), y=m.Out(T))
    io.y @= m.register(io.a, init=3, name="reg0")


class complex_register_wrapper(m.Circuit):
    T0 = m.Product.from_fields("anon", dict(x=m.Bits[8], y=m.Bit))
    T1 = m.Array[6, m.Bits[16]]
    T2 = m.Product.from_fields("anon", dict(u=T0, v=T1))
    io = m.IO(a=m.In(T0), b=m.In(T1), y=m.Out(T2))
    io += m.ClockIO(has_async_reset=True)
    reg_a = m.register(io.a, init=T0(10, 1), reset_type=m.AsyncReset)
    reg_b = m.register(io.b, init=T1(*(i * 2 for i in range(T1.N))))
    y = T2(reg_a, reg_b)
    io.y @= y


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
    _, z = simple_comb()(io.a, io.b, io.c)
    io.y @= z


class feedthrough(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I


class no_outputs(m.Circuit):
    io = m.IO(I=m.In(m.Bit))
    ~io.I


class simple_mixed_direction_ports(m.Circuit):
    S = m.Bits[8]
    T = m.Product.from_fields("anon", dict(x=m.In(S), y=m.Out(S)))
    io = m.IO(a=T)
    io.a.y @= io.a.x


class complex_mixed_direction_ports(m.Circuit):
    S = m.Bits[8]
    T = m.Product.from_fields("anon", dict(x=m.In(S), y=m.Out(S)))
    io = m.IO(a=m.Array[8, T], b=T.flip())
    m.wire(io.a[1], io.b)
    for i, aa in enumerate(io.a):
        if i == 1: continue
        aa.y @= 0


class complex_mixed_direction_ports2(m.Circuit):
    S = m.Bits[8]
    T = m.Product.from_fields("anon", dict(x=m.In(S), y=m.Out(S)))
    io = m.IO(a=T)
    simple = simple_mixed_direction_ports()
    m.wire(io.a.x, simple.a.x)
    m.wire(io.a.y, simple.a.y)


class simple_decl(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))


class simple_decl_external(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= simple_decl()(io.I)


class simple_verilog_defn(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    verilog = "assign O = I;"


class simple_verilog_defn_wrapper(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= simple_verilog_defn()(io.I)


class simple_length_one_array(m.Circuit):
    io = m.IO(I=m.In(m.Array[1, m.Bits[8]]), O=m.Out(m.Bits[8]))
    io.O @= io.I[0]


class simple_array_of_bit(m.Circuit):
    T = m.Array[8, m.Bit]
    io = m.IO(I=m.In(T), O=m.Out(T))
    io.O @= T(list(reversed(io.I)))


class simple_reduction(m.Circuit):
    T = m.Bits[8]
    io = m.IO(
        I0=m.In(T), I1=m.In(T), I2=m.In(T),
        O0=m.Out(m.Bit), O1=m.Out(m.Bit), O2=m.Out(m.Bit)
    )
    io.O1 @= io.I1.reduce_or()
    io.O0 @= io.I0.reduce_and()
    io.O2 @= io.I2.reduce_xor()
