import magma as m


def DeclareAnd(width):
    T = m.util.BitOrBits(width)
    class And(m.Circuit):
        name = f'And{width}'
        io = m.IO(I0=m.In(T), I1=m.In(T), O=m.Out(T))
    return And
