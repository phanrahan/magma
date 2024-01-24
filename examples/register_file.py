import magma as m


class RegisterFile(m.Generator):
    def __init__(self, n: int, T: m.Type, has_read_enable: bool = False):
        addr_len = m.bitutils.clog2(n)
        self.io = m.IO(
            raddr=m.In(m.Bits[addr_len]),
            rdata=m.Out(T),
            wen=m.In(m.Enable),
            waddr=m.In(m.Bits[addr_len]),
            wdata=m.In(T)
        )
        rdata = T()
        if has_read_enable:
            self.io += m.IO(ren=m.In(m.Enable))
            m.Register(T)()(rdata)

        regs = [m.Register(T)() for _ in range(n)]

        rdata @= 0  # default 0
        for i, reg in enumerate(regs):
            with m.when((self.io.waddr == i) & self.io.wen):
                reg.I @= self.io.wdata

            read_cond = self.io.raddr == i
            if has_read_enable:
                read_cond &= self.io.ren
            with m.when(read_cond):
                rdata @= reg.O

        self.io.rdata @= rdata
