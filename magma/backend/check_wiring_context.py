from magma.backend.coreir.coreir_utils import Slice
from magma.ref import PortViewRef
from magma.protocol_type import magma_value


def check_wiring_context(i, o):
    """
    Ensures that i and o come from the same definition context
    """
    if isinstance(o, Slice):
        o = o.value
    if isinstance(i, Slice):
        i = i.value
    i, o = magma_value(i), magma_value(o)
    if o.temp() or i.temp():
        # Will be handled recursively by the get_source logic
        return
    if o.const():
        return
    if isinstance(i.name, PortViewRef):
        i = i.name.root()
    if isinstance(o.name, PortViewRef):
        o = o.name.root()
    if (i.defn() is not None and
            o.defn() is not None and
            i.defn() is o.defn()):
        return
    if (i.inst() is not None and
            o.defn() is not None and
            i.inst().defn is o.defn()):
        return
    if (o.inst() is not None and
            i.defn() is not None and
            o.inst().defn is i.defn()):
        return
    if (o.inst() is not None and
            i.inst() is not None and
            o.inst().defn is i.inst().defn):
        return
    raise MagmaCompileException(
        f"Cannot wire {o.debug_name} to {i.debug_name} because they are"
        " not from the same definition context")
