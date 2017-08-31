import inspect
from collections import Sequence
from .port import INPUT, OUTPUT, INOUT
from .compatibility import IntegerTypes
from .bit import BitType, LOW, HIGH
from .array import ArrayType
from .tuple import TupleType
from .debug import debug_wire
from .error import error

__all__ = ['wire']


@debug_wire
def wire(o, i, debug_info):

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
        if len(i) != len(o):
            error('Wiring Error: wiring {} (len={}) to {} (len={})'.format(o, len(o), i, len(i)))
            return
        for j in range(len(o)):
            wire(o[j], i[j], debug_info)
        return

    # we are wiring a Type to a Sequence
    if isinstance(i, Sequence):
    #    if isinstance(o, ArrayType) and len(i) == len(o):
    #        for j in range(len(o)):
    #            wire(o[j], i[j], debug_info)
    #        return
        if len(i) != 1:
            error('Wiring Error: wiring {} ({}) to {} (Sequence of length={})'.format(o, type(o), i, len(i)))
            return
        i = i[0]

    # we are wiring a Sequence to a Type
    if isinstance(o, Sequence):
    #    if isinstance(i, ArrayType) and len(i) == len(o):
    #        for j in range(len(o)):
    #            wire(o[j], i[j], debug_info)
    #        return
        if len(o) != 1:
            error('Wiring Error: wiring {} (Sequence of length={}) to {} ({})'.format(o, len(o), i, type(i)))
            return
        o = o[0]

    # promote integer types to LOW/HIGH
    #if isinstance(o, IntegerTypes):
    #    o = HIGH if o else LOW

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
    i.wire(o, debug_info)

