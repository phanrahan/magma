from .port import INPUT, OUTPUT, INOUT
from .t import In, Out, InOut
from .bit import Bit, _BitKind, _BitType
from .wire import wire

__all__  = ['ClockKind', 'ClockType']
__all__ += ['Clock', 'ClockIn', 'ClockOut','ClockInOut']

__all__ += ['ClockInterface']

__all__ += ['wireclock', 'wiredefaultclock']

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
ClockInOut = ClockKind('Clock', (ClockType,), dict(direction=INOUT))


def ClockInterface(has_ce=False, has_reset=False, has_set=False):
    args = ['CLK', In(Clock)]
    if has_ce: args += ['CE', In(Bit)]
    if has_reset:  args += ['RESET', In(Bit)]
    if has_set:  args += ['SET', In(Bit)]
    return args

def wireclock(define, circuit):
    if hasattr(define,'CE'):
        assert hasattr(circuit, 'CE')
        wire(define.CE,    circuit.CE)
    if hasattr(define,'RESET'):  
        assert hasattr(circuit, 'RESET')
        wire(define.RESET, circuit.RESET)
    if hasattr(define,'SET'):    
        assert hasattr(circuit, 'SET')
        wire(define.SET,   circuit.SET)

def wiredefaultclock(defn, inst):
    #print('wiring clocks', str(defn), str(inst))
    defnclk = None
    for name, port in defn.interface.ports.items():
         if isinstance(port, ClockType):
             #print('defn clock', port)
             defnclk = port
    if defnclk:
        for name, port in inst.interface.ports.items():
             if isinstance(port, ClockType) and port.isinput() and not port.driven():
                 #print('inst clock', port)
                 wire(defnclk, port)
