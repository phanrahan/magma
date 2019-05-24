import magma as m


def test_add_ports_basic():
    Foo = m.DefineCircuit("Foo", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    m.EndCircuit()

    Foo.add_port("I2", m.In(m.Bit))
    assert isinstance(Foo.I2, m._BitType)

    # Instance Foo *after* adding a port.
    foo = Foo()
    assert isinstance(Foo.I2, m._BitType)


def test_add_ports_previous_instance():
    Foo = m.DefineCircuit("Foo", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    m.EndCircuit()

    # Instacne Foo *before* adding a port.
    foo = Foo()
    assert not hasattr(foo, "I2")
    
    Foo.add_port("I2", m.In(m.Bit))
    assert isinstance(Foo.I2, m._BitType)

    assert isinstance(Foo.I2, m._BitType)
