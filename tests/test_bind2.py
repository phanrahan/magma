import pytest

import magma as m
import magma.testing


def _assert_compilation(ckt, basename, suffix, opts):
    m.compile(f"build/{basename}", ckt, **opts)
    assert m.testing.check_files_equal(
        __file__,
        f"build/{basename}.{suffix}",
        f"gold/{basename}.{suffix}")


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

    basename = f"test_bind2_basic"
    suffix = "mlir" if backend == "mlir" else "v"
    opts = {
        "output": backend,
        "use_native_bind_processor": True,
    }
    _assert_compilation(Top, basename, suffix, opts)


@pytest.mark.parametrize(
    "backend,flatten_all_tuples",
    (
        ("mlir", True),
        ("mlir", False),
    )
)
def test_xmr(backend, flatten_all_tuples):

    class T(m.Product):
        x = m.Bit
        y = m.Bit

    class Bottom(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I

    class Middle(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= Bottom(name="bottom")(io.I)

    class Top(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        middle = Middle(name="middle")
        io.O @= middle(io.I)

    class TopXMRAsserts(m.Circuit):
        name = f"TopXMRAsserts_{backend}"
        io = m.IO(I=m.In(T), O=m.In(T), a=m.In(T), b=m.In(m.Bit))
        io.I.unused()
        io.O.unused()
        io.a.unused()
        io.b.unused()

    m.bind2(Top, TopXMRAsserts, Top.middle.bottom.O, Top.middle.bottom.I.x)

    basename = "test_bind2_xmr"
    if flatten_all_tuples:
        basename += "_flatten_all_tuples"
    suffix = "mlir" if backend == "mlir" else "v"
    opts = {
        "output": backend,
        "use_native_bind_processor": True,
        "flatten_all_tuples": flatten_all_tuples,
    }
    _assert_compilation(Top, basename, suffix, opts)


def test_generator():

    class Logic(m.Generator2):
        def __init__(self, width=None):
            T = m.Bit if width is None else m.Bits[width]
            self.io = io = m.IO(I=m.In(T), O=m.Out(T))
            io.O @= ~io.I

    class LogicAsserts(m.Generator2):
        def __init__(self, dut, width=None):
            T = m.Bit if width is None else m.Bits[width]
            self.width = width
            self.io = io = m.IO(I=m.In(T), O=m.In(T), other=m.In(m.Bit))
            m.inline_verilog("{I} {O} {other}", I=io.I, O=io.O, other=io.other)
            self.bind2_args = [m.bits(dut.I)[0]]

    m.bind2(Logic, LogicAsserts)

    class Top(m.Circuit):
        T = m.Bits[2]
        io = m.IO(I=m.In(T), O=m.Out(T))
        I = m.bits(list(map(lambda x: Logic()()(x), io.I)))
        io.O @= Logic(2)()(I)

    opts = {
        "output": "mlir",
        "use_native_bind_processor": True,
    }
    _assert_compilation(Top, "test_bind2_generator", "mlir", opts)
