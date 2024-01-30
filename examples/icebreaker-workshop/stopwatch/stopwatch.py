import magma as m


class bcd8_increment(m.Circuit):
    io = m.IO(din=m.In(m.UInt[8]), dout=m.Out(m.UInt[8]))
    with m.when(io.din == 99):
        io.dout @= 0
    with m.elsewhen(io.din[:4] == 9):
        io.dout @= m.concat(m.UInt[4](0), io.din[4:] + 1)
    with m.otherwise():
        io.dout @= m.concat(io.din[:4] + 1, io.din[4:])


class seven_seg_hex(m.Circuit):
    io = m.IO(din=m.In(m.Bits[4]), dout=m.Out(m.Bits[7]))
    # TODO: Could add T arg to dict lookup or magma dict constructor for T to
    # avoid T literal here
    io.dout @= m.list_lookup([
        m.Bits[7](0b0111111),
        m.Bits[7](0b0000110),
        m.Bits[7](0b1011011),
        m.Bits[7](0b1001111),
        m.Bits[7](0b1100110),
        m.Bits[7](0b1101101),
        m.Bits[7](0b1111101),
        m.Bits[7](0b0000111),
        m.Bits[7](0b1111111),
        m.Bits[7](0b1101111),
        m.Bits[7](0b1110111),
        m.Bits[7](0b1111100),
        m.Bits[7](0b0111001),
        m.Bits[7](0b1011110),
        m.Bits[7](0b1111001),
        m.Bits[7](0b1110001)
    ], io.din, default=0b1000000)


class seven_seg_ctrl(m.Circuit):
    io = m.IO(CLK=m.In(m.Clock),
              din=m.In(m.Bits[8]),
              dout=m.Out(m.Bits[8]))
    dout_reg = m.Register(m.Bits[8])()
    io.dout @= dout_reg

    msb_digit = seven_seg_hex()(io.din[4:])
    lsb_digit = seven_seg_hex()(io.din[:4])

    clkdiv = m.mantle.Counter(2 ** 10)()
    clkdiv_pulse = m.Register(m.Bit)()
    msb_not_lsb = m.Register(m.Bit)()

    clkdiv_pulse.I @= clkdiv.O.reduce_and()
    msb_not_lsb.I @= msb_not_lsb.O ^ clkdiv_pulse.O

    # TODO: Double check synchronous logic here
    with m.when(clkdiv_pulse.O):
        with m.when(msb_not_lsb.O):
            dout_reg.I[:7] @= ~msb_digit
            dout_reg.I[7] @= 0
        with m.otherwise():
            dout_reg.I[:7] @= ~lsb_digit
            dout_reg.I[7] @= 1


class top(m.Circuit):
    io = m.IO(
        CLK=m.In(m.Clock),
        BTN_N=m.In(m.Bit),
        BTN1=m.In(m.Bit),
        BTN2=m.In(m.Bit),
        BTN3=m.In(m.Bit),

        LED1=m.Out(m.Bit),
        LED2=m.Out(m.Bit),
        LED3=m.Out(m.Bit),
        LED4=m.Out(m.Bit),
        LED5=m.Out(m.Bit),

        P1A1=m.Out(m.Bit),
        P1A2=m.Out(m.Bit),
        P1A3=m.Out(m.Bit),
        P1A4=m.Out(m.Bit),
        P1A7=m.Out(m.Bit),
        P1A8=m.Out(m.Bit),
        P1A9=m.Out(m.Bit),
        P1A10=m.Out(m.Bit)
    )

    seven_segment = m.array(
        list(reversed([io.P1A10, io.P1A9, io.P1A8, io.P1A7, io.P1A4, io.P1A3,
                       io.P1A2, io.P1A1]))
    )

    display_value = m.Register(m.Bits[8])()
    display_value_inc = m.Bits[8]()

    lap_value = m.Register(m.Bits[8])()
    lap_timeout = m.Register(m.Bits[5])()

    clkdiv = m.mantle.Counter(1200000, has_cout=True)()
    clkdiv_pulse = clkdiv.COUT

    with m.when(clkdiv_pulse & (lap_timeout.O != 0)):
        lap_timeout.I @= lap_timeout.O - 1

    running = m.Register(m.Bit)()

    with m.when(clkdiv_pulse & running.O):
        display_value.I @= display_value_inc

    with m.when(~io.BTN_N):
        display_value.I @= 0
        running.I @= 0
        lap_timeout.I @= 0

    with m.when(io.BTN3):
        running.I @= 1

    with m.when(io.BTN1):
        running.I @= 0

    with m.when(io.BTN2):
        lap_value.I @= display_value.O
        lap_timeout.I @= 20

    io.LED1 @= io.BTN1 & io.BTN2
    io.LED2 @= io.BTN1 & io.BTN3
    io.LED3 @= io.BTN2 & io.BTN3
    io.LED4 @= ~io.BTN_N
    io.LED5 @= ~io.BTN_N | io.BTN1 | io.BTN2 | io.BTN3

    display_value_inc @= bcd8_increment()(display_value.O)
    # TODO: .ite() on Bits type doesn't work with mlir, have to do truth check
    # explicitly
    # seven_segment @= seven_seg_ctrl()(lap_timeout.O.ite(lap_value.O[:8],
    #                                                     display_value.O[:8]),
    #                                   CLK=io.CLK)
    seven_segment @= seven_seg_ctrl()(
        (lap_timeout.O != 0).ite(lap_value.O[:8], display_value.O[:8]),
        CLK=io.CLK
    )


if __name__ == "__main__":
    m.compile("stopwatch", top, output="mlir-verilog", sv=True,
              disallow_local_variables=True)
