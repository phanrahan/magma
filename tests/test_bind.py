import pytest

import magma as m
import magma.testing


@pytest.mark.parametrize("backend", ("coreir-verilog", "mlir"))
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

    m.compile(f"build/test_bind_basic_{backend}", Top, output=backend)

    suffix = "mlir" if backend == "mlir" else "v"
    assert m.testing.check_files_equal(
        __file__,
        f"build/test_bind_basic_{backend}.{suffix}",
        f"gold/test_bind_basic_{backend}.{suffix}")
    assert m.testing.check_files_equal(
        __file__,
        f"build/TopBasicAsserts_{backend}.sv",
        f"gold/TopBasicAsserts_{backend}.sv")
    list_filename = f"tests/build/test_bind_basic_{backend}_bind_files.list"
    with open(list_filename, "r") as f:
        list_contents = f.read()
    assert list_contents == f"TopBasicAsserts_{backend}.sv"
