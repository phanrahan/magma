import inspect
from collections import Sequence
from .port import INPUT, OUTPUT, INOUT
from .compatibility import IntegerTypes
from .t import Type
from .debug import debug_wire
from .logging import info, warning, error

__all__ = ['wire']


@debug_wire
def wire(o, i, debug_info):

    # Wire(o, Circuit)
    if hasattr(i, 'interface'):
        i.wire(o, debug_info)
        return

    # replace output Circuit with its output (should only be 1 output)
    if hasattr(o, 'interface'):
        # if wiring a Circuit to a Port
        # then circuit should have 1 output 
        o = o.interface.outputs()
        if len(o) != 1:
            error('Wiring Error: wiring {} (Sequence of length={}) to {} ({})'.format(o, len(o), i, type(i)))
            return
        o = o[0]

    # if o is an input
    if not isinstance(o, IntegerTypes) and o.isinput():
        # if i is not an input
        if isinstance(i, IntegerTypes) or not i.isinput():
            # flip i and o
            i, o = o, i

    #if hasattr(i, 'wire'):
    #    error('Wiring Error: The input must have a wire method -  {} to {}'.format(o, i))
    #    return

    # Wire(o, Type)
    i.wire(o, debug_info)

