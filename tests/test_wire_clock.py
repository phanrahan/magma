import magma as m
from magma.wire_clock import wiredefaultclock
from magma.testing.utils import has_info, has_warning


def test_wire_clock_succesful_logging(caplog):
    T = m.Bit

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO()
        io.O @= m.register(io.I)

    Foo_reg = Foo.instances[0]
    wiredefaultclock(Foo, Foo_reg)

    msg = f"Auto-wiring {repr(Foo.CLK)} to {repr(Foo_reg.CLK)}"
    assert has_info(caplog, msg)


def test_wire_clock_no_clock_logging(caplog):
    T = m.Bit

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I

    with Foo.open():
        Foo.O.unwire(Foo.I)
        Foo.O @= m.register(Foo.I)

    Foo_reg = Foo.instances[0]
    wiredefaultclock(Foo, Foo_reg)

    msg = f"Found no clocks in {Foo.name}; skipping auto-wiring {m.Clock}"
    assert has_warning(caplog, msg)


def test_wire_clock_multiple_clocks_logging(caplog):
    T = m.Bit

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T), C0=m.In(m.Clock), C1=m.In(m.Clock))
        io.O @= m.register(io.I)

    Foo_reg = Foo.instances[0]
    wiredefaultclock(Foo, Foo_reg)

    msg = f"Found multiple clocks in {Foo.name}; skipping auto-wiring {m.Clock}"
    assert has_warning(caplog, msg)
