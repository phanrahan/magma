import magma as m


def test_str_repr():
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))
    XOr2 = m.DeclareCircuit('XOr2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))
    Logic2 = m.DefineCircuit('Logic2', 'I0', m.In(m.Bit), 'I1', m.In(m.Bit), 'O', m.Out(m.Bit))
    m.wire(XOr2()(And2()(Logic2.I0, Logic2.I1), 1), Logic2.O)
    m.EndCircuit()

    assert str(Logic2) == "Logic2(I0: In(Bit), I1: In(Bit), O: Out(Bit))"
    assert repr(Logic2) == """\
Logic2 = DefineCircuit("Logic2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
inst0 = XOr2()
inst1 = And2()
wire(inst1.O, inst0.I0)
wire(1, inst0.I1)
wire(Logic2.I0, inst1.I0)
wire(Logic2.I1, inst1.I1)
wire(inst0.O, Logic2.O)
EndCircuit()\
"""

    expected = [
        "inst0<XOr2(I0: In(Bit), I1: In(Bit), O: Out(Bit))>",
        "inst1<And2(I0: In(Bit), I1: In(Bit), O: Out(Bit))>"
    ]
    for inst, expected in zip(Logic2.instances, expected):
        assert str(inst) == expected


def test_str_repr_anon():
    And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                            "O", m.Out(m.Bit))
    circ = m.DefineCircuit("Test", "I0", m.In(m.Bits(3)), "I1", m.In(m.Bits(3)), "O", m.Out(m.Bits(3)))
    anon = m.join(m.map_(And2, 3))
    m.wire(circ.I0, anon.I0)
    m.wire(circ.I1, anon.I1)
    m.wire(circ.O, anon.O)
    m.EndCircuit()

    string = str(anon)
    assert string[:len("AnonymousCircuitInst")] == "AnonymousCircuitInst"
    assert string[-len("<I0: Array(3,In(Bit)), I1: Array(3,In(Bit)), O: Array(3,Out(Bit))>"):] == "<I0: Array(3,In(Bit)), I1: Array(3,In(Bit)), O: Array(3,Out(Bit))>"
    assert repr(anon) == 'AnonymousCircuitType("I0", array([inst0.I0, inst1.I0, inst2.I0]), "I1", array([inst0.I1, inst1.I1, inst2.I1]), "O", array([inst0.O, inst1.O, inst2.O]))'
