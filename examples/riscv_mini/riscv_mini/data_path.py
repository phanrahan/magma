import magma as m
from hwtypes import UIntVector


from riscv_mini.alu import ALUArea
from riscv_mini.csr_gen import CSRGen
from riscv_mini.control import (make_ControlIO, PC_EPC, PC_0, PC_ALU, WB_ALU,
                                A_RS1, B_RS2, ST_SW, ST_SH, ST_SB, IMM_Z,
                                LD_LH, LD_LHU, LD_LB, LD_LBU, WB_MEM, WB_PC4,
                                WB_CSR)
from riscv_mini.const import Const
from riscv_mini.cache import make_CacheIO
from riscv_mini.imm_gen import ImmGenWire
import riscv_mini.instructions as Instructions
from riscv_mini.reg_file import RegFile
from riscv_mini.br_cond import BrCondArea


def make_HostIO(x_len):
    class HostIO(m.Product):
        fromhost = m.In(m.Valid[m.UInt[x_len]])
        tohost = m.Out(m.UInt[x_len])
    return HostIO


def make_DatapathIO(x_len):
    control_decl = make_ControlIO(x_len).decl()
    control_ports = {k: v for k, v in zip(control_decl[::2],
                                          control_decl[1::2])}
    return m.IO(
        host=make_HostIO(x_len),
        icache=m.Flip(make_CacheIO(x_len)),
        dcache=m.Flip(make_CacheIO(x_len)),
        ctrl=m.Flip(m.Product.from_fields("ControlIO", control_ports))
    )


