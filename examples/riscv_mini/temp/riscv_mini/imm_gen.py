from functools import reduce

import magma as m
from riscv_mini.control import IMM_I, IMM_S, IMM_B, IMM_U, IMM_J, IMM_Z


class ImmGen(m.Generator2):
    def __init__(self, x_len):
        self.io = m.IO(
            inst=m.In(m.UInt[x_len]),
            sel=m.In(m.UInt[3]),
            O=m.Out(m.UInt[x_len])
        )


class ImmGenWire(ImmGen):
    def __init__(self, x_len):
        super().__init__(x_len)
        inst = self.io.inst
        Iimm = m.sext_to(m.sint(inst[20:32]), x_len)
        Simm = m.sext_to(m.sint(m.concat(inst[7:12], inst[25:32])), x_len)
        Bimm = m.sext_to(m.sint(m.concat(
            m.bits(0, 1), inst[8:12], inst[25:31], inst[7], inst[31]
        )), x_len)
        Uimm = m.concat(m.bits(0, 12), inst[12:32])
        Jimm = m.sext_to(m.sint(m.concat(
            m.bits(0, 1), inst[21:25], inst[25:31], inst[20], inst[12:20],
            inst[31]
        )), x_len)
        Zimm = m.sint(m.zext_to(inst[15:20], x_len))

        self.io.O @= m.uint(m.dict_lookup({
            IMM_I: Iimm,
            IMM_S: Simm,
            IMM_B: Bimm,
            IMM_U: Uimm,
            IMM_J: Jimm,
            IMM_Z: Zimm
        }, self.io.sel, Iimm & -2))


class ImmGenMux(ImmGen):
    def __init__(self, x_len):
        super().__init__(x_len)
        inst = self.io.inst
        sel = self.io.sel

        is_i = sel == IMM_I
        is_s = sel == IMM_S
        is_b = sel == IMM_B
        is_u = sel == IMM_U
        is_j = sel == IMM_J
        is_z = sel == IMM_Z

        sign = is_z.ite(0, inst[31:32])

        b0_1 = is_s.ite(
            inst[7:8],
            is_i.ite(
                inst[20:21],
                is_z.ite(inst[15:16], 0)
            )
        )

        b1_5 = is_u.ite(
            0,
            (is_s | is_b).ite(
                inst[8:12],
                is_z.ite(inst[16:20], inst[21:25])
            )
        )

        b5_11 = (is_u | is_z).ite(0, inst[25:31])

        b11_12 = (is_u | is_z).ite(
            0,
            is_j.ite(
                inst[20:21],
                is_b.ite(inst[7:8], sign)
            )
        )

        # the reference impl inverts this mux with (!is_u & !is_j)
        b12_20 = (is_u | is_j).ite(inst[12:20], sign.repeat(8))

        b20_31 = is_u.ite(inst[20:31], sign.repeat(11))

        self.io.O @= m.uint(
            reduce(m.Bits.concat,
                   [b0_1, b1_5, b5_11, b11_12, b12_20, b20_31, sign]))
