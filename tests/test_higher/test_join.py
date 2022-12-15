import magma as m

def test_join():
    class And2(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))

    class _Top(m.Circuit):
        io = m.IO()
        and0 = And2(name='and0')
        and1 = And2(name='and1')
        a = m.join(and0, and1)

    assert repr(_Top.a) == 'AnonymousCircuitType("I0", array([and0.I0, and1.I0]), "I1", array([and0.I1, and1.I1]), "O", array([and0.O, and1.O]))'
