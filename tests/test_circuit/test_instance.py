import pytest

import magma as m
from magma.common import only


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


def test_getattr_instance_name():
    Bar = m.Register(m.Bit)  # just any module

    class Foo(m.Circuit):
        my_placeholder_var = Bar(name="my_instance_name")

    assert Foo.my_placeholder_var is Foo.my_instance_name


def test_getattr_instance_name_overwritten():
    Bar = m.Register(m.Bit)  # just any module

    class Foo(m.Circuit):
        my_placeholder_var = Bar(name="my_instance_name")
        my_instance_name = None

    assert Foo.my_instance_name is None
    assert Foo.my_placeholder_var is only(Foo.instances)


def test_getattr_attribute_error():

    class Foo(m.Circuit):
        pass

    with pytest.raises(AttributeError) as e:
        Foo.bar

    assert "has no attribute 'bar'" in str(e)


def test_get_instance_method():

    Bar = m.Register(m.Bit)  # just any module

    class Foo(m.Circuit):
        my_placeholder_var = Bar(name="my_instance_name")
        Bar(name="duplicated")
        Bar(name="duplicated")
        my_instance_name = None

    assert Foo.get_instance("my_instance_name") is Foo.my_placeholder_var
    with pytest.raises(KeyError):
        Foo.get_instance("blahblah")
    with pytest.raises(KeyError):
        Foo.get_instance("duplicated")