class Datapath(m.Generator2):
    def __init__(self, x_len, ALU=ALUArea, ImmGen=ImmGenWire,
                 BrCond=BrCondArea):
        self.io = make_DatapathIO(x_len) + m.ClockIO(has_reset=True)
        csr = CSRGen(x_len)()
        reg_file = RegFile(x_len)()
        alu = ALU(x_len)()
        imm_gen = ImmGen(x_len)()
        br_cond = BrCondArea(x_len)()

        # Fetch / Execute Registers
        fe_inst = m.Register(
            init=Instructions.NOP,
            has_enable=True,
            reset_type=m.Reset
        )()
        fe_pc = m.Register(m.UInt[x_len], has_enable=True)()

        # Execute / Write Back Registers
        ew_inst = m.Register(init=Instructions.NOP, reset_type=m.Reset)()
        ew_pc = m.Register(m.UInt[x_len])()
        ew_alu = m.Register(m.UInt[x_len])()
        csr_in = m.Register(m.UInt[x_len])()

        # Control signals
        st_type = m.Register(type(self.io.ctrl.st_type).undirected_t)()
        ld_type = m.Register(type(self.io.ctrl.ld_type).undirected_t)()
        wb_sel = m.Register(type(self.io.ctrl.wb_sel).undirected_t)()
        wb_en = m.Register(m.Bit)()
        csr_cmd = m.Register(type(self.io.ctrl.csr_cmd).undirected_t)()
        illegal = m.Register(m.Bit)()
        pc_check = m.Register(m.Bit)()

        # Fetch
        started = m.Register(m.Bit)()(m.bit(self.io.RESET))
        stall = ~self.io.icache.resp.valid | ~self.io.dcache.resp.valid
        pc = m.Register(
            init=UIntVector[x_len](Const.PC_START) - UIntVector[x_len](4),
            reset_type=m.Reset
        )()
        take_sum = m.Bit(name="take_sum")
        take_sum @= (self.io.ctrl.pc_sel == PC_ALU) | br_cond.taken
        npc = m.mux([
            m.mux([
                m.mux([
                    m.mux([
                        m.mux([
                            pc.O + m.uint(4, x_len),
                            pc.O
                        ], self.io.ctrl.pc_sel == PC_0),
                        alu.sum_ >> 1 << 1
                    ], take_sum),
                    csr.epc
                ], self.io.ctrl.pc_sel == PC_EPC),
                csr.evec
            ], csr.expt),
            pc.O
        ], stall)

        is_nop = m.Bit(name="is_nop")
        is_nop @= started | self.io.ctrl.inst_kill | br_cond.taken | csr.expt
        inst = m.mux([
            self.io.icache.resp.data.data,
            Instructions.NOP
        ], is_nop)

        pc.I @= npc
        self.io.icache.req.data.addr @= npc
        self.io.icache.req.data.data @= 0
        self.io.icache.req.data.mask @= 0
        self.io.icache.req.valid @= ~stall
        self.io.icache.abort @= False

        fe_pc.I @= pc.O
        fe_pc.CE @= m.enable(~stall)
        fe_inst.I @= inst
        fe_inst.CE @= m.enable(~stall)

        # Execute
        # Decode
        self.io.ctrl.inst @= fe_inst.O

        # reg_file read
        rs1_addr = fe_inst.O[15:20]
        rs2_addr = fe_inst.O[20:25]
        reg_file.raddr1 @= rs1_addr
        reg_file.raddr2 @= rs2_addr

        # gen immediates
        imm_gen.inst @= fe_inst.O
        imm_gen.sel @= self.io.ctrl.imm_sel

        # bypass
        wb_rd_addr = ew_inst.O[7:12]
        rs1_hazard = m.Bit(name="rs1_hazard")
        rs1_hazard @= (
            wb_en.O & rs1_addr.reduce_or() & (rs1_addr == wb_rd_addr) &
            (wb_sel.O == WB_ALU)
        )
        rs2_hazard = m.Bit(name="rs2_hazard")
        rs2_hazard @= (
            wb_en.O & rs2_addr.reduce_or() & (rs2_addr == wb_rd_addr) &
            (wb_sel.O == WB_ALU)
        )
        rs1 = m.mux([reg_file.rdata1, ew_alu.O], rs1_hazard)
        rs2 = m.mux([reg_file.rdata2, ew_alu.O], rs2_hazard)

        # ALU operations
        alu.A @= m.mux([fe_pc.O, rs1], self.io.ctrl.A_sel == A_RS1)
        alu.B @= m.mux([imm_gen.O, rs2], self.io.ctrl.B_sel == B_RS2)
        alu.op @= self.io.ctrl.alu_op

        # Branch condition calc
        br_cond.rs1 @= rs1
        br_cond.rs2 @= rs2
        br_cond.br_type @= self.io.ctrl.br_type

        # D$ access
        daddr = m.mux([alu.sum_, ew_alu.O], stall) >> 2 << 2
        w_offset = ((m.bits(alu.sum_[1], x_len) << 4) |
                    (m.bits(alu.sum_[0], x_len) << 3))
        self.io.dcache.req.valid @= ~stall & (self.io.ctrl.st_type.reduce_or() |
                                              self.io.ctrl.ld_type.reduce_or())
        self.io.dcache.req.data.addr @= daddr
        self.io.dcache.req.data.data @= rs2 << w_offset
        self.io.dcache.req.data.mask @= m.dict_lookup({
            ST_SW: m.bits(0b1111, 4),
            ST_SH: m.bits(0b11, 4) << m.zext(alu.sum_[0:2], 2),
            ST_SB: m.bits(0b1, 4) << m.zext(alu.sum_[0:2], 2),
        }, m.mux([self.io.ctrl.st_type, st_type.O], stall), m.bits(0, 4))

        # Pipelining
        ew_pc.I @= ew_pc.O
        ew_inst.I @= ew_inst.O
        ew_alu.I @= ew_alu.O
        csr_in.I @= csr_in.O
        st_type.I @= st_type.O
        ld_type.I @= ld_type.O
        wb_sel.I @= wb_sel.O
        wb_en.I @= wb_en.O
        csr_cmd.I @= csr_cmd.O
        illegal.I @= illegal.O
        pc_check.I @= pc_check.O
        with m.when(m.bit(self.io.RESET) | ~stall & csr.expt):
            st_type.I @= 0
            ld_type.I @= 0
            wb_en.I @= 0
            csr_cmd.I @= 0
            illegal.I @= False
            pc_check.I @= False
        with m.elsewhen(~stall & ~csr.expt):
            ew_pc.I @= fe_pc.O
            ew_inst.I @= fe_inst.O
            ew_alu.I @= alu.O
            csr_in.I @= m.mux([rs1, imm_gen.O],
                              self.io.ctrl.imm_sel == IMM_Z)
            st_type.I @= self.io.ctrl.st_type
            ld_type.I @= self.io.ctrl.ld_type
            wb_sel.I @= self.io.ctrl.wb_sel
            wb_en.I @= self.io.ctrl.wb_en
            csr_cmd.I @= self.io.ctrl.csr_cmd
            illegal.I @= self.io.ctrl.illegal
            pc_check.I @= self.io.ctrl.pc_sel == PC_ALU

        # Load
        l_offset = ((m.uint(ew_alu.O[1], x_len) << 4) |
                    (m.uint(ew_alu.O[0], x_len) << 3))
        l_shift = self.io.dcache.resp.data.data >> l_offset
        load = m.dict_lookup({
            LD_LH: m.sext_to(m.sint(l_shift[0:16]), x_len),
            LD_LHU: m.sint(m.zext_to(l_shift[0:16], x_len)),
            LD_LB: m.sext_to(m.sint(l_shift[0:8]), x_len),
            LD_LBU: m.sint(m.zext_to(l_shift[0:8], x_len))
        }, ld_type.O, m.sint(self.io.dcache.resp.data.data))

        # CSR access
        csr.stall @= stall
        csr.I @= csr_in.O
        csr.cmd @= csr_cmd.O
        csr.inst @= ew_inst.O
        csr.pc @= ew_pc.O
        csr.addr @= ew_alu.O
        csr.illegal @= illegal.O
        csr.pc_check @= pc_check.O
        csr.ld_type @= ld_type.O
        csr.st_type @= st_type.O
        self.io.host @= csr.host

        # Regfile write
        reg_write = m.dict_lookup({
            WB_MEM: m.uint(load),
            WB_PC4: (ew_pc.O + 4),
            WB_CSR: csr.O
        }, wb_sel.O, ew_alu.O)

        reg_file.wen @= m.enable(wb_en.O & ~stall & ~csr.expt)
        reg_file.waddr @= wb_rd_addr
        reg_file.wdata @= reg_write

        # Abort store when there's an exception
        self.io.dcache.abort @= csr.expt
