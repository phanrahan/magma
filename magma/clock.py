from .t import Direction, In
from .digital import DigitalMeta, Digital
from .wire import wire


class Clock(Digital, metaclass=DigitalMeta):
    pass


ClockIn = Clock[Direction.In]
ClockOut = Clock[Direction.Out]


# synchronous reset, active high (i.e. reset when signal is 1)
class Reset(Digital, metaclass=DigitalMeta):
    pass


ResetIn = Reset[Direction.In]
ResetOut = Reset[Direction.Out]


# synchronous reset, active low (i.e. reset when signal is 0)
class ResetN(Digital, metaclass=DigitalMeta):
    pass


ResetNIn = ResetN[Direction.In]
ResetNOut = ResetN[Direction.Out]


# asynchronous reset, active high (i.e. reset when signal is 1)
class AsyncReset(Digital, metaclass=DigitalMeta):
    pass


AsyncResetIn = AsyncReset[Direction.In]
AsyncResetOut = AsyncReset[Direction.Out]


# asynchronous reset, active low (i.e. reset when signal is 0)
class AsyncResetN(Digital, metaclass=DigitalMeta):
    pass


AsyncResetNIn = AsyncResetN[Direction.In]
AsyncResetNOut = AsyncResetN[Direction.Out]


# Preset
# Clear
class Enable(Digital, metaclass=DigitalMeta):
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


def wireclocktype(defn, inst, clocktype):
    defnclk = []
    for port in defn.interface.ports.values():
        if isinstance(port, clocktype) and port.is_output():
            defnclk += [port]
    if defnclk:
        defnclk = defnclk[0]  # wire first clock
        for port in inst.interface.ports.values():
            if isinstance(port, clocktype) and port.is_input() and not port.driven():
                wire(defnclk, port)


def wiredefaultclock(defn, inst):
    wireclocktype(defn, inst, Clock)


def wireclock(define, circuit):
    wireclocktype(define, circuit, Reset)
    wireclocktype(define, circuit, AsyncReset)
    wireclocktype(define, circuit, AsyncResetN)
    wireclocktype(define, circuit, Enable)
