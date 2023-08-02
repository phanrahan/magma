import pytest
from hwtypes import BitVector
import magma as m
import fault as f
from mantle2.counter import Counter

from riscv_mini.core import Core
from riscv_mini.imm_gen import ImmGenWire, ImmGenMux
from .utils import concat, ResetTester


class SimpleTests:
    tests = ["rv32ui-p-simple"]
    maxcycles = 150000


class ISATests:
    tests = []
    for test in ["simple", "add", "addi", "auipc", "and", "andi",
                 "sb", "sh", "sw", "lb", "lbu", "lh", "lhu", "lui", "lw",
                 "beq", "bge", "bgeu", "blt", "bltu", "bne", "j", "jal",
                 "jalr", "or", "ori", "sll", "slli", "slt", "slti", "sra",
                 "srai", "sub", "xor", "xori"]:
        # TODO: "fence_i" (also todo in chisel riscv-mini)
        tests.append(f"rv32ui-p-{test}")
    for test in ["sbreak", "scall", "illegal", "ma_fetch", "ma_addr", "csr"]:
        # TODO: "timer" (also todo in chisel riscv-mini)
        tests.append(f"rv32mi-p-{test}")
        maxcycles = 15000


class BmarkTests:
    tests = ["median.riscv", "multiply.riscv", "qsort.riscv", "towers.riscv",
             "vvadd.riscv"]
    maxcycles = 1500000


class LargeBmarkTests:
    tests = ["median.riscv-large", "multiply.riscv-large", "qsort.riscv-large",
             "towers.riscv-large", "vvadd.riscv-large"]
    maxcycles = 5000000


def parse_nibble(hex_str):
    hex_val = ord(hex_str)
    if hex_val >= ord('a'):
        return hex_val - ord('a') + 10
    return hex_val - ord('0')


def load_mem(lines, chunk):
    insts = []
    for line in lines:
        assert len(line) % (chunk // 4) == 0
        for i in range(len(line) - (chunk // 4), -1, -(chunk // 4)):
            inst = 0
            for j in range(0, chunk // 4):
                inst |= (parse_nibble(line[i + j]) <<
                         (4 * ((chunk // 4) - (j + 1))))
            insts.append(BitVector[chunk](inst))
    return insts


@pytest.mark.parametrize('test', [SimpleTests])  # , ISATests, BmarkTests])
@pytest.mark.parametrize('ImmGen', [ImmGenWire, ImmGenMux])
def test_core(test, ImmGen):
    for t in test.tests:
        x_len = 32
        with open(f'tests/resources/{t}.hex', 'r') as file_:
            contents = [line.rstrip() for line in file_.readlines()]
            loadmem = load_mem(contents, x_len)

        class DUT(m.Circuit):
            io = m.IO(done=m.Out(m.Bit)) + m.ClockIO(has_reset=True)
            core = Core(x_len,
                        data_path_kwargs=m.generator.ParamDict(ImmGen=ImmGen))()
            core.host.fromhost.data.undriven()
            core.host.fromhost.valid @= False

            # reverse concat because we're using utils with chisel ordering
            _hex = [concat(*reversed(x)) for x in loadmem]
            imem = m.Memory(1 << 20, m.UInt[x_len])()
            dmem = m.Memory(1 << 20, m.UInt[x_len])()

            INIT, RUN = False, True

            state = m.Register(init=INIT)()
            cycle = m.Register(m.UInt[32])()

            n = len(_hex)
            counter = Counter(
                n,
                has_enable=True,
                has_cout=True,
                reset_type=m.Reset
            )()
            counter.CE @= m.enable(state.O == INIT)
            cntr, done = counter.O, counter.COUT

            iaddr = (core.icache.req.data.addr // (x_len // 8))[:20]
            daddr = (core.dcache.req.data.addr // (x_len // 8))[:20]

            dmem.RADDR @= daddr
            dmem_data = dmem.RDATA
            imem.RADDR @= iaddr
            imem_data = imem.RDATA
            write = 0
            for i in range(x_len // 8):
                sel = m.Bit(name=f"sel_{i}")
                sel @= core.dcache.req.valid & core.dcache.req.data.mask[i]
                write |= m.zext_to(m.mux(
                    [dmem_data, core.dcache.req.data.data],
                    sel
                )[8 * i:8 * (i + 1)], 32) << (8 * i)

            core.RESET @= m.reset(state.O == INIT)

            core.icache.resp.valid @= state.O == RUN
            core.dcache.resp.valid @= state.O == RUN

            core.icache.resp.data.data @= m.Register(m.UInt[x_len])()(imem_data)
            core.dcache.resp.data.data @= m.Register(m.UInt[x_len])()(dmem_data)

            chunk = m.mux(_hex, cntr)

            imem.WADDR @= m.zext_to(cntr, 20)
            imem.WDATA @= chunk
            imem.WE @= m.enable(state.O == INIT)

            dmem.WADDR @= m.mux([daddr, m.zext_to(cntr, 20)], state.O == RUN)
            dmem.WDATA @= m.mux([write, chunk], state.O == RUN)
            dmem.WE @= m.enable(
                (state.O == INIT) | (core.dcache.req.valid &
                                     core.dcache.req.data.mask.reduce_or())
            )

            state.I @= state.O
            cycle.I @= cycle.O
            with m.when(state.O == RUN):
                cycle.I @= cycle.O + 1
            with m.elsewhen(done):
                state.I @= RUN

            debug = False
            if debug:
                m.display("LOADMEM[%x] <= %x", cntr * (x_len // 8),
                          chunk).when(m.posedge(io.CLK)).if_(state.O == INIT)

                m.display("INST[%x] => %x", iaddr * (x_len // 8),
                          dmem_data).when(m.posedge(io.CLK)).if_(
                              (state.O == RUN) & core.icache.req.valid)

                m.display("MEM[%x] <= %x", daddr * (x_len // 8),
                          write).when(m.posedge(io.CLK)).if_(
                              (state.O == RUN) & core.dcache.req.valid &
                              core.dcache.req.data.mask.reduce_or())

                m.display("MEM[%x] => %x", daddr * (x_len // 8),
                          dmem_data).when(m.posedge(io.CLK)).if_(
                              (state.O == RUN) & core.dcache.req.valid &
                              ~core.dcache.req.data.mask.reduce_or())

                m.display("cycles: %d", cycle.O).when(m.posedge(io.CLK)).if_(
                    io.done.value() == 1)
            f.assert_immediate(cycle.O < test.maxcycles)
            io.done @= core.host.tohost != 0
            f.assert_immediate((core.host.tohost >> 1) == 0,
                               failure_msg=("* tohost: %d *", core.host.tohost))

    tester = ResetTester(DUT, DUT.CLK)
    tester.reset()
    tester.wait_until_high(DUT.done)
    tester.compile_and_run(
        "verilator",
        magma_output="mlir-verilog",
        magma_opts={
            "flatten_all_tuples": True,
            "disallow_local_variables": True,
            "check_circt_opt_version": False,
        },
        flags=[
            '-Wno-unused',
            '-Wno-PINCONNECTEMPTY',
            '-Wno-undriven',
            '--assert',
        ],
    )
