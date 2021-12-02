import pytest
import magma as m

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
    with pytest.warns(DeprecationWarning):
        And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                                "O", m.Out(m.Bit))
        XOr2 = m.DeclareCircuit('XOr2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                                "O", m.Out(m.Bit))
        Logic2 = m.DefineCircuit('Logic2', 'I0', m.In(m.Bit), 'I1', m.In(m.Bit), 'O', m.Out(m.Bit))
        m.wire(XOr2()(And2()(Logic2.I0, Logic2.I1), 1), Logic2.O)
        m.EndCircuit()

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
    with pytest.warns(DeprecationWarning):
        And2 = m.DeclareCircuit('And2', "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                                "O", m.Out(m.Bit))
        circ = m.DefineCircuit("Test", "I0", m.In(m.Bits[3]), "I1", m.In(m.Bits[3]), "O", m.Out(m.Bits[3]))
        anon = m.join(m.map_(And2, 3))
        m.wire(circ.I0, anon.I0)
        m.wire(circ.I1, anon.I1)
        m.wire(circ.O, anon.O)
        m.EndCircuit()

    string = str(anon)
    assert string[:len("AnonymousCircuitInst")] == "AnonymousCircuitInst"
    assert string[-len("<I0: Array[(3, In(Bit))], I1: Array[(3, In(Bit))], O: Array[(3, Out(Bit))]>"):] == "<I0: Array[(3, In(Bit))], I1: Array[(3, In(Bit))], O: Array[(3, Out(Bit))]>"
    assert repr(anon) == 'AnonymousCircuitType("I0", array([And2_inst0.I0, And2_inst1.I0, And2_inst2.I0]), "I1", array([And2_inst0.I1, And2_inst1.I1, And2_inst2.I1]), "O", array([And2_inst0.O, And2_inst1.O, And2_inst2.O]))'
