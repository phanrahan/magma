import magma as m
from magma.testing.utils import check_gold


def test_fsm_wait():
    class State(m.FSMState):
        INIT = 0
        RUN = 1
        DONE = 2

    class Foo(m.Circuit):
        io = m.IO(O=m.Out(m.Bits[16]))
        # Must delay elaboration of state register until total number states
        # computed (number of wait statements)
        # Could use a builder here?
        with m.fsm(State) as state:
            with m.case(State.INIT):
                io.O @= 0xFEED
                state.next @= State.RUN
            with m.case(State.RUN):
                io.O @= 0xDEAD
                m.wait()
                io.O @= 0xBEEF
                state.next @= State.DONE
            with m.case(State.DONE):
                io.O @= 0xBEEF
                state.next @= State.DONE

    m.compile("build/test_sum_enum", Foo, output="mlir",
              flatten_all_tuples=True)
    assert check_gold(__file__, "test_sum_enum.mlir")
