from .compatibility import IntegerTypes
from .debug import debug_wire
from .port import report_wiring_error


__all__ = ['wire']


@debug_wire
def wire(o, i, debug_info=None):
    # Wire(o, Circuit).
    if hasattr(i, 'interface'):
        i.wire(o, debug_info)
        return

    # Replace output Circuit with its output (should only be 1 output).
    if hasattr(o, 'interface'):
        # If wiring a Circuit to a Port then circuit should have 1 output.
        o_orig = o
        o = o.interface.outputs()
        if len(o) != 1:
            report_wiring_error(f"Can only wire circuits with one output. "
                                f"Argument 0 to wire `{o_orig.debug_name}` has "
                                f"outputs {o}", debug_info)
            return
        o = o[0]

    # If o is an input.
    if not isinstance(o, IntegerTypes) and o.isinput():
        # If i is not an input.
        if isinstance(i, IntegerTypes) or not i.isinput():
            # Flip i and o.
            i, o = o, i

    # Wire(o, Type).
    i.wire(o, debug_info)
