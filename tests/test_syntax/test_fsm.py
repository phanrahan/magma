import magma as m
from magma.testing.utils import check_gold


def test_fsm_wait():
    class State(m.FSMState):
        INIT = 0
        RUN = 1
        WAIT = 2
        DONE = 3

    class Foo(m.Circuit):
        io = m.IO(O=m.Out(m.Bits[16]))
        with m.fsm(State, init=State.INIT) as state:
            with m.case(State.INIT):
                io.O @= 0xFEED
                state.next @= State.WAIT
            with m.case(State.WAIT):
                io.O @= 0xDEAD
                m.wait()
                io.O @= 0xBEEF
                state.next @= State.RUN
            with m.case(State.RUN):
                io.O @= 0xBEEF
                # Assumes state.next is not assigned before when
                m.wait()
                io.O @= 0xDEAD
                state.next @= State.DONE
            with m.case(State.DONE):
                io.O @= 0xDEED
                state.next @= State.DONE

    m.compile("build/test_fsm_wait", Foo, output="mlir")
    assert check_gold(__file__, "test_fsm_wait.mlir")


def test_fsm_loop_unroll():
    class State(m.FSMState):
        INIT = 0
        RUN = 1
        WAIT = 2
        DONE = 3

    class Foo(m.Circuit):
        io = m.IO(O=m.Out(m.Bits[2]))
        with m.fsm(State, init=State.INIT) as state:
            states = list(State.get_states())
            for i, x in enumerate(states):
                with m.case(x):
                    io.O @= i
                    state.next @= states[(i + 1) % 3]

    m.compile("build/test_fsm_loop_unroll", Foo, output="mlir")
    assert check_gold(__file__, "test_fsm_loop_unroll.mlir")


def test_fsm_wait_until():
    class State(m.FSMState):
        INIT = 0
        RUN = 1
        WAIT = 2
        DONE = 3

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bits[16]))
        with m.fsm(State, init=State.INIT) as state:
            with m.case(State.INIT):
                io.O @= 0xFEED
                state.next @= State.WAIT
            with m.case(State.WAIT):
                io.O @= 0xDEAD
                m.wait_until(io.I)
                io.O @= 0xBEEF
                state.next @= State.RUN
            with m.case(State.RUN):
                io.O @= 0xBEEF
                # Assumes state.next is not assigned before when
                m.wait()
                io.O @= 0xDEAD
                state.next @= State.DONE
            with m.case(State.DONE):
                io.O @= 0xDEED
                state.next @= State.DONE

    m.compile("build/test_fsm_wait_until", Foo, output="mlir")
    assert check_gold(__file__, "test_fsm_wait_until.mlir")


def test_fsm_wait_loop():
    class State(m.FSMState):
        INIT = 0
        RUN = 1
        WAIT = 2
        DONE = 3

    class Foo(m.Circuit):
        io = m.IO(n=m.In(m.UInt[8]), O=m.Out(m.Bits[16]))
        with m.fsm(State, init=State.INIT) as state:
            with m.case(State.INIT):
                io.O @= 0xFEED
                state.next @= State.WAIT
            with m.case(State.WAIT):
                io.O @= 0xDEAD
                with m.loop(0, io.n) as i:
                    io.O @= m.zext_to(i, 16)
                io.O @= 0xBEEF
                state.next @= State.RUN
            with m.case(State.RUN):
                io.O @= 0xBEEF
                m.wait()
                io.O @= 0xDEAD
                state.next @= State.DONE
            with m.case(State.DONE):
                io.O @= 0xDEED
                state.next @= State.DONE

    m.compile("build/test_fsm_wait_loop", Foo, output="mlir")
    assert check_gold(__file__, "test_fsm_wait_loop.mlir")


def test_fsm_axi_burst(use_namer_dict):
    class Resp(m.Enum):
        OKAY = 0b00
        EXOKAY = 0b01
        SLVERR = 0b10
        DECERR = 0b11

    class Burst(m.Enum):
        FIXED = 0b00
        INCR = 0b01
        WRAP = 0b10
        RESERVED = 0b11

    class State(m.FSMState):
        INIT = 0

    class AXIBurstReader(m.Circuit):
        io = m.IO(
            ARREADY=m.Out(m.Bit),

            ARVALID=m.In(m.Bit),
            ARADDR=m.In(m.Bits[32]),
            ARSIZE=m.In(m.Bits[3]),
            ARLEN=m.In(m.Bits[8]),

            RREADY=m.In(m.Bit),

            RVALID=m.Out(m.Bit),
            RLAST=m.Out(m.Bit),
            RDATA=m.Out(m.Bits[32]),
        ) + m.ClockIO()
        addr_reg = m.Register(m.UInt[32])()
        size_reg = m.Register(m.Bits[3])()
        len_reg = m.Register(m.UInt[8])()

        mem = m.Memory(2 ** 32, m.Bits[32], read_only=True)()
        io.RDATA @= mem.RDATA

        io.ARREADY @= 0
        io.RLAST @= 0
        io.RVALID @= 0
        with m.fsm(State, init=State.INIT) as state:
            with m.case(State.INIT):
                m.wait_until(io.ARVALID)
                addr_reg.I @= io.ARADDR
                size_reg.I @= io.ARSIZE
                len_reg.I @= io.ARLEN
                io.ARREADY @= 1
                m.wait()
                with m.loop(0, len_reg.O, iter_cond=io.RREADY) as i:
                    mem.RADDR @= addr_reg.O + m.zext_to(i, 32)
                    io.RVALID @= 1
                    io.RLAST @= i == (len_reg.O - 1)
                state.next @= State.INIT

    m.compile("build/test_fsm_axi_burst", AXIBurstReader, output="mlir")
    assert check_gold(__file__, "test_fsm_axi_burst.mlir")
