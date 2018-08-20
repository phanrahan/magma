class basic_func(m.Circuit):
    IO = ['I', m.In(m.Bits(2)), 'S', m.In(m.Bit), 'O', m.Out(m.Bit)]

    @classmethod
    def definition(io):
        O = mux([io.I[1], io.I[0]], io.S)
        m.wire(O, io.O)
