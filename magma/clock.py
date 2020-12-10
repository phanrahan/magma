from typing import Optional

from .t import Direction, In
from .digital import DigitalMeta, Digital
from .wire import wire
from magma.bit import Bit
from magma.array import Array
from magma.debug import debug_wire
from magma.tuple import Tuple


class _ClockType(Digital):
    @classmethod
    def is_clock(cls):
        return True

    def unused(self):
        Bit.unused(self)

    def undriven(self):
        Bit.undriven(self)

    @classmethod
    def is_wireable(cls, other):
        # Wiring requires strict subclasses
        # Note: we use the standard wiring logic to enforce directionality,
        # so we just check with the undirected type here
        if not issubclass(other, cls.qualify(Direction.Undirected)):
            return False
        return True


class Clock(_ClockType, metaclass=DigitalMeta):
    pass


ClockIn = Clock[Direction.In]
ClockOut = Clock[Direction.Out]


class AbstractReset(_ClockType, metaclass=DigitalMeta):
    pass


# synchronous reset, active high (i.e. reset when signal is 1)
class Reset(AbstractReset):
    pass


ResetIn = Reset[Direction.In]
ResetOut = Reset[Direction.Out]


# synchronous reset, active low (i.e. reset when signal is 0)
class ResetN(AbstractReset):
    pass


ResetNIn = ResetN[Direction.In]
ResetNOut = ResetN[Direction.Out]


# asynchronous reset, active high (i.e. reset when signal is 1)
class AsyncReset(AbstractReset):
    pass


AsyncResetIn = AsyncReset[Direction.In]
AsyncResetOut = AsyncReset[Direction.Out]


# asynchronous reset, active low (i.e. reset when signal is 0)
class AsyncResetN(AbstractReset):
    pass


AsyncResetNIn = AsyncResetN[Direction.In]
AsyncResetNOut = AsyncResetN[Direction.Out]


# Preset
# Clear
class Enable(Bit):
    pass


EnableIn = Enable[Direction.In]
EnableOut = Enable[Direction.Out]

ClockTypes = (Clock, Reset, ResetN, AsyncReset, AsyncResetN, Enable)


def ClockInterface(has_enable=False, has_reset=False, has_ce=False,
                   has_async_reset=False, has_async_resetn=False):
    args = ['CLK', In(Clock)]
    has_enable |= has_ce
    if has_enable:
        args += ['CE', In(Enable)]
    if has_reset:
        args += ['RESET', In(Reset)]
    if has_async_reset:
        args += ['ASYNCRESET', In(AsyncReset)]
    if has_async_resetn:
        args += ['ASYNCRESETN', In(AsyncResetN)]
    return args


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


def first(iterable):
    return next((item for item in iterable if item is not None), None)


def get_first_clock(port, clocktype):
    if isinstance(port, clocktype):
        return port
    if isinstance(port, Tuple):
        clks = (get_first_clock(elem, clocktype) for elem in port)
        return first(clks)
    if isinstance(port, Array):
        return get_first_clock(port[0], clocktype)
    return None


def wireclocktype(defn, inst, clocktype):
    # Check common case: top level clock port
    clks = (port if isinstance(port, clocktype) else None
            for port in defn.interface.ports.values())
    defnclk = first(clks)
    if defnclk is None:
        # Check recursive types
        clks = (get_first_clock(port, clocktype)
                for port in defn.interface.ports.values())
        defnclk = first(clks)
    if defnclk is None:
        return
    for port in inst.interface.inputs(include_clocks=True):
        wire_clock_port(port, clocktype, defnclk)


def wiredefaultclock(defn, inst):
    wireclocktype(defn, inst, Clock)


def wireclock(define, circuit):
    wireclocktype(define, circuit, Reset)
    wireclocktype(define, circuit, AsyncReset)
    wireclocktype(define, circuit, AsyncResetN)
    wireclocktype(define, circuit, Enable)


def get_reset_args(reset_type: Optional[AbstractReset]):
    if reset_type is None:
        return tuple(False for _ in range(4))
    if not issubclass(reset_type, AbstractReset):
        raise TypeError(
            f"Expected subclass of AbstractReset for argument reset_type, "
            f"not {type(reset_type)}")

    has_async_reset = issubclass(reset_type, AsyncReset)
    has_async_resetn = issubclass(reset_type, AsyncResetN)
    has_reset = issubclass(reset_type, Reset)
    has_resetn = issubclass(reset_type, ResetN)
    return (has_async_reset, has_async_resetn, has_reset, has_resetn)


def get_default_clocks(defn):
    clocks = {}
    for clock_type in ClockTypes:
        clocks[clock_type] = first(
            get_first_clock(port, clock_type)
            for port in defn.interface.ports.values()
        )
    return clocks


def is_clock_or_nested_clock(p):
    if issubclass(p, ClockTypes):
        return True
    if issubclass(p, Array):
        return is_clock_or_nested_clock(p.T)
    if issubclass(p, Tuple):
        for item in p.types():
            if is_clock_or_nested_clock(item):
                return True
    return False


def wire_default_clock(port, clocks):
    clock_wired = False
    for type_, default_driver in clocks.items():
        if default_driver is not None:
            clock_wired |= wire_clock_port(port, type_, default_driver)
    return clock_wired
