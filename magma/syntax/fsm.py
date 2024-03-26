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


class LoopWrapper:
    def __init__(self, value, when_ctx):
        self._value = value
        self._when_ctx = when_ctx

    def __enter__(self):
        self._when_ctx.__enter__()
        return self._value

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._when_ctx.__exit__(exc_type, exc_value, exc_tb)


def loop(start, end, step=1):
    with m.no_when():
        end_reg = m.Register(type(end))()
        end_reg.I @= end_reg.O
    end_reg.I @= end
    with m.no_when():
        i = m.Register(type(end))()
        i.I @= i.O + step
    i.I @= start
    m.wait()
    # TODO: We explicitly override after wait, otherwise defautl value will set
    # start, can we avoid this?
    i.I @= i.O + step
    when = m.when(end_reg.O < i.O)
    curr_fsm = _FSM_STACK.peek()
    when.exit_stack.callback(
        lambda: curr_fsm.cases[-1].exit_stack.enter_context(m.otherwise())
    )
    return LoopWrapper(i.O, when)
