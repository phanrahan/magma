import tempfile

import fault
import magma as m
# m.config.set_debug_mode(True)
from mantle2.counter import Counter
from riscv_mini.csr import CSR
from riscv_mini.csr_gen import CSRGen, make_Cause
import riscv_mini.control as Control
from riscv_mini.data_path import Const
import riscv_mini.instructions as Instructions

from hwtypes import BitVector as BV

from .utils import (I, rand_fn3, rand_rs1, rand_rs2, SYS, J, L, rand_rd, JR,
                    rand_inst, csr as csr_util, rs1, nop, ResetTester)
from .opcode import Funct3


def update_when(reg, value, cond):
    if reg.I.driven():
        default = reg.I.value()
        reg.I.unwire(default)
    else:
        default = reg.O
    # Temp hack for verilator width inference issue
    _cond = m.Bit(name=f"cond_{id(cond)}")
    _cond @= cond
    reg.I @= m.mux([default, value], _cond)


def incr_when(reg, cond):
    update_when(reg, reg.O + 1, cond)


def test_csr():
    x_len = 32

    insts = (
        [I(rand_fn3, 0, rand_rs1, reg) for reg in CSR.regs] +
        [SYS(Funct3.CSRRW, 0, reg, rand_rs1) for reg in CSR.regs] +
        [SYS(Funct3.CSRRS, 0, reg, rand_rs1) for reg in CSR.regs] +
        [SYS(Funct3.CSRRC, 0, reg, rand_rs1) for reg in CSR.regs] +
        [SYS(Funct3.CSRRWI, 0, reg, rand_rs1) for reg in CSR.regs] +
        [SYS(Funct3.CSRRSI, 0, reg, rand_rs1) for reg in CSR.regs] +
        [SYS(Funct3.CSRRCI, 0, reg, rand_rs1) for reg in CSR.regs] +
        [I(rand_fn3, 0, rand_rs1, reg) for reg in CSR.regs] + [
            # system insts
            # TODO: Can't mux Instructions (BitPattern)
            Instructions.ECALL.as_bv(), SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            Instructions.EBREAK.as_bv(), SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            Instructions.ERET.as_bv(), SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            # illegal addr
            J(rand_rd, BV.random(x_len)), SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            JR(rand_rd, rand_rs1, BV.random(x_len)),
            L(Funct3.LW, rand_rd, rand_rs1, rand_rs2),
            SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            L(Funct3.LH, rand_rd, rand_rs1, rand_rs2),
            SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            L(Funct3.LHU, rand_rd, rand_rs1, rand_rs2),
            SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            L(Funct3.SW, rand_rd, rand_rs1, rand_rs2),
            SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            L(Funct3.SH, rand_rd, rand_rs1, rand_rs2),
            SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            # illegal inst
            rand_inst, SYS(Funct3.CSRRC, 0, CSR.mcause, 0),
            # check counters
            SYS(Funct3.CSRRC, 0, CSR.time, 0),
            SYS(Funct3.CSRRC, 0, CSR.cycle, 0),
            SYS(Funct3.CSRRC, 0, CSR.instret, 0),
            SYS(Funct3.CSRRC, 0, CSR.mfromhost, 0)
        ]
    )
    print(insts)
    # print(hex(int(rand_inst)))
    # exit()

    n = len(insts)
    pc = [BV.random(x_len) for _ in range(n)]
    addr = [BV.random(x_len) for _ in range(n)]
    data = [BV.random(x_len) for _ in range(n)]

    class CSR_DUT(m.Circuit):
        io = m.IO(done=m.Out(m.Bit),
                  check=m.Out(m.Bit),
                  rdata=m.Out(m.UInt[x_len]),
                  expected_rdata=m.Out(m.UInt[x_len]),
                  epc=m.Out(m.UInt[x_len]),
                  expected_epc=m.Out(m.UInt[x_len]),
                  evec=m.Out(m.UInt[x_len]),
                  expected_evec=m.Out(m.UInt[x_len]),
                  expt=m.Out(m.Bit),
                  expected_expt=m.Out(m.Bit))
        io += m.ClockIO(has_reset=True)

        regs = {}
        for reg in CSR.regs:
            if reg == CSR.mcpuid:
                init = (1 << (ord('I') - ord('A')) |
                        1 << (ord('U') - ord('A')))
            elif reg == CSR.mstatus:
                init = (CSR.PRV_M.ext(30) << 4) | (CSR.PRV_M.ext(30) << 1)
            elif reg == CSR.mtvec:
                init = Const.PC_EVEC
            else:
                init = 0
            regs[reg] = m.Register(init=BV[32](init), reset_type=m.Reset)()

        csr = CSRGen(x_len)()
        ctrl = Control.Control(x_len)()

        counter = Counter(n, has_cout=True, reset_type=m.Reset)()
        inst = m.mux(insts, counter.O)
        ctrl.inst @= inst
        csr.inst @= inst
        csr_cmd = ctrl.csr_cmd
        csr.cmd @= csr_cmd
        csr.illegal @= ctrl.illegal
        csr.st_type @= ctrl.st_type
        csr.ld_type @= ctrl.ld_type
        csr.pc_check @= ctrl.pc_sel == Control.PC_ALU
        csr.pc @= m.mux(pc, counter.O)
        csr.addr @= m.mux(addr, counter.O)
        csr.I @= m.mux(data, counter.O)
        csr.stall @= False
        csr.host.fromhost.valid @= False
        csr.host.fromhost.data @= 0

        # values known statically
        _csr_addr = [csr_util(inst) for inst in insts]
        _rs1_addr = [rs1(inst) for inst in insts]
        _csr_ro = [((((x >> 11) & 0x1) > 0x0) & (((x >> 10) & 0x1) > 0x0)) |
                   (x == CSR.mtvec) | (x == CSR.mtdeleg) for x in _csr_addr]
        _csr_valid = [x in CSR.regs for x in _csr_addr]
        # should be <= prv in runtime
        _prv_level = [(x >> 8) & 0x3 for x in _csr_addr]
        # should consider prv in runtime
        _is_ecall = [((x & 0x1) == 0x0) & (((x >> 8) & 0x1) == 0x0)
                     for x in _csr_addr]
        _is_ebreak = [((x & 0x1) > 0x0) & (((x >> 8) & 0x1) == 0x0)
                      for x in _csr_addr]
        _is_eret = [((x & 0x1) == 0x0) & (((x >> 8) & 0x1) > 0x0)
                    for x in _csr_addr]
        # should consider pc_check in runtime
        _iaddr_invalid = [((x >> 1) & 0x1) > 0 for x in addr]
        # should consider ld_type & sd_type
        _waddr_invalid = [(((x >> 1) & 0x1) > 0) | ((x & 0x1) > 0)
                          for x in addr]
        _haddr_invalid = [(x & 0x1) > 0 for x in addr]

        # values known at runtime
        csr_addr = m.mux(_csr_addr, counter.O)
        rs1_addr = m.mux(_rs1_addr, counter.O)
        csr_ro = m.mux(_csr_ro, counter.O)
        csr_valid = m.mux(_csr_valid, counter.O)

        wen = (csr_cmd == CSR.W) | (csr_cmd[1] & (rs1_addr != 0))
        prv1 = (regs[CSR.mstatus].O >> 4) & 0x3
        ie1 = (regs[CSR.mstatus].O >> 3) & 0x1
        prv = (regs[CSR.mstatus].O >> 1) & 0x3
        ie = regs[CSR.mstatus].O & 0x1
        prv_inst = csr_cmd == CSR.P
        prv_valid = (m.uint(m.zext_to(m.mux(_prv_level, counter.O), 32)) <=
                     m.uint(prv))
        iaddr_invalid = m.mux(_iaddr_invalid, counter.O) & csr.pc_check.value()
        laddr_invalid = (
            m.mux(_haddr_invalid, counter.O) &
            ((ctrl.ld_type == Control.LD_LH) |
             (ctrl.ld_type == Control.LD_LHU)) |
            m.mux(_waddr_invalid, counter.O) &
            (ctrl.ld_type == Control.LD_LW)
        )
        saddr_invalid = (
            m.mux(_haddr_invalid, counter.O) &
            (ctrl.st_type == Control.ST_SH) |
            m.mux(_waddr_invalid, counter.O) &
            (ctrl.st_type == Control.ST_SW)
        )
        is_ecall = prv_inst & m.mux(_is_ecall, counter.O)
        is_ebreak = prv_inst & m.mux(_is_ebreak, counter.O)
        is_eret = prv_inst & m.mux(_is_eret, counter.O)
        exception = (ctrl.illegal | iaddr_invalid | laddr_invalid |
                     saddr_invalid |
                     (((csr_cmd & 0x3) > 0) & (~csr_valid | ~prv_valid)) |
                     (csr_ro & wen) | (prv_inst & ~prv_valid) | is_ecall |
                     is_ebreak)
        instret = (inst != nop) & (~exception | is_ecall | is_ebreak)

        rdata = m.dict_lookup({
            key: value.O for key, value in regs.items()
        }, csr_addr)
        wdata = m.dict_lookup({
            CSR.W: csr.I.value(),
            CSR.S: (csr.I.value() | rdata),
            CSR.C: (~csr.I.value() & rdata)
        }, csr_cmd)

        # compute state
        regs[CSR.time].I @= regs[CSR.time].O + 1
        regs[CSR.timew].I @= regs[CSR.timew].O + 1
        regs[CSR.mtime].I @= regs[CSR.mtime].O + 1
        regs[CSR.cycle].I @= regs[CSR.cycle].O + 1
        regs[CSR.cyclew].I @= regs[CSR.cyclew].O + 1

        time_max = regs[CSR.time].O.reduce_and()
        # TODO: mtime has same default value as this case (from chisel code)
        # https://github.com/ucb-bar/riscv-mini/blob/release/src/test/scala/CSRTests.scala#L140
        # mtime_reg = regs[CSR.mtime]
        # mtime_reg.I @= m.mux([mtime_reg.O, mtime_reg.O + 1], time_max)

        incr_when(regs[CSR.timeh], time_max)
        incr_when(regs[CSR.timehw], time_max)

        cycle_max = regs[CSR.cycle].O.reduce_and()

        incr_when(regs[CSR.cycleh], cycle_max)
        incr_when(regs[CSR.cyclehw], cycle_max)

        incr_when(regs[CSR.instret], instret)
        incr_when(regs[CSR.instretw], instret)

        instret_max = regs[CSR.instret].O.reduce_and()
        incr_when(regs[CSR.instreth], instret & instret_max)
        incr_when(regs[CSR.instrethw], instret & instret_max)

        cond = ~exception & ~is_eret & wen
        # Assuming these are mutually exclusive, so we don't need chained
        # elsewhen
        update_when(regs[CSR.mstatus], m.zext_to(wdata[0:6], 32),
                    cond & (csr_addr == CSR.mstatus))
        update_when(regs[CSR.mip],
                    (m.bits(wdata[7], 32) << 7) | (m.bits(wdata[3], 32) << 3),
                    cond & (csr_addr == CSR.mip))
        update_when(regs[CSR.mie],
                    (m.bits(wdata[7], 32) << 7) | (m.bits(wdata[3], 32) << 3),
                    cond & (csr_addr == CSR.mie))
        update_when(regs[CSR.mepc], (wdata >> 2) << 2,
                    cond & (csr_addr == CSR.mepc))
        update_when(regs[CSR.mcause], wdata & (1 << 31 | 0xf),
                    cond & (csr_addr == CSR.mcause))
        update_when(regs[CSR.time], wdata,
                    cond & ((csr_addr == CSR.timew) | (csr_addr == CSR.mtime)))
        update_when(regs[CSR.timew], wdata,
                    cond & ((csr_addr == CSR.timew) | (csr_addr == CSR.mtime)))
        update_when(regs[CSR.mtime], wdata,
                    cond & ((csr_addr == CSR.timew) | (csr_addr == CSR.mtime)))
        update_when(regs[CSR.timeh], wdata,
                    cond & ((csr_addr == CSR.timehw) |
                            (csr_addr == CSR.mtimeh)))
        update_when(regs[CSR.timehw], wdata,
                    cond & ((csr_addr == CSR.timehw) |
                            (csr_addr == CSR.mtimeh)))
        update_when(regs[CSR.mtimeh], wdata,
                    cond & ((csr_addr == CSR.timehw) |
                            (csr_addr == CSR.mtimeh)))
        update_when(regs[CSR.cycle], wdata,
                    cond & (csr_addr == CSR.cyclew))
        update_when(regs[CSR.cyclew], wdata,
                    cond & (csr_addr == CSR.cyclew))
        update_when(regs[CSR.cycleh], wdata,
                    cond & (csr_addr == CSR.cyclehw))
        update_when(regs[CSR.cyclehw], wdata,
                    cond & (csr_addr == CSR.cyclehw))
        update_when(regs[CSR.instret], wdata,
                    cond & (csr_addr == CSR.instretw))
        update_when(regs[CSR.instretw], wdata,
                    cond & (csr_addr == CSR.instretw))
        update_when(regs[CSR.instreth], wdata,
                    cond & (csr_addr == CSR.instrethw))
        update_when(regs[CSR.instrethw], wdata,
                    cond & (csr_addr == CSR.instrethw))
        update_when(regs[CSR.mtimecmp], wdata,
                    cond & (csr_addr == CSR.mtimecmp))
        update_when(regs[CSR.mscratch], wdata,
                    cond & (csr_addr == CSR.mscratch))
        update_when(regs[CSR.mbadaddr], wdata,
                    cond & (csr_addr == CSR.mbadaddr))
        update_when(regs[CSR.mtohost], wdata,
                    cond & (csr_addr == CSR.mtohost))
        update_when(regs[CSR.mfromhost], wdata,
                    cond & (csr_addr == CSR.mfromhost))

        # eret
        update_when(regs[CSR.mstatus],
                    (CSR.PRV_U.zext(30) << 4) | (1 << 3) | (prv1 << 1) |
                    ie1,
                    ~exception & is_eret)

        # TODO: exception logic comes after since it has priority
        Cause = make_Cause(x_len)
        mcause = m.mux([
            m.mux([
                m.mux([
                    m.mux([
                        m.mux([
                            Cause.IllegalInst,
                            Cause.Breakpoint
                        ], is_ebreak),
                        Cause.Ecall + prv,
                    ], is_ecall),
                    Cause.StoreAddrMisaligned,
                ], saddr_invalid),
                Cause.LoadAddrMisaligned,
            ], laddr_invalid),
            Cause.InstAddrMisaligned,
        ], iaddr_invalid)
        update_when(regs[CSR.mcause], mcause, exception)

        update_when(regs[CSR.mepc], (csr.pc.value() >> 2) << 2, exception)
        update_when(regs[CSR.mstatus],
                    (prv << 4) | (ie << 3) | (CSR.PRV_M.zext(30) << 1),
                    exception)
        update_when(regs[CSR.mbadaddr], csr.addr.value(), exception &
                    (iaddr_invalid | laddr_invalid | saddr_invalid))

        epc = regs[CSR.mepc].O
        evec = regs[CSR.mtvec].O + (prv << 6)

        m.display("*** Counter: %d ***", counter.O)
        m.display("[in] inst: 0x%x, pc: 0x%x, addr: 0x%x, in: 0x%x",
                  csr.inst, csr.pc, csr.addr, csr.I)

        m.display("     cmd: 0x%x, st_type: 0x%x, ld_type: 0x%x, illegal: %d, "
                  "pc_check: %d", csr.cmd, csr.st_type, csr.ld_type,
                  csr.illegal, csr.pc_check)

        m.display("[state] csr addr: %x", csr_addr)

        for reg_addr, reg in regs.items():
            m.display(f" {hex(int(reg_addr))} -> 0x%x", reg.O)

        m.display("[out] read: 0x%x =? 0x%x, epc: 0x%x =? 0x%x, evec: 0x%x ?= "
                  "0x%x, expt: %d ?= %d", csr.O, rdata, csr.epc, epc,
                  csr.evec, evec, csr.expt, exception)
        io.check @= counter.O.reduce_or()

        io.rdata @= csr.O
        io.expected_rdata @= rdata

        io.epc @= csr.epc
        io.expected_epc @= epc

        io.evec @= csr.evec
        io.expected_evec @= evec

        io.expt @= csr.expt
        io.expected_expt @= exception

        # io.failed @= counter.O.reduce_or() & (
        #     (csr.O != rdata) |
        #     (csr.epc != epc) |
        #     (csr.evec != evec) |
        #     (csr.expt != exception)
        # )
        io.done @= counter.COUT
        for key, reg in regs.items():
            if not reg.I.driven():
                reg.I @= reg.O

    tester = ResetTester(CSR_DUT, CSR_DUT.CLK)
    tester.reset()
    loop = tester._while(tester.circuit.done == 0)
    # loop.circuit.failed.expect(0)
    if_ = loop._if(tester.circuit.check)
    if_.circuit.rdata.expect(tester.peek(CSR_DUT.expected_rdata))
    if_.circuit.epc.expect(tester.peek(CSR_DUT.expected_epc))
    if_.circuit.evec.expect(tester.peek(CSR_DUT.expected_evec))
    if_.circuit.expt.expect(tester.peek(CSR_DUT.expected_expt))
    loop.step(2)
    # tester.circuit.failed.expect(0)
    if_ = tester._if(tester.circuit.check)
    if_.circuit.rdata.expect(tester.peek(CSR_DUT.expected_rdata))
    if_.circuit.epc.expect(tester.peek(CSR_DUT.expected_epc))
    if_.circuit.evec.expect(tester.peek(CSR_DUT.expected_evec))
    if_.circuit.expt.expect(tester.peek(CSR_DUT.expected_expt))
    with tempfile.TemporaryDirectory() as tempdir:
        tester.compile_and_run("verilator",
                               magma_opts={"disallow_local_variables": True,
                                           "flatten_all_tuples": True,
                                           "terminate_unused": True,
                                           "check_circt_opt_version": False},
                               magma_output="mlir-verilog",
                               flags=['-Wno-unused', '-Wno-PINCONNECTEMPTY'],
                               directory=tempdir
                               )
