from .compatibility import IntegerTypes
from .wire_container import Wire  # TODO(rsetaluri): only here for b.c.
from .debug import debug_wire
from .logging import root_logger
from .protocol_type import MagmaProtocol


_logger = root_logger()


@debug_wire
def wire(o, i, debug_info=None):
    if isinstance(o, MagmaProtocol):
        o = o._get_magma_value_()
    if isinstance(i, MagmaProtocol):
        i = i._get_magma_value_()

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
            _logger.error(f"Can only wire circuits with one output. Argument "
                          f"0 to wire `{o_orig.debug_name}` has outputs {o}",
                          debug_info=debug_info)
            return
        o = o[0]

    # If o is an input.
    if not isinstance(o, IntegerTypes) and o.is_input():
        # If i is not an input.
        if isinstance(i, IntegerTypes) or not i.is_input():
            # Flip i and o.
            i, o = o, i

    # Wire(o, Type).
    i.wire(o, debug_info)
