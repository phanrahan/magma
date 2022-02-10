import magma as m


class And2(m.Circuit):
    name = "And2"
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))


def test_str_repr_core():
    #Dont care what values they return as long as they retun non empty strings
    assert str(m.Circuit)
    assert repr(m.Circuit)
    assert str(m.circuit.CircuitKind)
    assert repr(m.circuit.CircuitKind)
    assert str(m.CircuitType)
    assert repr(m.CircuitType)
    assert str(m.AnonymousCircuitType)
    assert repr(m.AnonymousCircuitType)


def test_str_repr():

    class XOr2(m.Circuit):
        name = "XOr2"
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))

    class Logic2(m.Circuit):
        name = "Logic2"
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
        m.wire(XOr2()(And2()(io.I0, io.I1), 1), io.O)

    assert str(Logic2) == "Logic2(I0: In(Bit), I1: In(Bit), O: Out(Bit))"
    print(repr(Logic2))
    assert repr(Logic2) == """\
Logic2 = DefineCircuit("Logic2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
And2_inst0 = And2()
XOr2_inst0 = XOr2()
wire(Logic2.I0, And2_inst0.I0)
wire(Logic2.I1, And2_inst0.I1)
wire(And2_inst0.O, XOr2_inst0.I0)
wire(VCC, XOr2_inst0.I1)
wire(XOr2_inst0.O, Logic2.O)
EndCircuit()\
"""

    expected = [
        "XOr2_inst0<XOr2(I0: In(Bit), I1: In(Bit), O: Out(Bit))>",
        "And2_inst0<And2(I0: In(Bit), I1: In(Bit), O: Out(Bit))>"
    ]
    for inst, expected in zip(Logic2.instances, expected):
        assert str(inst) == expected


def test_str_repr_anon():

    class circ(m.Circuit):
        name = "Test"
        io = m.IO(I0=m.In(m.Bits[3]), I1=m.In(m.Bits[3]), O=m.Out(m.Bits[3]))
        anon = m.join(m.map_(And2, 3))
        m.wire(io.I0, anon.I0)
        m.wire(io.I1, anon.I1)
        m.wire(io.O, anon.O)

    string = str(circ.anon)
    assert string[:len("AnonymousCircuitInst")] == "AnonymousCircuitInst"
    assert string[-len("<I0: Array[(3, In(Bit))], I1: Array[(3, In(Bit))], O: Array[(3, Out(Bit))]>"):] == "<I0: Array[(3, In(Bit))], I1: Array[(3, In(Bit))], O: Array[(3, Out(Bit))]>"
    assert repr(circ.anon) == 'AnonymousCircuitType("I0", array([And2_inst0.I0, And2_inst1.I0, And2_inst2.I0]), "I1", array([And2_inst0.I1, And2_inst1.I1, And2_inst2.I1]), "O", array([And2_inst0.O, And2_inst1.O, And2_inst2.O]))'
