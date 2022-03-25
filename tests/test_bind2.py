import pytest

import magma as m
import magma.testing


@pytest.mark.parametrize("backend", ("mlir",))
def test_basic(backend):

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= ~io.I

    class TopBasicAsserts(m.Circuit):
        name = f"TopBasicAsserts_{backend}"
        io = m.IO(I=m.In(m.Bit), O=m.In(m.Bit), other=m.In(m.Bit))
        io.I.unused()
        io.O.unused()
        io.other.unused()

    m.bind2(Top, TopBasicAsserts, Top.I)

    basename = "test_bind2_basic"
    kwargs = {
        "output": backend,
        "use_native_bind_processor": True,
    }
    m.compile(f"build/{basename}", Top, **kwargs)

    suffix = "mlir" if backend == "mlir" else "v"
    assert m.testing.check_files_equal(
        __file__,
        f"build/{basename}.{suffix}",
        f"gold/{basename}.{suffix}")
