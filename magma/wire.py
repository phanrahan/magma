import inspect
from collections import Sequence
from .port import INPUT, OUTPUT, INOUT
from .compatibility import IntegerTypes
from .t import Type, Kind
from .debug import debug_wire
from .logging import info, warning, error
from .port import report_wiring_error
from .current_definition import get_current_definition
from .ref import InstRef, DefnRef, get_base_ref


__all__ = ['wire']


# Check that the wiring call is valid: if a port is an instance port, the
# instance should have been placed in the current definition; if a port is a
# definition port, the definition should be the current definition.
def _verify_ref(port):
    current_defn = get_current_definition()
    base_ref = get_base_ref(port.name)
    if isinstance(base_ref, InstRef):
        assert base_ref.inst.defn is current_defn
    elif isinstance(base_ref, DefnRef):
        assert base_ref.defn is current_defn


@debug_wire
def wire(o, i, debug_info):

    for port in (o, i):
        if not isinstance(type(port), Kind):
            continue
        _verify_ref(port)

    # Wire(o, Circuit)
    if hasattr(i, 'interface'):
        i.wire(o, debug_info)
        return

    # replace output Circuit with its output (should only be 1 output)
    if hasattr(o, 'interface'):
        # if wiring a Circuit to a Port
        # then circuit should have 1 output
        o_orig = o
        o = o.interface.outputs()
        if len(o) != 1:
            report_wiring_error(f'Can only wire circuits with one output. Argument 0 to wire `{o_orig.debug_name}` has outputs {o}', debug_info)  # noqa
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

