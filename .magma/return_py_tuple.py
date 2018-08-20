class return_py_tuple(m.Circuit):
    IO = ['I', m.In(m.Bits(2)), 'O0', m.Out(m.Bit), 'O1', m.Out(m.Bit)]

    @classmethod
    def definition(io):
        O0, O1 = io.I[0], io.I[1]
        m.wire(O0, io.O0)
        m.wire(O1, io.O1)
