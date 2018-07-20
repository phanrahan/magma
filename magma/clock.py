from .port import INPUT, OUTPUT, INOUT
from .t import In, Out, InOut
from .bit import Bit, _BitKind, _BitType
from .wire import wire

__all__  = ['ClockKind', 'ClockType']
__all__ += ['Clock', 'ClockIn', 'ClockOut']

__all__ += ['ResetKind', 'ResetType']
__all__ += ['Reset', 'ResetIn', 'ResetOut']

__all__ += ['AsyncResetKind', 'AsyncResetType']
__all__ += ['AsyncReset', 'AsyncResetIn', 'AsyncResetOut']

__all__ += ['EnableKind', 'EnableType']
__all__ += ['Enable', 'EnableIn', 'EnableOut']

__all__ += ['ClockInterface', 'ClockTypes']
__all__ += ['wireclock', 'wireclocktype', 'wiredefaultclock']




class ClockKind(_BitKind):
    def __str__(cls):
        if cls.isinput():  return 'In(Clock)'
        if cls.isoutput(): return 'Out(Clock)'
        return 'Clock'

    def qualify(cls, direction):
        if   direction is None:   return Clock
        elif direction == INPUT:  return ClockIn
        elif direction == OUTPUT: return ClockOut
        return cls

    def flip(cls):
        if   cls.isoriented(INPUT):  return ClockOut
        elif cls.isoriented(OUTPUT): return ClockIn
        return cls

class ClockType(_BitType):
    pass

Clock = ClockKind('Clock', (ClockType,), {})
ClockIn = ClockKind('Clock', (ClockType,), dict(direction=INPUT))
ClockOut = ClockKind('Clock', (ClockType,), dict(direction=OUTPUT))


class ResetKind(_BitKind):
    def __str__(cls):
        if cls.isinput():  return 'In(Reset)'
        if cls.isoutput(): return 'Out(Reset)'
        return 'Reset'

    def qualify(cls, direction):
        if   direction is None:   return Reset
        elif direction == INPUT:  return ResetIn
        elif direction == OUTPUT: return ResetOut
        return cls

    def flip(cls):
        if   cls.isoriented(INPUT):  return ResetOut
        elif cls.isoriented(OUTPUT): return ResetIn
        return cls

class ResetType(_BitType):
    pass

Reset = ResetKind('Reset', (ResetType,), {})
ResetIn = ResetKind('Reset', (ResetType,), dict(direction=INPUT))
ResetOut = ResetKind('Reset', (ResetType,), dict(direction=OUTPUT))

class AsyncResetKind(_BitKind):
    def __str__(cls):
        if cls.isinput():  return 'In(AsyncReset)'
        if cls.isoutput(): return 'Out(AsyncReset)'
        return 'AsyncReset'

    def qualify(cls, direction):
        if   direction is None:   return AsyncReset
        elif direction == INPUT:  return AsyncResetIn
        elif direction == OUTPUT: return AsyncResetOut
        return cls

    def flip(cls):
        if   cls.isoriented(INPUT):  return AsyncResetOut
        elif cls.isoriented(OUTPUT): return AsyncResetIn
        return cls

class AsyncResetType(_BitType):
    pass

AsyncReset = AsyncResetKind('AsyncReset', (AsyncResetType,), {})
AsyncResetIn = AsyncResetKind('AsyncReset', (AsyncResetType,), dict(direction=INPUT))
AsyncResetOut = AsyncResetKind('AsyncReset', (AsyncResetType,), dict(direction=OUTPUT))

# Preset
# Clear

class EnableKind(_BitKind):
    def __str__(cls):
        if cls.isinput():  return 'In(Enable)'
        if cls.isoutput(): return 'Out(Enable)'
        return 'Enable'

    def qualify(cls, direction):
        if   direction is None:   return Enable
        elif direction == INPUT:  return EnableIn
        elif direction == OUTPUT: return EnableOut
        return cls

    def flip(cls):
        if   cls.isoriented(INPUT):  return EnableOut
        elif cls.isoriented(OUTPUT): return EnableIn
        return cls

class EnableType(_BitType):
    pass

Enable = EnableKind('Enable', (EnableType,), {})
EnableIn = EnableKind('Enable', (EnableType,), dict(direction=INPUT))
EnableOut = EnableKind('Enable', (EnableType,), dict(direction=OUTPUT))

ClockTypes = (ClockType, ResetType, AsyncResetType, EnableType)


def ClockInterface(has_enable=False, has_reset=False, has_set=False,
                   has_ce=False, has_async_reset=False):
    args = ['CLK', In(Clock)]
    has_enable |= has_ce
    if has_enable:
        args += ['CE', In(Enable)]
    if has_reset:
        args += ['RESET', In(Reset)]
    if has_async_reset:
        args += ['ASYNCRESET', In(AsyncReset)]
    return args


def wireclocktype(defn, inst, clocktype):
    #print('wiring clocks', str(defn), str(inst))
    defnclk = []
    for name, port in defn.interface.ports.items():
         if isinstance(port, clocktype) and port.isoutput():
             #print('defn clock', port)
             defnclk += [port]
    if defnclk:
        defnclk = defnclk[0] # wire first clock
        for name, port in inst.interface.ports.items():
             if isinstance(port, clocktype) and port.isinput() and not port.driven():
                 #print('inst clock', port)
                 wire(defnclk, port)

def wiredefaultclock(defn, inst):
    wireclocktype(defn, inst, ClockType)

def wireclock(define, circuit):
    wireclocktype(define, circuit, ResetType)
    wireclocktype(define, circuit, AsyncResetType)
    wireclocktype(define, circuit, EnableType)
