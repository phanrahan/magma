import tempfile

import pytest
import fault as f
import magma as m
from mantle2.counter import Counter

from riscv_mini.data_path import Datapath, Const
from riscv_mini.control import Control
from riscv_mini.imm_gen import ImmGenWire, ImmGenMux
from .utils import tests, test_results, fin, nop, ResetTester


@pytest.mark.parametrize('test', ['bypass', 'exception'])
@pytest.mark.parametrize('ImmGen', [ImmGenWire, ImmGenMux])
def test_datapath(test, ImmGen):
    class DUT(m.Circuit):
        x_len = 32
        io = m.IO(done=m.Out(m.Bit)) + m.ClockIO(has_reset=True)
        data_path = Datapath(x_len, ImmGen=ImmGen)()
        control = Control(x_len)()
        for key, value in data_path.ctrl.items():
            m.wire(value, getattr(control, key))
        data_path.host.fromhost.data.undriven()
        data_path.host.fromhost.valid @= 0

        insts = tests[test]
        INIT, RUN = False, True
        state = m.Register(init=INIT)()
        n = len(insts)
        counter = Counter(
            n,
            has_enable=True,
            has_cout=True,
            reset_type=m.Reset
        )()
        counter.CE @= m.enable(state.O == INIT)
        cntr, done = counter.O, counter.COUT
        timeout = m.Register(m.Bits[x_len])()
        n_write_ports = len(range(0, Const.PC_START, 4)) + 2
        mem = m.MultiportMemory(
            1 << 20, m.UInt[x_len], num_read_ports=2,
            num_write_ports=n_write_ports)()
        iaddr = (data_path.icache.req.data.addr // (x_len // 8))[:20]
        daddr = (data_path.dcache.req.data.addr // (x_len // 8))[:20]
        write = 0
        mem.RADDR_0 @= daddr
        mem.RADDR_1 @= iaddr
        mem_daddr = mem.RDATA_0
        mem_iaddr = mem.RDATA_1
        for i in range(x_len // 8):
            write |= m.mux([
                mem_daddr & (0xff << (8 * i)),
                data_path.dcache.req.data.data
            ], data_path.dcache.req.data.mask[i])
        data_path.RESET @= m.reset(state.O == INIT)
        data_path.icache.resp.data.data @= \
            m.Register(m.UInt[x_len])()(mem_iaddr)
        data_path.icache.resp.valid @= state.O == RUN

        data_path.dcache.resp.data.data @= \
            m.Register(m.UInt[x_len])()(mem_daddr)
        data_path.dcache.resp.valid @= state.O == RUN

        i = 0
        for addr in range(0, Const.PC_START, 4):
            wdata = fin if addr == Const.PC_EVEC + (3 << 6) else nop
            getattr(mem, f"WADDR_{i}").wire(addr // 4)
            getattr(mem, f"WDATA_{i}").wire(wdata)
            getattr(mem, f"WE_{i}").wire(m.enable(state.O == INIT))
            i += 1
        getattr(mem, f"WADDR_{i}").wire(
            Const.PC_START // (x_len // 8) + m.zext_to(cntr, 20)
        )
        getattr(mem, f"WDATA_{i}").wire(m.mux(insts, cntr))
        getattr(mem, f"WE_{i}").wire(m.enable(state.O == INIT))

        i += 1
        getattr(mem, f"WADDR_{i}").wire(daddr)
        getattr(mem, f"WDATA_{i}").wire(write)
        getattr(mem, f"WE_{i}").wire(
            m.enable((state.O == RUN) & data_path.dcache.req.valid &
                     data_path.dcache.req.data.mask.reduce_or()))

        m.display("INST[%x] = %x, iaddr: %x", data_path.icache.req.data.addr,
                  mem_iaddr, iaddr).when(m.posedge(io.CLK))\
            .if_((state.O == RUN) & data_path.icache.req.valid)

        m.display("MEM[%x] <= %x", data_path.dcache.req.data.addr,
                  write).when(m.posedge(io.CLK))\
            .if_((state.O == RUN) & data_path.dcache.req.valid &
                 data_path.dcache.req.data.mask.reduce_or())

        m.display("MEM[%x] => %x", data_path.dcache.req.data.addr,
                  mem_daddr).when(m.posedge(io.CLK))\
            .if_((state.O == RUN) & data_path.dcache.req.valid &
                 ~data_path.dcache.req.data.mask.reduce_or())

        state.I @= state.O
        timeout.I @= timeout.O
        io.done @= False
        with m.when(state.O == RUN):
            timeout.I @= timeout.O + 1
            with m.when(data_path.host.tohost != 0):
                io.done @= True
        with m.elsewhen(done):
            state.I @= RUN

        f.assert_immediate(
            (state.O != RUN) | (data_path.host.tohost == 0) |
            (data_path.host.tohost == test_results[test]),
            failure_msg=(f"* tohost: %d != {test_results[test]} *",
                         data_path.host.tohost)
        )

    tester = ResetTester(DUT, DUT.CLK)
    tester.reset()
    tester.wait_until_high(DUT.done)
    with tempfile.TemporaryDirectory() as tempdir:
        tester.compile_and_run(
            "verilator",
            magma_opts={
                "flatten_all_tuples": True,
                "disallow_local_variables": True,
                "check_circt_opt_version": False,
            },
            magma_output="mlir-verilog",
            flags=[
                '-Wno-unused',
                '-Wno-PINCONNECTEMPTY',
                '-Wno-undriven',
                '--assert',
            ],
            disp_type="realtime",
            directory=tempdir,
        )
