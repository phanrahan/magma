import magma as m


class RegFile(m.Generator2):
    """
    Basic two read port, one write port register file

    Register at address 0 always holds the value 0
    """

    def __init__(self, x_len: int):
        self.io = io = m.IO(
            raddr1=m.In(m.UInt[5]),
            raddr2=m.In(m.UInt[5]),
            rdata1=m.Out(m.UInt[x_len]),
            rdata2=m.Out(m.UInt[x_len]),
            wen=m.In(m.Enable),
            waddr=m.In(m.UInt[5]),
            wdata=m.In(m.UInt[x_len])
        ) + m.ClockIO(has_reset=True)
        regs = m.MultiportMemory(32, m.UInt[x_len], num_read_ports=2)()
        regs.RADDR_0 @= io.raddr1
        regs.RADDR_1 @= io.raddr2
        io.rdata1 @= m.mux([0, regs.RDATA_0], io.raddr1.reduce_or())
        io.rdata2 @= m.mux([0, regs.RDATA_1], io.raddr2.reduce_or())
        wen = m.bit(io.wen) & io.waddr.reduce_or()
        regs.WADDR_0 @= io.waddr
        regs.WDATA_0 @= io.wdata
        regs.WE_0 @= wen
