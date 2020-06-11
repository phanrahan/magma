from .clock import AsyncReset, AsyncResetN, Clock, Enable, Reset, ResetN
from .interface import IO
from .t import In


def ClockIO(has_enable=False, has_reset=False, has_resetn=False, has_ce=False,
            has_async_reset=False, has_async_resetn=False):
    args = {'CLK': In(Clock)}
    has_enable |= has_ce
    if has_enable:
        args['CE'] = In(Enable)
    if has_reset:
        args['RESET'] = In(Reset)
    if has_resetn:
        args['RESETN'] = In(ResetN)
    if has_async_reset:
        args['ASYNCRESET'] = In(AsyncReset)
    if has_async_resetn:
        args['ASYNCRESETN'] = In(AsyncResetN)
    return IO(**args)
