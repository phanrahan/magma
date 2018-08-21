class return_magma_named_tuple(m.Circuit):
    IO = ['I', m.In(m.Bits(2)), 'O', m.Out(m.Tuple(x=m.Bit, y=m.Bit))]

    @classmethod
    def definition(io):
        O = m.namedtuple(x=io.I[0], y=io.I[1])
        m.wire(O, io.O)
