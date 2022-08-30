import magma as m


class Foo(m.Circuit):
    io = m.IO(I=m.In(m.SInt[2]), S=m.In(m.Bit), O=m.Out(m.SInt[2]))
    with m.when(io.S):
        io.O @= io.I
    with m.otherwise():
        io.O @= m.sint(m.uint(io.I) >> 1)


m.compile("build/Foo", Foo, output="mlir-verilog")
