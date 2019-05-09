
import magma as m


def test_declare_simple():
    And2 = m.DeclareCircuit("And2", "I0", m.In(m.Bit), "I1", m.In(m.Bit), "O",
                            m.Out(m.Bit))
    assert isinstance(And2.I0, m.BitType)
