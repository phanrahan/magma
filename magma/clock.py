from .t import Direction, In
from .digital import DigitalMeta, Digital
from .wire import wire
from magma.bit import Bit
from magma.array import Array
from magma.tuple import Tuple


class _ClockType(Digital):
    @classmethod
    def is_clock(cls):
        return True

    def unused(self):
        Bit.unused(self)

    def undriven(self):
        Bit.undriven(self)


class Clock(_ClockType, metaclass=DigitalMeta):
    pass


ClockIn = Clock[Direction.In]
ClockOut = Clock[Direction.Out]


# synchronous reset, active high (i.e. reset when signal is 1)
class Reset(_ClockType, metaclass=DigitalMeta):
    pass


ResetIn = Reset[Direction.In]
ResetOut = Reset[Direction.Out]


# synchronous reset, active low (i.e. reset when signal is 0)
class ResetN(_ClockType, metaclass=DigitalMeta):
    pass


ResetNIn = ResetN[Direction.In]
ResetNOut = ResetN[Direction.Out]


# asynchronous reset, active high (i.e. reset when signal is 1)
class AsyncReset(_ClockType, metaclass=DigitalMeta):
    pass


AsyncResetIn = AsyncReset[Direction.In]
AsyncResetOut = AsyncReset[Direction.Out]


# asynchronous reset, active low (i.e. reset when signal is 0)
class AsyncResetN(_ClockType, metaclass=DigitalMeta):
    pass


AsyncResetNIn = AsyncResetN[Direction.In]
AsyncResetNOut = AsyncResetN[Direction.Out]


# Preset
# Clear
class Enable(_ClockType, metaclass=DigitalMeta):
    pass


EnableIn = Enable[Direction.In]
EnableOut = Enable[Direction.Out]

ClockTypes = (Clock, Reset, AsyncReset, Enable)


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


def _wire_clock_port(port, clocktype, defnclk):
    wired = False
    if isinstance(port, Tuple):
        for elem in port:
            wired |= _wire_clock_port(elem, clocktype, defnclk)
    elif isinstance(port, Array):
        wired = _wire_clock_port(port[0], clocktype, defnclk)
        # Only traverse all children circuit if first child has a clock
        if not wired:
            return False
        # TODO: Magma doesn't support length zero array, so slicing a
        # length 1 array off the end doesn't work as expected in normal
        # Python, so we explicilty slice port.ts
        for t in port.ts[1:]:
            for elem in port[1:]:
              _wire_clock_port(elem, clocktype, defnclk)
    elif isinstance(port, clocktype) and not port.driven():
        wire(defnclk, port)
        wired = True
    return wired


def _first(iterable):
    return next((item for item in iterable if item is not None), None)


def _get_first_clock(port, clocktype):
    if isinstance(port, clocktype):
        return port
    if isinstance(port, Tuple):
        clks = (_get_first_clock(elem, clocktype) for elem in port)
        return _first(clks)
    if isinstance(port, Array):
        return _get_first_clock(port[0], clocktype)
    return None


def wireclocktype(defn, inst, clocktype):
    # Check common case: top level clock port
    clks = (port if isinstance(port, clocktype) else None
            for port in defn.interface.ports.values())
    defnclk = _first(clks)
    if defnclk is None:
        # Check recursive types
        clks = (_get_first_clock(port, clocktype)
                for port in defn.interface.ports.values())
        defnclk = _first(clks)
    if defnclk is None:
        return
    for port in inst.interface.inputs(include_clocks=True):
        _wire_clock_port(port, clocktype, defnclk)


def wiredefaultclock(defn, inst):
    wireclocktype(defn, inst, Clock)


def wireclock(define, circuit):
    wireclocktype(define, circuit, Reset)
    wireclocktype(define, circuit, AsyncReset)
    wireclocktype(define, circuit, AsyncResetN)
    wireclocktype(define, circuit, Enable)
