import magma as m

from common import print_verilog


class Foo(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I


class Top(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= Foo()(io.I)


if __name__ == "__main__":
    print_verilog(Top, inline=True)
