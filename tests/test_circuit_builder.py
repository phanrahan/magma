import magma as m


def test_basic():

    class _Top(m.Circuit):
        io = m.IO(x=m.In(m.Bit), y=m.Out(m.Bit))

        builder = m.CircuitBuilder(name="my_pt")
        builder.add("I", m.In(m.Bit))
        builder.add("O", m.Out(m.Bit))

        builder.I @= io.x
        io.y @= builder.O

    print (_Top._context_._builders)
    print (repr(_Top))

    m.compile("_Top", _Top, output="coreir")
