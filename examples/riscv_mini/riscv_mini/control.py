from hwtypes import BitVector as BV
import magma as m

from riscv_mini.instructions import (
    LB, LH, LW, LBU, LHU, SB, SH, SW, SLL, SLLI, SRL, SRLI, SRA, SRAI, ADD,
    ADDI, SUB, LUI, AUIPC, XOR, XORI, OR, ORI, AND, ANDI, SLT, SLTI, SLTU,
    SLTIU, BEQ, BNE, BLT, BGE, BLTU, BGEU, JAL, JALR, FENCE, FENCEI, CSRRW,
    CSRRS, CSRRC, CSRRWI, CSRRSI, CSRRCI, ECALL, EBREAK, ERET, WFI)
from riscv_mini.alu import ALUOP
from riscv_mini.csr import CSR

ALU_ADD = ALUOP.ADD
ALU_SUB = ALUOP.SUB
ALU_AND = ALUOP.AND
ALU_OR = ALUOP.OR
ALU_XOR = ALUOP.XOR
ALU_SLT = ALUOP.SLT
ALU_SLL = ALUOP.SLL
ALU_SLTU = ALUOP.SLTU
ALU_SRL = ALUOP.SRL
ALU_SRA = ALUOP.SRA
ALU_COPY_A = ALUOP.COPY_A
ALU_COPY_B = ALUOP.COPY_B
ALU_XXX = ALUOP.XXX

Y = True
N = False

# pc_sel
PC_4 = BV[2](0)
PC_ALU = BV[2](1)
PC_0 = BV[2](2)
PC_EPC = BV[2](3)

# A_sel
A_XXX = BV[1](0)
A_PC = BV[1](0)
A_RS1 = BV[1](1)

# B_sel
B_XXX = BV[1](0)
B_IMM = BV[1](0)
B_RS2 = BV[1](1)

# imm_sel
IMM_X = BV[3](0)
IMM_I = BV[3](1)
IMM_S = BV[3](2)
IMM_U = BV[3](3)
IMM_J = BV[3](4)
IMM_B = BV[3](5)
IMM_Z = BV[3](6)

# br_type
BR_XXX = BV[3](0)
BR_LTU = BV[3](1)
BR_LT = BV[3](2)
BR_EQ = BV[3](3)
BR_GEU = BV[3](4)
BR_GE = BV[3](5)
BR_NE = BV[3](6)

# st_type
ST_XXX = BV[2](0)
ST_SW = BV[2](1)
ST_SH = BV[2](2)
ST_SB = BV[2](3)

# ld_type
LD_XXX = BV[3](0)
LD_LW = BV[3](1)
LD_LH = BV[3](2)
LD_LB = BV[3](3)
LD_LHU = BV[3](4)
LD_LBU = BV[3](5)

# wb_sel
WB_ALU = BV[2](0)
WB_MEM = BV[2](1)
WB_PC4 = BV[2](2)
WB_CSR = BV[2](3)


def make_ControlIO(x_len):
    return m.IO(inst=m.In(m.UInt[x_len]),
                pc_sel=m.Out(m.UInt[2]),
                inst_kill=m.Out(m.Bit),
                A_sel=m.Out(m.UInt[1]),
                B_sel=m.Out(m.UInt[1]),
                imm_sel=m.Out(m.UInt[3]),
                alu_op=m.Out(m.UInt[4]),
                br_type=m.Out(m.UInt[3]),
                st_type=m.Out(m.UInt[2]),
                ld_type=m.Out(m.UInt[3]),
                wb_sel=m.Out(m.UInt[2]),
                wb_en=m.Out(m.Bit),
                csr_cmd=m.Out(m.UInt[3]),
                illegal=m.Out(m.Bit))


#                                                     kill
#          pc_sel A_sel  B_sel imm_sel  alu_op br_type |  st_type ld_type
#            |      |      |     |       |       |     |     |       |
default = (PC_4, A_XXX, B_XXX, IMM_X, ALU_XXX, BR_XXX, N, ST_XXX, LD_XXX,
           #      wb_en    illegal?
           # wb_sel| csr_cmd |
           #   |   |    |    |
           WB_ALU, N, CSR.N, Y)
