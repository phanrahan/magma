from hwtypes import BitVector, Bit

from .compatibility import IntegerTypes
from .wire_container import Wire  # TODO(rsetaluri): only here for b.c.
from .debug import debug_wire
from .logging import root_logger
from .protocol_type import magma_value

from magma.wire_container import WiringLog


_logger = root_logger()


_CONSTANTS = (IntegerTypes, BitVector, Bit)


@debug_wire
def wire(o, i, debug_info=None):
    o = magma_value(o)
    i = magma_value(i)

    # Circular import
    from .conversions import tuple_
    if isinstance(o, tuple):
        o = tuple_(o)
    if isinstance(i, tuple):
        i = tuple_(i)

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
    if not isinstance(o, _CONSTANTS) and o.is_input():
        # If i is not an input.
        if isinstance(i, _CONSTANTS) or not i.is_input():
            # Flip i and o.
            i, o = o, i

    i_T, o_T = type(i), type(o)
    if not i_T.is_wireable(o_T):
        _logger.error(
            WiringLog(f"Cannot wire {{}} ({o_T}) to {{}} ({i_T})",
                      o, i),
            debug_info=debug_info
        )
        return

    # Wire(o, Type).
    i.wire(o, debug_info)
