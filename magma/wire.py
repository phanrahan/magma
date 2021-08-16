from hwtypes import BitVector, Bit

from .compatibility import IntegerTypes
from .wire_container import Wire  # TODO(rsetaluri): only here for b.c.
from .debug import debug_wire
from .logging import root_logger
from .protocol_type import magma_value

from magma.definition_context_stack import DEFINITION_CONTEXT_STACK
from magma.ref import LazyCircuit, PortViewRef
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

    if isinstance(i, _CONSTANTS) or isinstance(o, _CONSTANTS):
        pass
    elif (isinstance(i.name, PortViewRef) or
          isinstance(o.name, PortViewRef)):
        pass
    elif i.temp() or o.temp():
        pass
    elif (i.defn() is not None and
          o.defn() is not None):
        if i.defn() is not o.defn():
            _logger.error(
                WiringLog(f"Cannot wire {o} to {i} because they are not from"
                          f" the same definition:"
                          f"\n    {o} is from {o.defn()},"
                          f"\n    {i} is from {i.defn()}"),
                debug_info=debug_info
            )
            return
    # TODO: How to handle circuit builders?
    elif (i.inst() is not None and
          i.inst() is LazyCircuit):
        pass
    # TODO: How to handle circuit builders?
    elif (o.inst() is not None and
          o.inst() is LazyCircuit):
        pass
    elif (i.inst() is not None and
          o.defn() is not None and
          i.inst().defn is o.defn() and
          (o.defn() is LazyCircuit or
           o.defn() is DEFINITION_CONTEXT_STACK.peek().placer._defn)):
        pass
    elif (o.inst() is not None and
          i.defn() is not None and
          o.inst().defn is i.defn() and
          (i.defn() is LazyCircuit or
           i.defn() is DEFINITION_CONTEXT_STACK.peek().placer._defn)):
        pass
    elif (o.inst() is not None and
          i.inst() is not None and
          o.inst().defn is i.inst().defn and
          (i.inst().defn is LazyCircuit or
           i.inst().defn is DEFINITION_CONTEXT_STACK.peek().placer._defn)):
        pass
    else:
        raise Exception(f"Cannot wire together {o} and {i}")

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
