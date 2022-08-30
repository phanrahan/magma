import magma as m


T = m.Array
n = 512


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
    io.O @= io.I
    io.O2[:n // 2] @= io.I[n // 2:]
    io.O2[n // 2:] @= io.I[:n // 2]
    io.O3 @= io.I
    io.O4 @= io.I4
    io.O5 @= add()(io.I, io.I)


m.compile("build/Foo", Foo, output="coreir-verilog")
