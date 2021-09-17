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
