import pytest

import magma as m


def test_declare_simple():
    with pytest.warns(DeprecationWarning):
        And2 = m.DeclareCircuit("And2", "I0", m.In(m.Bit), "I1", m.In(m.Bit), "O",
                                m.Out(m.Bit))
    assert isinstance(And2.I0, m.Bit)


def test_declare_interface_polarity():
    with pytest.warns(DeprecationWarning):
        And2Decl = m.DeclareCircuit("And2", "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                                    "O", m.Out(m.Bit))
        And2Defn = m.DefineCircuit("And2", "I0", m.In(m.Bit), "I1", m.In(m.Bit),
                                   "O", m.Out(m.Bit))

    assert And2Decl.interface.ports["I0"].is_input() == \
        And2Defn.interface.ports["I0"].is_input()
