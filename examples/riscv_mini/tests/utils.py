import random
import magma as m
from hwtypes import BitVector, Bit
from .opcode import Opcode, Funct3, Funct7
from riscv_mini.instructions import FENCEI, ECALL, EBREAK, ERET
from riscv_mini.csr import CSR


def reg(x):
    return BitVector[5](x & ((1 << 5) - 1))


def imm(x):
    if isinstance(x, int):
        x = BitVector[21](x)
    else:
        assert isinstance(x, BitVector)
        x = x[:21]
    return (x & ((1 << 20) - 1))


def _concat(*args):
    x = args[0]
    if isinstance(x, Bit):
        x = BitVector[1](x)
    if len(args) == 1:
        return x
    return x.concat(_concat(*args[1:]))


def concat(*args):
    # Chisel and magma concats are reversed
    return _concat(*reversed(args))


def B(funct3, rs1, rs2, i):
    return concat(imm(i)[12], imm(i)[5:11], reg(rs2), reg(rs1), funct3,
                  imm(i)[1:5], imm(i)[11], Opcode.BRANCH)


def I(funct3, rd, rs1, i):
    return concat(imm(i)[0:12], reg(rs1), funct3, reg(rd), Opcode.ITYPE)


def SYS(funct3, rd, csr, rs1):
    return concat(csr, reg(rs1), funct3, reg(rd), Opcode.SYSTEM)


def J(rd, i):
    return concat(imm(i)[20], imm(i)[1:11], imm(i)[11], imm(i)[12:20], reg(rd),
                  Opcode.JAL)


def L(funct3, rd, rs1, i):
    if isinstance(i, BitVector) and len(i) < 12:
        i = i.zext(12 - len(i))
    return concat(imm(i)[0:12], reg(rs1), funct3, reg(rd),
                  Opcode.LOAD)


def JR(rd, rs1, i):
    return concat(imm(i)[0:12], reg(rs1), BitVector[3](0), reg(rd),
                  Opcode.JALR)


rand_fn3 = BitVector.random(3)
rand_rs1 = BitVector.random(5) + 1
rand_rs2 = BitVector.random(5) + 1
rand_rd = BitVector.random(5) + 1
rand_inst = BitVector.random(32)


def csr(inst):
    return (inst >> 20)[:12]


def rs1(inst):
    return ((inst >> 15) & 0x1f)[:12]


nop = concat(BitVector[12](0), reg(0), Funct3.ADD, reg(0), Opcode.ITYPE)

rand_fn7 = BitVector.random(7)
fence = concat(
    BitVector[4](0), BitVector[4](0xf), BitVector[4](0xf), BitVector[13](0),
    Opcode.MEMORY
)
rand_csr = random.choice(CSR.regs)

