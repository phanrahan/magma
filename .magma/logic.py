class logic(m.Circuit):
    IO = ['a', m.In(m.Bit), 'O0', m.Out(m.Bit)]

    @classmethod
    def definition(io):
        c = mux([m.bit(1), mux([m.bit(0), m.bit(0)], EQ()(io.a, m.bit(0)))],
            EQ()(io.a, m.bit(0)))
        O0, = c,
        m.wire(O0, io.O0)
