class ternary_nested2(m.Circuit):
    IO = ['I', m.In(m.Bits(4)), 'S', m.In(m.Bits(2)), 'O', m.Out(m.Bit)]

    @classmethod
    def definition(io):
        O = mux([io.I[2], mux([io.I[1], io.I[0]], io.S[0])], io.S[1])
        m.wire(O, io.O)
