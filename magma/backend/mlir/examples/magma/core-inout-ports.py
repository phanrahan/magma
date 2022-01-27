import magma as m

from common import print_verilog


class Foo(m.Circuit):
    io = m.IO(I=m.InOut(m.Bit), O=m.InOut(m.Bit))
    m.wire(io.I, io.O)


class Top(m.Circuit):
    io = m.IO(I=m.InOut(m.Bit), O=m.InOut(m.Bit))
    foo0 = Foo()
    foo1 = Foo()
    m.wire(io.I, foo0.I)
    m.wire(foo0.O, foo1.O)
    m.wire(foo1.I, io.O)


if __name__ == "__main__":
    print_verilog(Top, print_ir=True, inline=True)
