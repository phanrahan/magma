import magma as m

def test_fork():
    class And2(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))

    class Or2(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))

    class _Top(m.Circuit):
        io = m.IO()
        and2 = And2(name='and2')
        or2 = Or2(name='or2')
        lut = m.fork(and2,or2)

    assert str(_Top.and2.interface) == 'Interface("I0", In(Bit), "I1", In(Bit), "O", Out(Bit))'
    assert str(_Top.or2.interface) == 'Interface("I0", In(Bit), "I1", In(Bit), "O", Out(Bit))'
    assert len(_Top.lut.interface) == 3
