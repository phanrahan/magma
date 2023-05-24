import magma as m


from riscv_mini.control import BR_EQ, BR_NE, BR_LT, BR_GE, BR_LTU, BR_GEU


class BrCond(m.Generator2):
    def __init__(self, x_len):
        self.io = m.IO(
            rs1=m.In(m.UInt[x_len]),
            rs2=m.In(m.UInt[x_len]),
            br_type=m.In(m.UInt[3]),
            taken=m.Out(m.Bit)
        )


class BrCondSimple(BrCond):
    def __init__(self, x_len):
        super().__init__(x_len)
        io = self.io
        eq = io.rs1 == io.rs2
        neq = ~eq
        lt = m.sint(io.rs1) < m.sint(io.rs2)
        ge = ~lt
        ltu = io.rs1 < io.rs2
        geu = ~ltu
        io.taken @= (
            ((io.br_type == BR_EQ) & eq) |
            ((io.br_type == BR_NE) & neq) |
            ((io.br_type == BR_LT) & lt) |
            ((io.br_type == BR_GE) & ge) |
            ((io.br_type == BR_LTU) & ltu) |
            ((io.br_type == BR_GEU) & geu)
        )


class BrCondArea(BrCond):
    def __init__(self, x_len):
        super().__init__(x_len)
        io = self.io
        diff = io.rs1 - io.rs2
        neq = diff.reduce_or()
        eq = ~neq
        is_same_sign = io.rs1[-1] == io.rs2[-1]
        lt = m.mux([io.rs1[-1], diff[-1]], is_same_sign)
        ltu = m.mux([io.rs2[-1], diff[-1]], is_same_sign)
        ge = ~lt
        geu = ~ltu
        io.taken @= (
            ((io.br_type == BR_EQ) & eq) |
            ((io.br_type == BR_NE) & neq) |
            ((io.br_type == BR_LT) & lt) |
            ((io.br_type == BR_GE) & ge) |
            ((io.br_type == BR_LTU) & ltu) |
            ((io.br_type == BR_GEU) & geu)
        )
