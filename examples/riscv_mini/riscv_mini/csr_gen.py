import operator
import magma as m

from hwtypes import Bit
from hwtypes import BitVector as BV

from riscv_mini.const import Const
from riscv_mini.csr import CSR
import riscv_mini.instructions as Instructions
import riscv_mini.control as Control


def HostIO(x_len):
    return m.IO(
        host=m.Product.from_fields("HostIO", {
            "fromhost": m.In(m.Valid[m.UInt[x_len]]),
            "tohost": m.Out(m.UInt[x_len])
        })
    )


def make_Cause(x_len):
    class Cause:
        InstAddrMisaligned = BV[x_len](0x0)
        IllegalInst = BV[x_len](0x2)
        Breakpoint = BV[x_len](0x3)
        LoadAddrMisaligned = BV[x_len](0x4)
        StoreAddrMisaligned = BV[x_len](0x6)
        Ecall = BV[x_len](0x8)
    return Cause


class CSRGen(m.Generator2):
    def __init__(self, x_len):
        Cause = make_Cause(x_len)

        self.io = io = m.IO(
            stall=m.In(m.Bit),
            cmd=m.In(m.UInt[3]),
            I=m.In(m.UInt[x_len]),
            O=m.Out(m.UInt[x_len]),
            # Excpetion
            pc=m.In(m.UInt[x_len]),
            addr=m.In(m.UInt[x_len]),
            inst=m.In(m.UInt[x_len]),
            illegal=m.In(m.Bit),
            st_type=m.In(m.UInt[2]),
            ld_type=m.In(m.UInt[3]),
            pc_check=m.In(m.Bit),
            expt=m.Out(m.Bit),
            evec=m.Out(m.UInt[x_len]),
            epc=m.Out(m.UInt[x_len])
        ) + HostIO(x_len) + m.ClockIO(has_reset=True)

        csr_addr = io.inst[20:32]
        rs1_addr = io.inst[15:20]

        # user counters
        time = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        timeh = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        cycle = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        cycleh = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        instret = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        instreth = m.Register(m.UInt[x_len], reset_type=m.Reset)()

        mcpuid = m.concat(
            BV[26](1 << (ord('I') - ord('A')) |  # Base ISA
                   1 << (ord('U') - ord('A'))),  # User Mode
            BV[x_len - 28](0),
            BV[2](0),  # RV32I
        )
        mimpid = BV[x_len](0)
        mhartid = BV[x_len](0)

        # interrupt enable stack
        PRV = m.Register(m.UInt[len(CSR.PRV_M)], init=CSR.PRV_M,
                         reset_type=m.Reset)()
        PRV1 = m.Register(m.UInt[len(CSR.PRV_M)], init=CSR.PRV_M,
                          reset_type=m.Reset)()
        PRV2 = BV[2](0)
        PRV3 = BV[2](0)
        IE = m.Register(m.Bit, init=False, reset_type=m.Reset)()
        IE1 = m.Register(m.Bit, init=False, reset_type=m.Reset)()
        IE2 = False
        IE3 = False

        # virtualization management field
        VM = BV[5](0)

        # memory privilege
        MPRV = False

        # Extension context status
        XS = BV[2](0)
        FS = BV[2](0)
        SD = BV[1](0)
        mstatus = m.concat(IE.O, PRV.O, IE1.O, PRV1.O, IE2, PRV2, IE3, PRV3,
                           FS, XS, MPRV, VM, BV[x_len - 23](0), SD)
        mtvec = BV[x_len](Const.PC_EVEC)
        mtdeleg = BV[x_len](0)

        # interrupt registers
        MTIP = m.Register(m.Bit, init=False, reset_type=m.Reset)()
        HTIP = False
        STIP = False
        MTIE = m.Register(m.Bit, init=False, reset_type=m.Reset)()
        HTIE = False
        STIE = False
        MSIP = m.Register(m.Bit, init=False, reset_type=m.Reset)()
        HSIP = False
        SSIP = False
        MSIE = m.Register(m.Bit, init=False, reset_type=m.Reset)()
        HSIE = False
        SSIE = False

        mip = m.concat(Bit(False), SSIP, HSIP, MSIP.O, Bit(False), STIP, HTIP,
                       MTIP.O, BV[x_len - 8](0))
        mie = m.concat(Bit(False), SSIE, HSIE, MSIE.O, Bit(False), STIE, HTIE,
                       MTIE.O, BV[x_len - 8](0))

        mtimecmp = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        mscratch = m.Register(m.UInt[x_len], reset_type=m.Reset)()

        mepc = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        mcause = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        mbadaddr = m.Register(m.UInt[x_len], reset_type=m.Reset)()

        mtohost = m.Register(m.UInt[x_len], reset_type=m.Reset)()
        mfromhost = m.Register(m.UInt[x_len], reset_type=m.Reset)()

        io.host.tohost @= mtohost.O
        csr_file = {
            CSR.cycle: cycle.O,
            CSR.time: time.O,
            CSR.instret: instret.O,
            CSR.cycleh: cycleh.O,
            CSR.timeh: timeh.O,
            CSR.instreth: instreth.O,
            CSR.cyclew: cycle.O,
            CSR.timew: time.O,
            CSR.instretw: instret.O,
            CSR.cyclehw: cycleh.O,
            CSR.timehw: timeh.O,
            CSR.instrethw: instreth.O,
            CSR.mcpuid: mcpuid,
            CSR.mimpid: mimpid,
            CSR.mhartid: mhartid,
            CSR.mtvec: mtvec,
            CSR.mtdeleg: mtdeleg,
            CSR.mie: mie,
            CSR.mtimecmp: mtimecmp.O,
            CSR.mtime: time.O,
            CSR.mtimeh: timeh.O,
            CSR.mscratch: mscratch.O,
            CSR.mepc: mepc.O,
            CSR.mcause: mcause.O,
            CSR.mbadaddr: mbadaddr.O,
            CSR.mip: mip,
            CSR.mtohost: mtohost.O,
            CSR.mfromhost: mfromhost.O,
            CSR.mstatus: mstatus,
        }
        out = m.dict_lookup(csr_file, csr_addr)
        io.O @= out

        priv_valid = csr_addr[8:10] <= PRV.O
        priv_inst = io.cmd == CSR.P
        is_E_call = priv_inst & ~csr_addr[0] & ~csr_addr[8]
        is_E_break = priv_inst & csr_addr[0] & ~csr_addr[8]
        is_E_ret = priv_inst & ~csr_addr[0] & csr_addr[8]
        csr_valid = m.reduce(operator.or_, m.bits([csr_addr == key
                                                   for key in csr_file]))
        csr_RO = (csr_addr[10:12].reduce_and() |
                  (csr_addr == CSR.mtvec) | (csr_addr == CSR.mtdeleg))
        wen = (io.cmd == CSR.W) | io.cmd[1] & rs1_addr.reduce_or()
        wdata = m.dict_lookup({
            CSR.W: io.I,
            CSR.S: out | io.I,
            CSR.C: out & ~io.I
        }, io.cmd)

        iaddr_invalid = io.pc_check & io.addr[1]

        laddr_invalid = m.dict_lookup({
            Control.LD_LW: io.addr[0:2].reduce_or(),
            Control.LD_LH: io.addr[0],
            Control.LD_LHU: io.addr[0]
        }, io.ld_type)

        saddr_invalid = m.dict_lookup({
            Control.ST_SW: io.addr[0:2].reduce_or(),
            Control.ST_SH: io.addr[0]
        }, io.st_type)

        expt = (io.illegal | iaddr_invalid | laddr_invalid | saddr_invalid |
                io.cmd[0:2].reduce_or() &
                (~csr_valid | ~priv_valid) | wen & csr_RO |
                (priv_inst & ~priv_valid) | is_E_call | is_E_break)
        io.expt @= expt

        io.evec @= mtvec + (m.zext_to(PRV.O, x_len) << 6)
        io.epc @= mepc.O

        is_inst_ret = m.Bit(name="is_inst_ret")
        is_inst_ret @= ((io.inst != Instructions.NOP) &
                        (~expt | is_E_call | is_E_break) & ~io.stall)

        is_inst_reth = m.Bit(name="is_inst_reth")
        is_inst_reth @= is_inst_ret & instret.O.reduce_and()

        not_stall = m.Bit(name="not_stall")
        not_stall @= ~io.stall

        is_mbadaddr = m.Bit(name="is_mbadaddr")
        is_mbadaddr @= iaddr_invalid | laddr_invalid | saddr_invalid

        # Counters
        time.I @= time.O + 1
        timeh.I @= timeh.O
        with m.when(time.O.reduce_and()):
            timeh.I @= timeh.O + 1

        cycle.I @= cycle.O + 1
        cycleh.I @= cycleh.O
        with m.when(cycle.O.reduce_and()):
            cycleh.I @= cycleh.O + 1
        instret.I @= instret.O
        with m.when(is_inst_ret):
            instret.I @= instret.O + 1
        instreth.I @= instreth.O
        with m.when(is_inst_reth):
            instreth.I @= instreth.O + 1

        mbadaddr.I @= mbadaddr.O
        mepc.I @= mepc.O
        mcause.I @= mcause.O
        PRV.I @= PRV.O
        IE.I @= IE.O
        IE1.I @= IE1.O
        PRV1.I @= PRV1.O
        MTIP.I @= MTIP.O
        MSIP.I @= MSIP.O
        MTIE.I @= MTIE.O
        MSIE.I @= MSIE.O
        mtimecmp.I @= mtimecmp.O
        mscratch.I @= mscratch.O
        mtohost.I @= mtohost.O
        mfromhost.I @= mfromhost.O
        with m.when(io.host.fromhost.valid):
            mfromhost.I @= io.host.fromhost.data

        with m.when(not_stall):
            with m.when(expt):
                mepc.I @= io.pc >> 2 << 2
                with m.when(iaddr_invalid):
                    mcause.I @= Cause.InstAddrMisaligned
                with m.elsewhen(laddr_invalid):
                    mcause.I @= Cause.LoadAddrMisaligned
                with m.elsewhen(saddr_invalid):
                    mcause.I @= Cause.StoreAddrMisaligned
                with m.elsewhen(is_E_call):
                    mcause.I @= Cause.Ecall + m.zext_to(PRV.O, x_len)
                with m.elsewhen(is_E_break):
                    mcause.I @= Cause.Breakpoint
                with m.otherwise():
                    mcause.I @= Cause.IllegalInst
                PRV.I @= CSR.PRV_M
                IE.I @= False
                PRV1.I @= PRV.O
                IE1.I @= IE.O
                with m.when(is_mbadaddr):
                    mbadaddr.I @= io.addr
            with m.elsewhen(is_E_ret):
                PRV.I @= PRV1.O
                IE.I @= IE1.O
                PRV1.I @= CSR.PRV_U
                IE1.I @= True
            with m.elsewhen(wen):
                with m.when(csr_addr == CSR.mstatus):
                    PRV1.I @= wdata[4:6]
                    IE1.I @= wdata[3]
                    PRV.I @= wdata[1:3]
                    IE.I @= wdata[0]
                with m.elsewhen(csr_addr == CSR.mip):
                    MTIP.I @= wdata[7]
                    MSIP.I @= wdata[3]
                with m.elsewhen(csr_addr == CSR.mie):
                    MTIE.I @= wdata[7]
                    MSIE.I @= wdata[3]
                with m.elsewhen(csr_addr == CSR.mtime):
                    time.I @= wdata
                with m.elsewhen(csr_addr == CSR.mtimeh):
                    timeh.I @= wdata
                with m.elsewhen(csr_addr == CSR.mtimecmp):
                    mtimecmp.I @= wdata
                with m.elsewhen(csr_addr == CSR.mscratch):
                    mscratch.I @= wdata
                with m.elsewhen(csr_addr == CSR.mepc):
                    mepc.I @= wdata >> 2 << 2
                with m.elsewhen(csr_addr == CSR.mcause):
                    mcause.I @= wdata & (1 << (x_len - 1) | 0xf)
                with m.elsewhen(csr_addr == CSR.mbadaddr):
                    mbadaddr.I @= wdata
                with m.elsewhen(csr_addr == CSR.mtohost):
                    mtohost.I @= wdata
                with m.elsewhen(csr_addr == CSR.mfromhost):
                    mfromhost.I @= wdata
                with m.elsewhen(csr_addr == CSR.cyclew):
                    cycle.I @= wdata
                with m.elsewhen(csr_addr == CSR.timew):
                    time.I @= wdata
                with m.elsewhen(csr_addr == CSR.instretw):
                    instret.I @= wdata
                with m.elsewhen(csr_addr == CSR.cyclehw):
                    cycleh.I @= wdata
                with m.elsewhen(csr_addr == CSR.timehw):
                    timeh.I @= wdata
                with m.elsewhen(csr_addr == CSR.instrethw):
                    instreth.I @= wdata
