import magma as m

def test_flat():

    class F(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bits[2]]), O=m.Out(m.Bit))

    class _Top(m.Circuit):
        io = m.IO()
        f = F(name="f")
        g = m.flat(f)

    assert len(_Top.g.interface) == 2
    assert len(_Top.g.I) == 4

def test_partition():
    class F(m.Circuit):
        io = m.IO(I=m.In(m.Bits[4]), O=m.Out(m.Bit))

    class _Top(m.Circuit):
        io = m.IO()
        f = F(name="f")
        g = m.partition(f, 2)

    assert len(_Top.g.interface) == 3
    assert len(_Top.g.I0) == 2
    assert len(_Top.g.I1) == 2
