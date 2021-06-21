import magma as m


def test_circuit_base_attr():

    class _FooInterface(m.Circuit):
        _circuit_base_ = True

    class _FooBase(_FooInterface):
        pass

    class _FooImpl(_FooBase):
        pass

    assert _FooInterface._circuit_base_ == True
    assert _FooBase._circuit_base_ == False
    assert _FooImpl._circuit_base_ == False
