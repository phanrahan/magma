
import magma as m


def test_declare_simple():
    And2 = m.DeclareCircuit("And2", "I0", m.In(m.Bit), "I1", m.In(m.Bit), "O",
                            m.Out(m.Bit))
    assert isinstance(And2.I0, m.BitType)


def test_declare_interface_polarity():
    And2Decl = m.DeclareCircuit("And2", "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                                "O", m.Out(m.Bit))
    And2Defn = m.DefineCircuit("And2", "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                               "O", m.Out(m.Bit))

    assert And2Decl.interface.ports["I0"].isinput() == \
        And2Defn.interface.ports["I0"].isinput()
