import functools
import tempfile

import magma as m


class _BinOpInterface(m.Circuit):
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))


class _OrImpl(m.Circuit):
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I0 | io.I1


class _AndImpl(m.Circuit):
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I0 & io.I1


class _XorImpl(m.Circuit):
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= io.I0 ^ io.I1


class _Top(m.Circuit):
    io = m.IO(I0=m.In(m.Bit), I1=m.In(m.Bit), O=m.Out(m.Bit))
    io.O @= _BinOpInterface()(io.I0, io.I1)


def _wrap_with_clear_link_info(fn):

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        m.clear_link_info()
        return fn()

    return wrapped


def _compile():
    with tempfile.TemporaryDirectory() as tempdir:
        basename = f"{tempdir}/Top"
        m.compile(basename, _Top, output="coreir")
    modules = m.backend.coreir.coreir_runtime.module_map()
    return modules[list(modules.keys())[0]]['global']


@_wrap_with_clear_link_info
def test_only_default():
    m.link_default_module(_BinOpInterface, _OrImpl)
    assert m.linking.has_default_linked_module(_BinOpInterface)
    assert m.linking.get_default_linked_module(_BinOpInterface) is _OrImpl
    modules = _compile()
    linked = modules["_BinOpInterface"].get_default_linked_module()
    assert linked is modules["_OrImpl"]
    assert not modules["_BinOpInterface"].get_linked_modules()  # expect empty


@_wrap_with_clear_link_info
def test_linked_modules_no_default():
    m.link_module(_BinOpInterface, "OR", _OrImpl)
    m.link_module(_BinOpInterface, "AND", _AndImpl)
    assert not m.linking.has_default_linked_module(_BinOpInterface)
    assert m.linking.get_linked_modules(_BinOpInterface) == {
        "OR": _OrImpl,
        "AND": _AndImpl,
    }
    modules = _compile()
    assert not modules["_BinOpInterface"].has_default_linked_module()
    linked = modules["_BinOpInterface"].get_linked_modules()
    assert len(linked) == 2
    assert linked["OR"] is modules["_OrImpl"]
    assert linked["AND"] is modules["_AndImpl"]


@_wrap_with_clear_link_info
def test_linked_modules_with_default():
    m.link_module(_BinOpInterface, "OR", _OrImpl)
    m.link_module(_BinOpInterface, "AND", _AndImpl)
    m.link_default_module(_BinOpInterface, _OrImpl)
    assert m.linking.get_linked_modules(_BinOpInterface) == {
        "OR": _OrImpl,
        "AND": _AndImpl,
    }
    assert m.linking.has_default_linked_module(_BinOpInterface)
    assert m.linking.get_default_linked_module(_BinOpInterface) is _OrImpl
    modules = _compile()
    linked = modules["_BinOpInterface"].get_default_linked_module()
    assert linked is modules["_OrImpl"]
    linked = modules["_BinOpInterface"].get_linked_modules()
    assert len(linked) == 2
    assert linked["OR"] is modules["_OrImpl"]
    assert linked["AND"] is modules["_AndImpl"]
