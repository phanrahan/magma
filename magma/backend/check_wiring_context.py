from magma.backend.coreir.coreir_utils import Slice
from magma.ref import PortViewRef, get_ref_inst, get_ref_defn, is_temp_ref
from magma.protocol_type import magma_value
from magma.compile_exception import MagmaCompileException
from magma.view import InstView


def _get_inst(value):
    if isinstance(value, InstView):
        return value.inst
    return get_ref_inst(value.name)


def _get_defn(value):
    if isinstance(value, InstView):
        return None
    return get_ref_defn(value.name)


def check_wiring_context(i, o):
    """
    Ensures that i and o come from the same definition context
    """
    orig_i, orig_o = i, o
    if isinstance(o, Slice):
        o = o.value
    if isinstance(i, Slice):
        i = i.value
    i, o = magma_value(i), magma_value(o)
    if is_temp_ref(o.name) or is_temp_ref(i.name):
        # Will be handled recursively by the get_source logic for the coreir
        # backend, i.e. when a connection is made, we only ever use the source
        # and sink (temporary values are for non-whole arrays that we then
        # recurse over)
        # NOTE: For other backends, we may need to adapt this logic
        return
    if o.const():
        return
    if isinstance(i.name, PortViewRef):
        i = i.name.root()
    if isinstance(o.name, PortViewRef):
        o = o.name.root()
    i_defn = _get_defn(i)
    o_defn = _get_defn(o)
    if i_defn is not None and o_defn is not None and i_defn is o_defn:
        return
    i_inst = _get_inst(i)
    o_inst = _get_inst(o)
    if i_inst is not None and o_defn is not None and i_inst.defn is o_defn:
        return
    if o_inst is not None and i_defn is not None and o_inst.defn is i_defn:
        return
    if (o_inst is not None and i_inst is not None and
            o_inst.defn is i_inst.defn):
        return
    raise MagmaCompileException(
        f"Cannot wire {orig_o.debug_name} to {orig_i.debug_name} because they "
        "are not from the same definition context")
