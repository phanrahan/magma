import tempfile

import fault as f
import magma as m
from mantle2.counter import Counter
import pytest

from riscv_mini.control import (Control, IMM_I, IMM_S, IMM_B, IMM_U, IMM_J,
                                IMM_Z)
from riscv_mini.imm_gen import ImmGenWire, ImmGenMux

from .utils import insts, iimm, simm, bimm, uimm, jimm, zimm


@pytest.mark.parametrize('ImmGen', [ImmGenWire, ImmGenMux])
def test_imm_gen_wire(ImmGen):
    class DUT(m.Circuit):
        io = m.IO(done=m.Out(m.Bit)) + m.ClockIO()
        imm = ImmGen(32)()
        ctrl = Control(32)()

        counter = Counter(len(insts), has_cout=True)()
        i = m.mux([iimm(i) for i in insts], counter.O)
        s = m.mux([simm(i) for i in insts], counter.O)
        b = m.mux([bimm(i) for i in insts], counter.O)
        u = m.mux([uimm(i) for i in insts], counter.O)
        j = m.mux([jimm(i) for i in insts], counter.O)
        z = m.mux([zimm(i) for i in insts], counter.O)
        x = m.mux([iimm(i) & -2 for i in insts], counter.O)

        O = m.mux([
            m.mux([
                m.mux([
                    m.mux([
                        m.mux([
                            m.mux([
                                x,
                                z
                            ], ctrl.imm_sel == IMM_Z),
                            j
                        ], ctrl.imm_sel == IMM_J),
                        u
                    ], ctrl.imm_sel == IMM_U),
                    b
                ], ctrl.imm_sel == IMM_B),
                s
            ], ctrl.imm_sel == IMM_S),
            i
        ], ctrl.imm_sel == IMM_I)
        inst = m.mux(insts, counter.O)
        ctrl.inst @= inst
        imm.inst @= inst
        imm.sel @= ctrl.imm_sel
        io.done @= counter.COUT

        f.assert_immediate(imm.O == O, failure_msg=(
            "Counter: %d, Type: 0x%x, O: %x ?= %x", counter.O, imm.sel,
            imm.O, O))
        m.display("Counter: %d, Type: 0x%x, O: %x ?= %x",
                  counter.O, imm.sel, imm.O, O)

    tester = f.Tester(DUT, DUT.CLK)
    tester.wait_until_high(DUT.done)
    with tempfile.TemporaryDirectory() as tempdir:
        tester.compile_and_run("verilator",
                               magma_opts={"flatten_all_tuples": True,
                                           "disallow_local_variables": True,
                                           "terminate_unused": True,
                                           "check_circt_opt_version": False},
                               magma_output="mlir-verilog",
                               flags=['--assert', "-Wno-unused"],
                               disp_type="realtime",
                               directory=tempdir)
