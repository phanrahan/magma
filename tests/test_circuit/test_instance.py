import pytest

import magma as m


def test_callback_basic():

    def _callback(path, data):
        data[0] = (path,)

    class _Test(m.Circuit):
        reg = m.Register(m.Bit)(name="r")
        m.register_instance_callback(reg, _callback)

    path = [_Test]
    data = {}
    callback = m.get_instance_callback(_Test.reg)
    callback(path, data)
    assert data[0] == (path,)


def test_callback_missing():

    class _Test(m.Circuit):
        reg = m.Register(m.Bit)(name="r")

    with pytest.raises(AttributeError):
        m.get_instance_callback(_Test.reg)


def test_callback_registered():

    class _Test(m.Circuit):
        reg = m.Register(m.Bit)(name="r")

    m.register_instance_callback(_Test.reg, lambda _, __: None)
    with pytest.raises(AttributeError):
        m.register_instance_callback(_Test.reg, lambda _, __: None)
