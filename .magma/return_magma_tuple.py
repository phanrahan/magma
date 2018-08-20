class return_magma_tuple(m.Circuit):
    IO = ['I', m.In(m.Bits(2)), 'O', m.Out(m.Tuple(m.Bit, m.Bit))]

    @classmethod
    def definition(io):
        O = m.tuple_([io.I[0], io.I[1]])
        m.wire(O, io.O)
