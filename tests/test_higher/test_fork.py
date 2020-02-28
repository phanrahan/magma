import magma as m

def test_fork():
    class And2(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    #print(repr(And2))
    and2 = And2(name='and2')
    #print(repr(type(and2)))
    #print(and2)
    #print(repr(and2))
    assert str(and2.interface) == '"I0", In(Bit), "I1", In(Bit), "O", Out(Bit)'

    class Or2(m.Circuit):
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    or2 = Or2(name='or2')
    #print(or2)
    #print(repr(type(or2)))
    assert str(or2.interface) == '"I0", In(Bit), "I1", In(Bit), "O", Out(Bit)'

    lut = m.fork(and2,or2)
    assert len(lut.interface) == 3
    #print(type(lut))
    #print(repr(lut))

test_fork()