insts = [
    concat(rand_fn7, rand_rs2, rand_rs1, rand_fn3, rand_rd, Opcode.LUI),
    concat(rand_fn7, rand_rs2, rand_rs1, rand_fn3, rand_rd, Opcode.AUIPC),
    concat(rand_fn7, rand_rs2, rand_rs1, rand_fn3, rand_rd, Opcode.JAL),
    concat(rand_fn7, rand_rs2, rand_rs1, BitVector[3](0), rand_rd, Opcode.JALR),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.BEQ, rand_rd, Opcode.BRANCH),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.BNE, rand_rd, Opcode.BRANCH),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.BLT, rand_rd, Opcode.BRANCH),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.BGE, rand_rd, Opcode.BRANCH),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.BLTU, rand_rd, Opcode.BRANCH),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.BGEU, rand_rd, Opcode.BRANCH),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.LB, rand_rd, Opcode.LOAD),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.LH, rand_rd, Opcode.LOAD),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.LW, rand_rd, Opcode.LOAD),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.LBU, rand_rd, Opcode.LOAD),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.LHU, rand_rd, Opcode.LOAD),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.SB, rand_rd, Opcode.STORE),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.SH, rand_rd, Opcode.STORE),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.SW, rand_rd, Opcode.STORE),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.ADD, rand_rd, Opcode.ITYPE),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.SLT, rand_rd, Opcode.ITYPE),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.SLTU, rand_rd, Opcode.ITYPE),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.XOR, rand_rd, Opcode.ITYPE),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.OR, rand_rd, Opcode.ITYPE),
    concat(rand_fn7, rand_rs2, rand_rs1, Funct3.AND, rand_rd, Opcode.ITYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.SLL, rand_rd, Opcode.ITYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.SR, rand_rd, Opcode.ITYPE),
    concat(Funct7.S, rand_rs2, rand_rs1, Funct3.SR, rand_rd, Opcode.ITYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.ADD, rand_rd, Opcode.RTYPE),
    concat(Funct7.S, rand_rs2, rand_rs1, Funct3.ADD, rand_rd, Opcode.RTYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.SLL, rand_rd, Opcode.RTYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.SLT, rand_rd, Opcode.RTYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.SLTU, rand_rd, Opcode.RTYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.XOR, rand_rd, Opcode.RTYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.SR, rand_rd, Opcode.RTYPE),
    concat(Funct7.S, rand_rs2, rand_rs1, Funct3.SR, rand_rd, Opcode.RTYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.OR, rand_rd, Opcode.RTYPE),
    concat(Funct7.U, rand_rs2, rand_rs1, Funct3.AND, rand_rd, Opcode.RTYPE),
    fence, FENCEI.as_bv(),
    concat(rand_csr, rand_rs1, Funct3.CSRRW, rand_rd, Opcode.SYSTEM),
    concat(rand_csr, rand_rs1, Funct3.CSRRS, rand_rd, Opcode.SYSTEM),
    concat(rand_csr, rand_rs1, Funct3.CSRRC, rand_rd, Opcode.SYSTEM),
    concat(rand_csr, rand_rs1, Funct3.CSRRWI, rand_rd, Opcode.SYSTEM),
    concat(rand_csr, rand_rs1, Funct3.CSRRSI, rand_rd, Opcode.SYSTEM),
    concat(rand_csr, rand_rs1, Funct3.CSRRCI, rand_rd, Opcode.SYSTEM),
    ECALL.as_bv(), EBREAK.as_bv(), ERET.as_bv(), nop, rand_inst
]


def inst_31(inst):
    if isinstance(inst, m.BitPattern):
        inst = inst.as_bv()
    return ((inst >> 31) & 0x1)[0]


def inst_30_25(inst):
    if isinstance(inst, m.BitPattern):
        inst = inst.as_bv()
    return ((inst >> 25) & 0x3f)[:6]


def inst_24_21(inst):
    if isinstance(inst, m.BitPattern):
        inst = inst.as_bv()
    return ((inst >> 21) & 0xf)[:4]


def inst_20(inst):
    if isinstance(inst, m.BitPattern):
        inst = inst.as_bv()
    return ((inst >> 20) & 0x1)[0]


def inst_19_12(inst):
    if isinstance(inst, m.BitPattern):
        inst = inst.as_bv()
    return ((inst >> 12) & 0xff)[:8]


def inst_11_8(inst):
    if isinstance(inst, m.BitPattern):
        inst = inst.as_bv()
    return ((inst >> 8) & 0xf)[:4]


def inst_7(inst):
    if isinstance(inst, m.BitPattern):
        inst = inst.as_bv()
    return ((inst >> 7) & 0x1)[0]


def iimm(inst):
    return concat(
        concat(*(inst_31(inst) for _ in range(21))),
        inst_30_25(inst), inst_24_21(inst), inst_20(inst)
    )


def simm(inst):
    return concat(
        concat(*(inst_31(inst) for _ in range(21))),
        inst_30_25(inst), inst_11_8(inst), inst_7(inst)
    )


def bimm(inst):
    return concat(
        concat(*(inst_31(inst) for _ in range(20))),
        inst_7(inst), inst_30_25(inst), inst_11_8(inst), BitVector[1](0)
    )


