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
        ) + m.ClockIO()
        if has_read_enable:
            self.io += m.IO(ren=m.In(m.Enable))


class RegisterFileWhen(RegisterFile):
    def __init__(self, n: int, T: m.Type, has_read_enable: bool = False):
        super().__init__(n, T, has_read_enable)

        regs = [m.Register(T)() for _ in range(n)]

        rdata = T()
        rdata @= 0
        for i, reg in enumerate(regs):
            with m.when((self.io.waddr == i) & self.io.wen):
                reg.I @= self.io.wdata

            with m.when(self.io.raddr == i):
                rdata @= reg.O

        if has_read_enable:
            rdata = m.Register(T, has_enable=True)()(rdata, self.io.ren)

        self.io.rdata @= rdata


class RegisterFileComprehension(RegisterFile):
    def __init__(self, n: int, T: m.Type, has_read_enable: bool = False):
        super().__init__(n, T, has_read_enable)

        regs = [
            m.Register(T, has_enable=True)()(
                self.io.wdata, (self.io.waddr == i) & self.io.wen
            )
            for i in range(n)
        ]

        rdata = T()
        rdata @= 0
        for i, reg in enumerate(regs):
            with m.when(self.io.raddr == i):
                rdata @= reg

        if has_read_enable:
            rdata = m.Register(T, has_enable=True)()(rdata, self.io.ren)

        self.io.rdata @= rdata


class RegisterFileBraid(RegisterFile):
    def __init__(self, n: int, T: m.Type, has_read_enable: bool = False):
        super().__init__(n, T, has_read_enable)

        enables = m.array(
            [(self.io.waddr == i) & self.io.wen for i in range(n)]
        )
        regs = m.braid(
            [m.Register(T, has_enable=True)() for _ in range(n)],
            forkargs=['I']
        )(self.io.wdata, enables)

        rdata = T()
        rdata @= 0
        for i, reg in enumerate(regs):
            with m.when(self.io.raddr == i):
                rdata @= reg

        if has_read_enable:
            rdata = m.Register(T, has_enable=True)()(rdata, self.io.ren)

        self.io.rdata @= rdata
