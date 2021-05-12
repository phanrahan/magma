import magma as m


class T(m.Product):
    x = m.Bit
    y = m.Bits[2]


class Baz(m.Circuit):
    io = m.IO(I=m.In(T), O=m.Out(T))
    io.O @= io.I


class Bar(m.Circuit):
    io = m.IO(I=m.In(T), O=m.Out(T))
    io.O @= Baz()(io.I)


class Foo(m.Circuit):
    io = m.IO(I=m.In(T), O=m.Out(T))
    io.O @= Bar()(io.I)


m.compile("build/Foo", Foo)
