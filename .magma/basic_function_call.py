class basic_function_call(m.Circuit):
    IO = ['I', m.In(m.Bits(2)), 'S', m.In(m.Bit), 'O', m.Out(m.Bit)]

    @classmethod
    def definition(io):
        O = basic_func(io.I, io.S)
        m.wire(O, io.O)
