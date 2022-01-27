import magma as m

from common import print_verilog


class Top2to1(m.Circuit):
    io = m.IO(
        I0=m.In(m.Bits[4]),
        I1=m.In(m.Bits[4]),
        S=m.In(m.Bit),
        O=m.Out(m.Bits[4]))
    io.O @= m.mux([io.I0, io.I1], io.S)


class Top8to1(m.Circuit):
    io = m.IO(
        I0=m.In(m.Bits[4]),
        I1=m.In(m.Bits[4]),
        I2=m.In(m.Bits[4]),
        I3=m.In(m.Bits[4]),
        I4=m.In(m.Bits[4]),
        I5=m.In(m.Bits[4]),
        I6=m.In(m.Bits[4]),
        I7=m.In(m.Bits[4]),
        S=m.In(m.Bits[3]),
        O=m.Out(m.Bits[4]))
    io.O @= m.mux(
        [io.I0, io.I1, io.I2, io.I3, io.I4, io.I5, io.I6, io.I7], io.S)


if __name__ == "__main__":
    print_verilog(Top2to1, inline=True)
    print_verilog(Top8to1, inline=True)
