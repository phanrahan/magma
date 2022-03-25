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


@pytest.mark.parametrize("backend", ("mlir",))
def test_xmr(backend):

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

    ############################################################################
    from magma.primitives.wire import Wire

    class Wire2(m.Generator2):
        def __init__(self, T):
            self.io = io = m.IO(I=m.In(T), O=m.Out(T))
            I = m.as_bits(io.I)
            O = Wire(m.Bits[len(I)])()(I)
            io.O @= m.from_bits(T, O)

    inst = Top.instances[-1]
    args = [p.value() for p in list(inst.interface.ports.values())[len(Top.interface.ports):]]
    from magma.ref import PortViewRef
    for idx, arg in enumerate(args):
        if not isinstance(arg.name, PortViewRef):
            continue
        xmr = arg.name.view
        defn = xmr.parent.inst.defn
        with defn.open():
            value = xmr.port
            if value.is_input():
                value = value.value()
            Wire2(type(value))(name=f"bind_value_{idx}")(value)
        arg.name.view._resolved_ = "dasfdf"
    ############################################################################

    basename = "test_bind2_xmr"
    suffix = "mlir" if backend == "mlir" else "v"
    opts = {
        "output": backend,
        "use_native_bind_processor": True,
    }
    _assert_compilation(Top, basename, suffix, opts)
