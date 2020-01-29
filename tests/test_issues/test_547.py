import magma as m

def test_basic():
    class Test(m.Circuit):
        IO = ["I", m.In(m.Bits[1]), "O", m.Out(m.Bits[1])]

        @classmethod
        def definition(io):
            io.O[0] @= io.I[0]

def test_slice():
    class Test(m.Circuit):
        IO = ["I", m.In(m.Bits[2]), "O", m.Out(m.Bits[2])]

        @classmethod
        def definition(io):
            io.O[:] @= io.I[:]

def test_compound():
    class Test(m.Circuit):
        IO = ["I0", m.In(m.Bits[1]), "I1", m.In(m.Bits[1]), "O", m.Out(m.Bits[2])]

        @classmethod
        def definition(io):
            io.O[0] @= io.I0
            io.O[1] @= io.I1


