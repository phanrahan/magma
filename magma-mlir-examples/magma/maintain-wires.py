import magma as m

from common import print_verilog


class Top(m.Circuit):
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    _x = io.I0 | io.I1
    x = m.Bit(_x, name="x")
    io.O @= x


if __name__ == "__main__":
    print_verilog(Top, inline=True)
