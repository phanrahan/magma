from magma.array import Array
from magma.tuple import Tuple
from magma.primitives.wire import Wire
from magma.clock import (ClockTypes, Clock, Reset, Enable, ResetN, AsyncReset,
                         AsyncResetN)
from magma.common import only, IterableOnlyException
from magma.wire import wire


def get_clocks(port, clocktype):
    if port.is_input():
        # We are looking for default drivers (only need to consider outputs).
        return None
    if isinstance(port, clocktype):
        yield port
    if isinstance(port, Tuple):
        for elem in port:
            yield from get_clocks(elem, clocktype)
    if isinstance(port, Array):
        first_clks = get_clocks(port[0], clocktype)
        try:
            first_clk = next(first_clks)
        except StopIteration:
            # Exit early to avoid traversing children when unnecessary.
            return None
        yield first_clk
        yield from first_clks
        for elem in port[1:]:
            yield from get_clocks(elem, clocktype)


def get_clocks_from_defn(defn, clocktype):
    for port in defn.interface.ports.values():
        yield from get_clocks(port, clocktype)
    for inst in defn.instances:
        if isinstance(type(inst), Wire):
            # Skip clock wires, because they are both inputs and outputs, so we
            # don't treat them as default drivers
            continue
        for port in inst.interface.ports.values():
            yield from get_clocks(port, clocktype)


def get_default_clocks(defn):
    default_clocks = {}
    for clock_type in ClockTypes:
        clocks = get_clocks_from_defn(defn, clock_type)
        try:
            default_clocks[clock_type] = only(clocks)
        except IterableOnlyException:
            default_clocks[clock_type] = None
    return default_clocks


def wire_clock_port(port, clocktype, defnclk):
    wired = False
    if isinstance(port, Tuple):
        for elem in port:
            wired |= wire_clock_port(elem, clocktype, defnclk)
    elif isinstance(port, Array):
        wired = wire_clock_port(port[0], clocktype, defnclk)
        # Only traverse all children circuit if first child has a clock
        if not wired:
            return False
        # TODO: Magma doesn't support length zero array, so slicing a
        # length 1 array off the end doesn't work as expected in normal
        # Python, so we explicilty slice port.ts
        for t in port.ts[1:]:
            for elem in port[1:]:
                wire_clock_port(elem, clocktype, defnclk)
    elif isinstance(port, clocktype) and port.trace() is None:
        # Trace to last undriven driver
        while port.driven():
            port = port.value()
        wire(defnclk, port)
        wired = True
    return wired


def wireclocktype(defn, inst, clocktype):
    # Check common case: top level clock port
    clks = get_clocks_from_defn(defn, clocktype)
    try:
        defnclk = only(clks)
    except IterableOnlyException:
        return
    for port in inst.interface.inputs(include_clocks=True):
        wire_clock_port(port, clocktype, defnclk)


def wiredefaultclock(defn, inst):
    wireclocktype(defn, inst, Clock)


def wireclock(define, circuit):
    wireclocktype(define, circuit, Reset)
    wireclocktype(define, circuit, ResetN)
    wireclocktype(define, circuit, AsyncReset)
    wireclocktype(define, circuit, AsyncResetN)
    wireclocktype(define, circuit, Enable)


def wire_default_clock(port, clocks):
    clock_wired = False
    for type_, default_driver in clocks.items():
        if default_driver is not None:
            clock_wired |= wire_clock_port(port, type_, default_driver)
    return clock_wired
