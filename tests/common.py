import magma as m


def DeclareAnd(width):
    T = m.util.BitOrBits(width)
    return m.DeclareCircuit(f'And{width}', "I0", m.In(T), "I1", m.In(T),
                            "O", m.Out(T))
