import functools
import pytest
import tempfile

import magma as m
from magma.testing import check_files_equal


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
        return fn(*args, **kwargs)

    return wrapped


def _compile(output, basename=None):
    if output == "coreir":
        with tempfile.TemporaryDirectory() as tempdir:
            basename = f"{tempdir}/Top"
            m.compile(basename, _Top, output="coreir")
        modules = m.backend.coreir.coreir_runtime.module_map()
        return modules[list(modules.keys())[0]]['global']
    if output == "mlir":
        m.compile(f"build/{basename}", _Top, output="mlir")
        return
    raise NotImplementedError(output)


def _make_basename(output, basename):
    if output == "coreir":
        return None
    if output == "mlir":
        return basename
    raise NotImplementedError(output)


def _run_file_check(basename):
    assert check_files_equal(
        __file__, f"build/{basename}.mlir", f"gold/{basename}.mlir")


@_wrap_with_clear_link_info
@pytest.mark.parametrize("output", ("coreir", "mlir"))
def test_only_default(output):
    m.link_default_module(_BinOpInterface, _OrImpl)
    assert m.linking.has_default_linked_module(_BinOpInterface)
    assert m.linking.get_default_linked_module(_BinOpInterface) is _OrImpl
    basename = _make_basename(output, "test_module_linking_only_default")
    modules = _compile(output, basename=basename)
    if output == "coreir":
        linked = modules["_BinOpInterface"].get_default_linked_module()
        assert linked is modules["_OrImpl"]
        assert not modules["_BinOpInterface"].get_linked_modules()  # expect empty
        return
    if output == "mlir":
        _run_file_check(basename)
        return
    raise NotImplementedError(output)


@_wrap_with_clear_link_info
@pytest.mark.parametrize("output", ("coreir", "mlir"))
def test_linked_modules_no_default(output):
    m.link_module(_BinOpInterface, "OR", _OrImpl)
    m.link_module(_BinOpInterface, "AND", _AndImpl)
    assert not m.linking.has_default_linked_module(_BinOpInterface)
    assert m.linking.get_linked_modules(_BinOpInterface) == {
        "OR": _OrImpl,
        "AND": _AndImpl,
    }
    basename = _make_basename(output, "test_module_linking_no_default")
    modules = _compile(output, basename=basename)
    if output == "coreir":
        assert not modules["_BinOpInterface"].has_default_linked_module()
        linked = modules["_BinOpInterface"].get_linked_modules()
        assert len(linked) == 2
        assert linked["OR"] is modules["_OrImpl"]
        assert linked["AND"] is modules["_AndImpl"]
        return
    if output == "mlir":
        _run_file_check(basename)
        return
    raise NotImplementedError(output)


@_wrap_with_clear_link_info
@pytest.mark.parametrize("output", ("coreir", "mlir"))
def test_linked_modules_with_default(output):
    m.link_module(_BinOpInterface, "OR", _OrImpl)
    m.link_module(_BinOpInterface, "AND", _AndImpl)
    m.link_default_module(_BinOpInterface, _OrImpl)
    assert m.linking.get_linked_modules(_BinOpInterface) == {
        "OR": _OrImpl,
        "AND": _AndImpl,
    }
    assert m.linking.has_default_linked_module(_BinOpInterface)
    assert m.linking.get_default_linked_module(_BinOpInterface) is _OrImpl
    basename = _make_basename(output, "test_module_linking_with_default")
    modules = _compile(output, basename=basename)
    if output == "coreir":
        linked = modules["_BinOpInterface"].get_default_linked_module()
        assert linked is modules["_OrImpl"]
        linked = modules["_BinOpInterface"].get_linked_modules()
        assert len(linked) == 2
        assert linked["OR"] is modules["_OrImpl"]
        assert linked["AND"] is modules["_AndImpl"]
        return
    if output == "mlir":
        _run_file_check(basename)
        return
    raise NotImplementedError(output)