def uimm(inst):
    return concat(
        inst_31(inst), inst_30_25(inst), inst_24_21(inst),
        inst_20(inst), inst_19_12(inst), BitVector[12](0)
    )


def jimm(inst):
    return concat(
        concat(*(inst_31(inst) for _ in range(12))),
        inst_19_12(inst), inst_20(inst), inst_30_25(inst), inst_24_21(inst),
        BitVector[1](0)
    )


def zimm(inst):
    if isinstance(inst, m.BitPattern):
        inst = inst.as_bv()
    return (inst >> 15) & 0x1f


def S(funct3, rs2, rs1, i):
    return concat(imm(i)[5:12], reg(rs2), reg(rs1), funct3, imm(i)[0:5],
                  Opcode.STORE)


def RU(funct3, rd, rs1, rs2):
    return concat(Funct7.U, reg(rs2), reg(rs1), funct3, reg(rd), Opcode.RTYPE)


def RS(funct3, rd, rs1, rs2):
    return concat(Funct7.S, reg(rs2), reg(rs1), funct3, reg(rd), Opcode.RTYPE)


fin = concat(CSR.mtohost, reg(31), Funct3.CSRRW, reg(0), Opcode.SYSTEM)

bypass_test = [
    I(Funct3.ADD, 1, 0, 1),   # ADDI x1, x0, 1   # x1 <- 1
    S(Funct3.SW, 1, 0, 12),   # SW   x1, x0, 12  # Mem[12] <- 1
    L(Funct3.LW, 2, 0, 12),   # LW   x2, x0, 12  # x2 <- 1
    RU(Funct3.ADD, 3, 2, 2),  # ADD  x3, x2, x2  # x3 <- 2
    RS(Funct3.ADD, 4, 3, 2),  # SUB  x4, x2, x3  # x4 <- 1
    RU(Funct3.SLL, 5, 3, 4),  # SLL  x5, x2, x4  # x5 <- 4
    RU(Funct3.SLT, 6, 4, 5),  # SLT  x6, x4, x5  # x6 <- 1
    B(Funct3.BEQ, 1, 6, 8),   # BEQ  x1, x6, 8   # go to the BGE branch
    J(0, 12),                 # JAL  x0, 12      # skip nop
    B(Funct3.BGE, 4, 1, -4),  # BGE  x4, x1, -4  # go to the jump
    nop, nop,
    RU(Funct3.ADD, 26, 0, 1),  # ADD x26,  x0, x1  # x26 <- 1
    RU(Funct3.ADD, 27, 26, 2),  # ADD x27, x26, x2  # x27 <- 2
    RU(Funct3.ADD, 28, 27, 3),  # ADD x28, x27, x3  # x28 <- 4
    RU(Funct3.ADD, 29, 28, 4),  # ADD x29, x28, x4  # x29 <- 5
    RU(Funct3.ADD, 30, 29, 5),  # ADD x30, x29, x5  # x30 <- 9
    RU(Funct3.ADD, 31, 30, 6),  # ADD x31, x31, x6  # x31 <- 10
    fin
]

exception_test = [
    fence,
    I(Funct3.ADD, 31, 0, 2),  # ADDI x31, x0,  1 # x31 <- 2
    I(Funct3.ADD, 31, 31, 1),  # ADDI x31, x31, 1 # x31 <- 3
    I(Funct3.ADD, 31, 31, 1),  # ADDI x31, x32, 1 # x31 <- 4
    BitVector[32](0),          # exception
    I(Funct3.ADD, 31, 31, 1),  # ADDI x31, x31, 1 # x31 <- 5
    I(Funct3.ADD, 31, 31, 1),  # ADDI x31, x31, 1 # x31 <- 6
    I(Funct3.ADD, 31, 31, 1),  # ADDI x31, x31, 1 # x31 <- 7
    fin
]

tests = {
    "bypass": bypass_test,
    "exception": exception_test
}

test_results = {
    "bypass": 10,
    "exception": 4
}
