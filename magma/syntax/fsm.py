import magma as m
from magma.common import Stack
from magma.sum_type import MatchContext, Enum2


_FSM_STACK = Stack()


def reset_fsm_context():
    _FSM_STACK.clear()


class FSMState(Enum2):
    @classmethod
    def get_states(cls):
        return cls._key_map.values()


class FSMContext(MatchContext):
    def __init__(self, state_reg):
        self.state_reg = state_reg
        super().__init__(state_reg.O)

    @property
    def next(self):
        return self.state_reg.I

    @next.setter
    def next(self, value):
        pass

    def __enter__(self):
        _FSM_STACK.push(self)
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, exc_tb):
        assert _FSM_STACK.pop() is self
        super().__exit__(exc_type, exc_value, exc_tb)


def fsm(T: m.Kind, init: FSMState):
    state_reg = m.Register(T, init=init)()
    return FSMContext(state_reg)


def wait_until(cond: m.Bit):
    curr_fsm = _FSM_STACK.peek()
    with m.no_when():
        state_reg = m.Register(m.Bit, init=0)()
        state_reg.I @= 0
    state_reg.I @= cond
    curr_fsm.cases[-1].exit_stack.enter_context(m.when(state_reg.O))


def wait():
    wait_until(1)
