import magma as m


class PRIM_AND(m.Circuit):
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    stateful = False
    primitive = True

    def simulate(self, value_store, state_store):
        I0 = value_store.get_value(self.I0)
        I1 = value_store.get_value(self.I1)
        val = I0 and I1
        value_store.set_value(self.O, val)


class PRIM_OR(m.Circuit):
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    stateful = False
    primitive = True

    def simulate(self, value_store, state_store):
        I0 = value_store.get_value(self.I0)
        I1 = value_store.get_value(self.I1)
        val = I0 or I1
        value_store.set_value(self.O, val)


class PRIM_NOT(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
    stateful = False
    primitive = True

    def simulate(self, value_store, state_store):
        I = value_store.get_value(self.I)
        value_store.set_value(self.O, not I)


class PRIM_FF(m.Circuit):
    io = m.IO(CLK=m.In(m.Clock), D=m.In(m.Bit), Q=m.Out(m.Bit))
    stateful = True
    primitive = True

    def simulate(self, value_store, state_store):
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
