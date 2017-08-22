from magma import *
from magma.bitutils import *

def simulate_prim_not(self, value_store, state_store):
    I = value_store.get_value(self.I)
    value_store.set_value(self.O, not I)

def simulate_prim_and(self, value_store, state_store):
    I0 = value_store.get_value(self.I0)
    I1 = value_store.get_value(self.I1)
    val = I0 and I1
    value_store.set_value(self.O, val)

def simulate_prim_or(self, value_store, state_store):
    I0 = value_store.get_value(self.I0)
    I1 = value_store.get_value(self.I1)
    val = I0 or I1
    value_store.set_value(self.O, val)

def simulate_prim_flip_flop(self, value_store, state_store):
    cur_clock = value_store.get_value(self.CLK)

    if not state_store:
        state_store['prev_clock'] = cur_clock
        state_store['cur_val'] = False

    prev_clock = state_store['prev_clock']

    clock_edge = not cur_clock and prev_clock

    new_val = state_store['cur_val']

    if clock_edge:
        input_val = value_store.get_value(self.D)
        new_val = input_val

    state_store['prev_clock'] = cur_clock
    state_store['cur_val'] = new_val
    value_store.set_value(self.Q, new_val)


PRIM_AND = DeclareCircuit('PRIM_AND', 'I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit), stateful=False, primitive=True, simulate=simulate_prim_and)
PRIM_OR = DeclareCircuit('PRIM_OR', 'I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit), stateful=False, primitive=True, simulate=simulate_prim_or)
PRIM_NOT = DeclareCircuit('PRIM_NOT', 'I', In(Bit), 'O', Out(Bit), stateful=False, primitive=True, simulate=simulate_prim_not)
PRIM_FF = DeclareCircuit('PRIM_FF', 'CLK', In(Bit), 'D', In(Bit), 'Q', Out(Bit), stateful=True, primitive=True, simulate=simulate_prim_flip_flop)
