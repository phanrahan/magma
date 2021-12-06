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


def is_clock_or_nested_clock(p, types=ClockTypes):
    if issubclass(p, types):
        return True
    if issubclass(p, Array):
        return is_clock_or_nested_clock(p.T, types)
    if issubclass(p, Tuple):
        for item in p.types():
            if is_clock_or_nested_clock(item, types):
                return True
    return False
