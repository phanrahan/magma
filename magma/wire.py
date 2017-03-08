from collections import Sequence
from .port import INPUT, OUTPUT, INOUT
from .compatibility import IntegerTypes
from .bit import BitType, LOW, HIGH
from .array import ArrayType
from .tuple import TupleType

__all__ = ['wire', 'wireclock', 'wiredefaultclock']


def wire(o, i):

    # replace output circuit with output arguments
    if hasattr(o, 'interface'):
        o = o.interface.outputs()

    # replace input circuit with input arguments
    if hasattr(i, 'interface'):
        i = i.interface.inputs()

    # if the input and output are both Sequences,
    #    then wire up the elements of the input and output Sequences
    # this occurs if 
    #    wire(Circuit, Circuit)
    #    wire(Circuit, Sequence)
    #    wire(Sequence, Circuit)
    if isinstance(i, Sequence) and isinstance(o, Sequence):
        assert len(i) == len(o)
        for j in range(len(o)):
            wire(o[j], i[j])
        return

    # we are wiring a Type to a Sequence
    if isinstance(i, Sequence):
        assert len(i) == 1
        i = i[0]

    # we are wiring a Sequence to a Type
    if isinstance(o, Sequence):
        assert len(o) == 1
        o = o[0]

    # promote integer types to LOW/HIGH
    if isinstance(o, IntegerTypes):
        o = HIGH if o else LOW
    if isinstance(i, IntegerTypes):
        i = HIGH if i else LOW

    # check directions ...
    #if isinstance(i, BitType) or isinstance(i, ArrayType) or isinstance(i, TupleType):
    #    idirection = i.direction
    #elif isinstance(i, IntegerTypes):
    #    idirection = OUTPUT
    #else:
    #    print('Illegal input')
    #    return

    #if isinstance(o, BitType) or isinstance(o, ArrayType) or isinstance(o, TupleType):
    #    odirection = o.direction
    #elif isinstance(o, IntegerTypes):
    #    odirection = OUTPUT
    #else:
    #    print('Illegal output')
    #    return

    #if odirection == INPUT and idirection == OUTPUT:
    #    i, o = o, i
        
    # Wire(Type, Type)
    i.wire(o)


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

def wiredefaultclock(cls, instance):
    #print('wiring clocks', str(cls), str(instance))

    if hasattr(instance, 'CLK') and not instance.CLK.driven():
        #print('wiring clock to CLK')
        if not hasattr(cls,'CLK'):
            print("Warning: %s does not have a CLK" % str(cls))
            return
        wire(cls.CLK, instance.CLK)
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

