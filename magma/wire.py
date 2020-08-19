from .compatibility import IntegerTypes
from .wire_container import Wire  # TODO(rsetaluri): only here for b.c.
from .debug import debug_wire
from .logging import root_logger
from .protocol_type import MagmaProtocol
from magma.wire_container import WiringLog


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
        outputs = o.interface.outputs()
        if len(outputs) != 1:
            _logger.error(
                WiringLog(f"Can only wire circuits with one output; circuit "
                          f"`{{}}` has outputs "
                          f"{[output.name.name for output in outputs]}", o),
                debug_info=debug_info
            )
            return
        o = outputs[0]

    # If o is an input.
    if not isinstance(o, IntegerTypes) and o.is_input():
        # If i is not an input.
        if isinstance(i, IntegerTypes) or not i.is_input():
            # Flip i and o.
            i, o = o, i

    # Wire(o, Type).
    i.wire(o, debug_info)
