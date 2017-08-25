from .port import INPUT, OUTPUT, INOUT
from .t import In, Out, InOut
from .bit import Bit, _BitKind, _BitType
from .wire import wire

__all__  = ['Clock', 'ClockKind', 'ClockType']

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


def ClockInterface(has_ce, has_reset, has_set):
    args = ['CLK', In(Bit)]
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

_FFS  = ['FDRSE']
_FFS += ['SB_DFF',  'SB_DFFSS',  'SB_DFFSR', 'SB_DFFS', 'SB_DFFR']
_FFS += ['SB_DFFE', 'SB_DFFESS', 'SB_DFFESR', 'SB_DFFES', 'SB_DFFER']
_FFS += ['SB_DFFN',  'SB_DFFNSS',  'SB_DFFNSR', 'SB_DFFNS', 'SB_DFFNR']
_FFS += ['SB_DFFNE', 'SB_DFFNESS', 'SB_DFFNESR', 'SB_DFFNES', 'SB_DFFNER']

def wireclocktype(defn, inst, type):
    for name, port in defn.interface.ports.items():
         print(name, port)
         if isinstance(port, ClockType):
             print('Clock')
         if isinstance(port, ClockKind):
             print('Clock')
    for name, port in inst.interface.ports.items():
         print(name, port)
         if isinstance(port, ClockType):
             print('Clock')

def wiredefaultclock(cls, instance):
    #print('wiring clocks', str(cls), str(instance))

    if hasattr(instance, 'CLK') and not instance.CLK.driven():
        #print('wiring clock to CLK')
        if not hasattr(cls,'CLK'):
            print("Warning: %s does not have a CLK" % str(cls))
            return
        wire(cls.CLK, instance.CLK)
    if hasattr(instance, 'clk') and not instance.clk.driven():
        #print('wiring clock to clk')
        if not hasattr(cls,'CLK'):
            print("Warning: %s does not have a CLK" % str(cls))
            return
        wire(cls.CLK, instance.clk)
    if hasattr(instance, 'CLKA') and not instance.CLKA.driven():
        #print('wiring clock to CLKA')
        if not hasattr(cls,'CLK'):
            print("Warning: %s does not have a CLK" % str(cls))
            return
        wire(cls.CLK, instance.CLKA)
    if hasattr(instance, 'CLKB') and not instance.CLKB.driven():
        #print('wiring clock to CLKB')
        if not hasattr(cls,'CLK'):
            print("Warning: %s does not have a CLK" % str(cls))
            return
        wire(cls.CLK, instance.CLKB)
    if hasattr(instance, 'RCLK') and not instance.RCLK.driven():
        #print('wiring clock to RCLK')
        if not hasattr(cls,'CLK'):
            print("Warning: %s does not have a CLK" % str(cls))
            return
        wire(cls.CLK, instance.RCLK)
    if hasattr(instance, 'WCLK') and not instance.WCLK.driven():
        #print('wiring clock to WCLK')
        if not hasattr(cls,'CLK'):
            print("Warning: %s does not have a CLK" % str(cls))
            return
        wire(cls.CLK, instance.WCLK)
    if type(instance).__name__ in _FFS:
        if hasattr(instance,'C') and not instance.C.driven():
            if not hasattr(cls,'CLK'):
                print("Warning: %s does not have a CLK" % str(cls))
                return
            #print('wiring clock to FF')
            wire(cls.CLK, instance.C)

