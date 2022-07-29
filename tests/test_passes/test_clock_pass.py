import logging

import magma as m
from magma.passes.clock import drive_undriven_clock_types_in_inst
from magma.testing.utils import has_debug, has_warning


def test_drive_undriven_clock_types_succesful_logging(caplog):
    T = m.Bit

    with caplog.at_level(logging.DEBUG, logger="magma"):
        class Foo(m.Circuit):
            io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO()
            io.O @= m.register(io.I)

        Foo_reg = Foo.instances[0]
        drive_undriven_clock_types_in_inst(Foo, Foo_reg)

    msg = f"Auto-wiring {repr(Foo.CLK)} to {repr(Foo_reg.CLK)}"
    assert has_debug(caplog, msg)


def test_drive_undriven_clock_types_no_clock_logging(caplog):
    T = m.Bit

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I

    with Foo.open():
        Foo.O.unwire(Foo.I)
        Foo.O @= m.register(Foo.I)

    Foo_reg = Foo.instances[0]
    drive_undriven_clock_types_in_inst(Foo, Foo_reg)

    msg = f"Found no clocks in {Foo.name}; skipping auto-wiring {m.Clock}"
    assert has_warning(caplog, msg)


def test_drive_undriven_clock_types_multiple_clocks_logging(caplog):
    T = m.Bit

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T), C0=m.In(m.Clock), C1=m.In(m.Clock))
        io.O @= m.register(io.I)

    Foo_reg = Foo.instances[0]
    drive_undriven_clock_types_in_inst(Foo, Foo_reg)

    msg = (
        f"Found multiple clocks in {Foo.name}; skipping auto-wiring {m.Clock} "
        f"(Foo.C0, Foo.C1)"
    )
    assert has_warning(caplog, msg)


def test_drive_undriven_clock_types_combinational_logging(caplog):
    T = m.Bit

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= ~io.I

    inst = Foo.instances[0]
    drive_undriven_clock_types_in_inst(Foo, inst)

    msg = f"Found no clocks in {Foo.name}; skipping auto-wiring {m.Clock}"
    assert not has_warning(caplog, msg)
