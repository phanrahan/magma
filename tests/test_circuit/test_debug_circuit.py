import magma as m


def test_debug_circuit():
    assert m.config.get_debug_mode() is False

    class Foo(m.DebugCircuit):
        assert m.config.get_debug_mode() is True
        io = m.IO(I=m.In(m.Bit))

    assert m.config.get_debug_mode() is False


def test_debug_generator():
    assert m.config.get_debug_mode() is False

    class Foo(m.DebugGenerator2):
        def __init__(self, n: int):
            assert m.config.get_debug_mode() is True
            self.io = m.IO(I=m.In(m.Bits[n]))

    Foo(4)
    assert m.config.get_debug_mode() is False
