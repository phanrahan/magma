import pytest

import magma as m
import magma.testing


def _parameterize_by_backend(fn):
    return pytest.mark.parametrize("backend", ("coreir-verilog", "mlir"))(fn)


def _run_test(dut, bound_module, basename, backend):
    m.compile(f"build/{basename}_{backend}", dut, output=backend)

    suffix = "mlir" if backend == "mlir" else "v"
    assert m.testing.check_files_equal(
        __file__,
        f"build/{basename}_{backend}.{suffix}",
        f"gold/{basename}_{backend}.{suffix}")
    assert m.testing.check_files_equal(
        __file__,
        f"build/{bound_module.name}.sv",
        f"gold/{bound_module.name}.sv")
    list_filename = f"tests/build/{basename}_{backend}_bind_files.list"
    with open(list_filename, "r") as f:
        list_contents = f.read()
    assert list_contents == f"{bound_module.name}.sv"


@_parameterize_by_backend
def test_basic(backend):

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= io.I

    class TopBasicAsserts(m.Circuit):
        name = f"TopBasicAsserts_{backend}"
        io = m.IO(I=m.In(m.Bit), O=m.In(m.Bit), other=m.In(m.Bit))
        io.I.unused()
        io.O.unused()
        io.other.unused()

    Top.bind(TopBasicAsserts, Top.I)

    _run_test(Top, TopBasicAsserts, "test_bind_basic", backend)


@_parameterize_by_backend
def test_xmr(backend):

    class Bottom(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= io.I

    class Middle(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= Bottom(name="bottom")(io.I)

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        middle = Middle(name="middle")
        io.O @= middle(io.I)

    class TopXMRAsserts(m.Circuit):
        name = f"TopXMRAsserts_{backend}"
        io = m.IO(I=m.In(m.Bit), O=m.In(m.Bit), other=m.In(m.Bit))
        io.I.unused()
        io.O.unused()
        io.other.unused()

    Top.bind(TopXMRAsserts, Top.middle.bottom.I)

    _run_test(Top, TopXMRAsserts, "test_bind_xmr", backend)
