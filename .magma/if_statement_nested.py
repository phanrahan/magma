class if_statement_nested(m.Circuit):
    IO = ['I', m.In(m.Bits(4)), 'S', m.In(m.Bits(2)), 'O', m.Out(m.Bit)]

    @classmethod
    def definition(io):
        O = mux([mux([io.I[3], io.I[2]], io.S[1]), mux([io.I[1], io.I[0]],
            io.S[1])], io.S[0])
        m.wire(O, io.O)
