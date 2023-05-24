from hwtypes import BitVector as BV


class CSR:
    N = BV[3](0)
    W = BV[3](1)
    S = BV[3](2)
    C = BV[3](3)
    P = BV[3](4)

    # Supports machine & user modes
    PRV_U = BV[2](0x0)
    PRV_M = BV[2](0x3)

    # User-level CSR addrs
    cycle = BV[12](0xc00)
    time = BV[12](0xc01)
    instret = BV[12](0xc02)
    cycleh = BV[12](0xc80)
    timeh = BV[12](0xc81)
    instreth = BV[12](0xc82)

    # Supervisor-level CSR addrs
    cyclew = BV[12](0x900)
    timew = BV[12](0x901)
    instretw = BV[12](0x902)
    cyclehw = BV[12](0x980)
    timehw = BV[12](0x981)
    instrethw = BV[12](0x982)

    # Machine-level CSR addrs
    # Machine Information Registers
    mcpuid = BV[12](0xf00)
    mimpid = BV[12](0xf01)
    mhartid = BV[12](0xf10)

    # Machine Trap Setup
    mstatus = BV[12](0x300)
    mtvec = BV[12](0x301)
    mtdeleg = BV[12](0x302)
    mie = BV[12](0x304)
    mtimecmp = BV[12](0x321)

    # Machine Timers and Counters
    mtime = BV[12](0x701)
    mtimeh = BV[12](0x741)

    # Machine Trap Handling
    mscratch = BV[12](0x340)
    mepc = BV[12](0x341)
    mcause = BV[12](0x342)
    mbadaddr = BV[12](0x343)
    mip = BV[12](0x344)

    # Machine HITF
    mtohost = BV[12](0x780)
    mfromhost = BV[12](0x781)

    regs = [cycle, time, instret, cycleh, timeh, instreth, cyclew, timew,
            instretw, cyclehw, timehw, instrethw, mcpuid, mimpid, mhartid,
            mtvec, mtdeleg, mie, mtimecmp, mtime, mtimeh, mscratch, mepc,
            mcause, mbadaddr, mip, mtohost, mfromhost, mstatus]
