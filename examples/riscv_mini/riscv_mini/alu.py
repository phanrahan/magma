import magma as m


class ALUOP(m.Enum):
    ADD = 0
    SUB = 1
    AND = 2
    OR = 3
    XOR = 4
    SLT = 5
    SLL = 6
    SLTU = 7
    SRL = 8
    SRA = 9
    COPY_A = 10
    COPY_B = 11
    XXX = 15


class ALUBase(m.Generator):
    def __init__(self, x_len: int):
        self.io = m.IO(A=m.In(m.UInt[x_len]), B=m.In(m.UInt[x_len]),
                       op=m.In(ALUOP), O=m.Out(m.UInt[x_len]),
                       sum_=m.Out(m.UInt[x_len]))


class ALUSimple(ALUBase):
    def __init__(self, x_len: int):
        super().__init__(x_len)
        io = self.io

        with m.when(io.op == ALUOP.ADD):
            io.O @= io.A + io.B
        with m.elsewhen(io.op == ALUOP.SUB):
            io.O @= io.A - io.B
        with m.elsewhen(io.op == ALUOP.SRA):
            io.O @= m.uint(m.sint(io.A) >> m.sint(io.B))
        with m.elsewhen(io.op == ALUOP.SRL):
            io.O @= io.A >> io.B
        with m.elsewhen(io.op == ALUOP.SLL):
            io.O @= io.A << io.B
        with m.elsewhen(io.op == ALUOP.SLT):
            io.O @= m.uint(m.sint(io.A) < m.sint(io.B), x_len)
        with m.elsewhen(io.op == ALUOP.SLTU):
            io.O @= m.uint(io.A < io.B, x_len)
        with m.elsewhen(io.op == ALUOP.AND):
            io.O @= io.A & io.B
        with m.elsewhen(io.op == ALUOP.OR):
            io.O @= io.A | io.B
        with m.elsewhen(io.op == ALUOP.XOR):
            io.O @= io.A ^ io.B
        with m.elsewhen(io.op == ALUOP.COPY_A):
            io.O @= io.A
        with m.otherwise():
            io.O @= io.B

        io.sum_ @= io.A + m.mux([io.B, -io.B], io.op[0])


class ALUArea(ALUBase):
    def __init__(self, x_len: int):
        super().__init__(x_len)
        io = self.io
        sum_ = io.A + m.mux([io.B, -io.B], io.op[0])
        cmp = m.uint(m.mux([m.mux([io.A[-1], io.B[-1]], io.op[1]), sum_[-1]],
                           io.A[-1] == io.B[-1]), x_len)
        shin = m.mux([io.A[::-1], io.A], io.op[3])
        shiftr = m.uint(m.sint(
            m.concat(shin, io.op[0] & shin[x_len - 1])
        ) >> m.sint(m.zext(io.B, 1)))[:x_len]
        shiftl = shiftr[::-1]

        with m.when((io.op == ALUOP.ADD) | (io.op == ALUOP.SUB)):
            io.O @= sum_
        with m.elsewhen((io.op == ALUOP.SLT) | (io.op == ALUOP.SLTU)):
            io.O @= cmp
        with m.elsewhen((io.op == ALUOP.SRA) | (io.op == ALUOP.SRL)):
            io.O @= shiftr
        with m.elsewhen(io.op == ALUOP.SLL):
            io.O @= shiftl
        with m.elsewhen(io.op == ALUOP.AND):
            io.O @= io.A & io.B
        with m.elsewhen(io.op == ALUOP.OR):
            io.O @= io.A | io.B
        with m.elsewhen(io.op == ALUOP.XOR):
            io.O @= io.A ^ io.B
        with m.elsewhen(io.op == ALUOP.COPY_A):
            io.O @= io.A
        with m.otherwise():
            io.O @= io.B
        io.sum_ @= sum_