inst_map = {
    LUI: (PC_4, A_PC, B_IMM, IMM_U, ALU_COPY_B, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    AUIPC: (PC_4, A_PC, B_IMM, IMM_U, ALU_ADD, BR_XXX, N, ST_XXX, LD_XXX,
            WB_ALU, Y, CSR.N, N),
    JAL: (PC_ALU, A_PC, B_IMM, IMM_J, ALU_ADD, BR_XXX, Y, ST_XXX, LD_XXX,
          WB_PC4, Y, CSR.N, N),
    JALR: (PC_ALU, A_RS1, B_IMM, IMM_I, ALU_ADD, BR_XXX, Y, ST_XXX, LD_XXX,
           WB_PC4, Y, CSR.N, N),
    BEQ: (PC_4, A_PC, B_IMM, IMM_B, ALU_ADD, BR_EQ, N, ST_XXX, LD_XXX, WB_ALU,
          N, CSR.N, N),
    BNE: (PC_4, A_PC, B_IMM, IMM_B, ALU_ADD, BR_NE, N, ST_XXX, LD_XXX, WB_ALU,
          N, CSR.N, N),
    BLT: (PC_4, A_PC, B_IMM, IMM_B, ALU_ADD, BR_LT, N, ST_XXX, LD_XXX, WB_ALU,
          N, CSR.N, N),
    BGE: (PC_4, A_PC, B_IMM, IMM_B, ALU_ADD, BR_GE, N, ST_XXX, LD_XXX, WB_ALU,
          N, CSR.N, N),
    BLTU: (PC_4, A_PC, B_IMM, IMM_B, ALU_ADD, BR_LTU, N, ST_XXX, LD_XXX,
           WB_ALU, N, CSR.N, N),
    BGEU: (PC_4, A_PC, B_IMM, IMM_B, ALU_ADD, BR_GEU, N, ST_XXX, LD_XXX,
           WB_ALU, N, CSR.N, N),
    LB: (PC_0, A_RS1, B_IMM, IMM_I, ALU_ADD, BR_XXX, Y, ST_XXX, LD_LB, WB_MEM,
         Y, CSR.N, N),
    LH: (PC_0, A_RS1, B_IMM, IMM_I, ALU_ADD, BR_XXX, Y, ST_XXX, LD_LH, WB_MEM,
         Y, CSR.N, N),
    LW: (PC_0, A_RS1, B_IMM, IMM_I, ALU_ADD, BR_XXX, Y, ST_XXX, LD_LW, WB_MEM,
         Y, CSR.N, N),
    LBU: (PC_0, A_RS1, B_IMM, IMM_I, ALU_ADD, BR_XXX, Y, ST_XXX, LD_LBU,
          WB_MEM, Y, CSR.N, N),
    LHU: (PC_0, A_RS1, B_IMM, IMM_I, ALU_ADD, BR_XXX, Y, ST_XXX, LD_LHU,
          WB_MEM, Y, CSR.N, N),
    SB: (PC_4, A_RS1, B_IMM, IMM_S, ALU_ADD, BR_XXX, N, ST_SB, LD_XXX, WB_ALU,
         N, CSR.N, N),
    SH: (PC_4, A_RS1, B_IMM, IMM_S, ALU_ADD, BR_XXX, N, ST_SH, LD_XXX, WB_ALU,
         N, CSR.N, N),
    SW: (PC_4, A_RS1, B_IMM, IMM_S, ALU_ADD, BR_XXX, N, ST_SW, LD_XXX, WB_ALU,
         N, CSR.N, N),
    ADDI: (PC_4, A_RS1, B_IMM, IMM_I, ALU_ADD, BR_XXX, N, ST_XXX, LD_XXX,
           WB_ALU, Y, CSR.N, N),
    SLTI: (PC_4, A_RS1, B_IMM, IMM_I, ALU_SLT, BR_XXX, N, ST_XXX, LD_XXX,
           WB_ALU, Y, CSR.N, N),
    SLTIU: (PC_4, A_RS1, B_IMM, IMM_I, ALU_SLTU, BR_XXX, N, ST_XXX, LD_XXX,
            WB_ALU, Y, CSR.N, N),
    XORI: (PC_4, A_RS1, B_IMM, IMM_I, ALU_XOR, BR_XXX, N, ST_XXX, LD_XXX,
           WB_ALU, Y, CSR.N, N),
    ORI: (PC_4, A_RS1, B_IMM, IMM_I, ALU_OR, BR_XXX, N, ST_XXX, LD_XXX, WB_ALU,
          Y, CSR.N, N),
    ANDI: (PC_4, A_RS1, B_IMM, IMM_I, ALU_AND, BR_XXX, N, ST_XXX, LD_XXX,
           WB_ALU, Y, CSR.N, N),
    SLLI: (PC_4, A_RS1, B_IMM, IMM_I, ALU_SLL, BR_XXX, N, ST_XXX, LD_XXX,
           WB_ALU, Y, CSR.N, N),
    SRLI: (PC_4, A_RS1, B_IMM, IMM_I, ALU_SRL, BR_XXX, N, ST_XXX, LD_XXX,
           WB_ALU, Y, CSR.N, N),
    SRAI: (PC_4, A_RS1, B_IMM, IMM_I, ALU_SRA, BR_XXX, N, ST_XXX, LD_XXX,
           WB_ALU, Y, CSR.N, N),
    ADD: (PC_4, A_RS1, B_RS2, IMM_X, ALU_ADD, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    SUB: (PC_4, A_RS1, B_RS2, IMM_X, ALU_SUB, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    SLL: (PC_4, A_RS1, B_RS2, IMM_X, ALU_SLL, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    SLT: (PC_4, A_RS1, B_RS2, IMM_X, ALU_SLT, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    SLTU: (PC_4, A_RS1, B_RS2, IMM_X, ALU_SLTU, BR_XXX, N, ST_XXX, LD_XXX,
           WB_ALU, Y, CSR.N, N),
    XOR: (PC_4, A_RS1, B_RS2, IMM_X, ALU_XOR, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    SRL: (PC_4, A_RS1, B_RS2, IMM_X, ALU_SRL, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    SRA: (PC_4, A_RS1, B_RS2, IMM_X, ALU_SRA, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    OR: (PC_4, A_RS1, B_RS2, IMM_X, ALU_OR, BR_XXX, N, ST_XXX, LD_XXX, WB_ALU,
         Y, CSR.N, N),
    AND: (PC_4, A_RS1, B_RS2, IMM_X, ALU_AND, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, Y, CSR.N, N),
    FENCE: (PC_4, A_XXX, B_XXX, IMM_X, ALU_XXX, BR_XXX, N, ST_XXX, LD_XXX,
            WB_ALU, N, CSR.N, N),
    FENCEI: (PC_0, A_XXX, B_XXX, IMM_X, ALU_XXX, BR_XXX, Y, ST_XXX, LD_XXX,
             WB_ALU, N, CSR.N, N),
    CSRRW: (PC_0, A_RS1, B_XXX, IMM_X, ALU_COPY_A, BR_XXX, Y, ST_XXX, LD_XXX,
            WB_CSR, Y, CSR.W, N),
    CSRRS: (PC_0, A_RS1, B_XXX, IMM_X, ALU_COPY_A, BR_XXX, Y, ST_XXX, LD_XXX,
            WB_CSR, Y, CSR.S, N),
    CSRRC: (PC_0, A_RS1, B_XXX, IMM_X, ALU_COPY_A, BR_XXX, Y, ST_XXX, LD_XXX,
            WB_CSR, Y, CSR.C, N),
    CSRRWI: (PC_0, A_XXX, B_XXX, IMM_Z, ALU_XXX, BR_XXX, Y, ST_XXX, LD_XXX,
             WB_CSR, Y, CSR.W, N),
    CSRRSI: (PC_0, A_XXX, B_XXX, IMM_Z, ALU_XXX, BR_XXX, Y, ST_XXX, LD_XXX,
             WB_CSR, Y, CSR.S, N),
    CSRRCI: (PC_0, A_XXX, B_XXX, IMM_Z, ALU_XXX, BR_XXX, Y, ST_XXX, LD_XXX,
             WB_CSR, Y, CSR.C, N),
    ECALL: (PC_4, A_XXX, B_XXX, IMM_X, ALU_XXX, BR_XXX, N, ST_XXX, LD_XXX,
            WB_CSR, N, CSR.P, N),
    EBREAK: (PC_4, A_XXX, B_XXX, IMM_X, ALU_XXX, BR_XXX, N, ST_XXX, LD_XXX,
             WB_CSR, N, CSR.P, N),
    ERET: (PC_EPC, A_XXX, B_XXX, IMM_X, ALU_XXX, BR_XXX, Y, ST_XXX, LD_XXX,
           WB_CSR, N, CSR.P, N),
    WFI: (PC_4, A_XXX, B_XXX, IMM_X, ALU_XXX, BR_XXX, N, ST_XXX, LD_XXX,
          WB_ALU, N, CSR.N, N),
}


class Control(m.Generator2):
    def __init__(self, x_len):
        self.io = io = make_ControlIO(x_len)

        ctrl_signals = m.dict_lookup(inst_map, io.inst, default=default)

        # Control signals for Fetch
        io.pc_sel @= ctrl_signals[0]
        io.inst_kill @= ctrl_signals[6]

        # Control signals for Execute
        io.A_sel @= ctrl_signals[1]
        io.B_sel @= ctrl_signals[2]
        io.imm_sel @= ctrl_signals[3]
        io.alu_op @= ctrl_signals[4]
        io.br_type @= ctrl_signals[5]
        io.st_type @= ctrl_signals[7]

        # Control signals for Write Back
        io.ld_type @= ctrl_signals[8]
        io.wb_sel @= ctrl_signals[9]
        io.wb_en @= ctrl_signals[10]
        io.csr_cmd @= ctrl_signals[11]
        io.illegal @= ctrl_signals[12]
