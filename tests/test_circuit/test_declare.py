import magma as m


class _And2(m.Circuit):
    name = "And2"
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))


def test_declare_repr():
    assert str(_And2) == 'And2(I0: In(Bit), I1: In(Bit), O: Out(Bit))'
    assert repr(_And2) == ('And2 = DeclareCircuit("And2", "I0", In(Bit), "I1", '
                           'In(Bit), "O", Out(Bit))')

    class _Top(m.Circuit):
        io = m.IO()
        and2 = _And2(name="and2")

    and2 = _Top.and2
    assert str(and2) == "and2<And2(I0: In(Bit), I1: In(Bit), O: Out(Bit))>"
    assert str(and2.I0) == "I0"


def test_declare_simple():
    assert isinstance(_And2.I0, m.Bit)


def test_declare_interface_polarity():

    class _And2Defn(m.Circuit):
        name = "And2"
        io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
        io.O <= io.I0  # just something to make this a definition

    assert (_And2.interface.ports["I0"].is_input() ==
            _And2Defn.interface.ports["I0"].is_input())
