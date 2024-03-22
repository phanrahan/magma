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
