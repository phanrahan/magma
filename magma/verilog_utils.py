from magma.array import Array
from magma.circuit import Circuit
from magma.digital import Digital
from magma.ref import (DefnRef, InstRef, NamedRef, ArrayRef, TupleRef,
                       PortViewRef, TempNamedRef)
from magma.t import Type, Direction
from magma.tuple import Tuple
from magma.view import InstView, PortView


def is_nd_array(T, skip=True):
    if issubclass(T, Digital) and not skip:
        return True
    if issubclass(T, Array):
        return is_nd_array(T.T, False)
    return False


def _should_recurse(value, disable_ndarray):
    if isinstance(value, PortView):
        value = value.port
    return (isinstance(value, Array) and not issubclass(value.T, Digital) and
            is_nd_array(type(value)) and disable_ndarray)


def value_to_verilog_name(value, disable_ndarray=False):
    if _should_recurse(value, disable_ndarray):
        elems = ", ".join(value_to_verilog_name(t, disable_ndarray)
                          for t in reversed(value))
        return f"'{{{elems}}}"
    elif isinstance(value, Tuple):
        raise NotImplementedError("Inlining unflattened tuple")
    elif isinstance(value, InstView):
        prefix = ""
        if value.parent is not None:
            prefix = value_to_verilog_name(value.parent, disable_ndarray) + "."
        return prefix + value.inst.name
    return verilog_name(value.name, disable_ndarray=disable_ndarray)


def verilog_name(name, inst_sep="_", disable_ndarray=False):
    if isinstance(name, PortViewRef):
        curr = name.view.parent
        hierarchical_path = curr.inst.name + "."
        while isinstance(curr.parent, InstView):
            hierarchical_path = curr.parent.inst.name + "." + hierarchical_path
            curr = curr.parent
        return hierarchical_path + verilog_name(
            name.view.port.name, disable_ndarray=disable_ndarray)
    if isinstance(name, DefnRef):
        return str(name)
    if isinstance(name, InstRef):
        return f"{name.inst.name}{inst_sep}{str(name)}"
    if isinstance(name, NamedRef):
        return str(name)
    if isinstance(name, ArrayRef):
        array_name = verilog_name(name.array.name,
                                  disable_ndarray=disable_ndarray)
        if (issubclass(name.array.T, Digital) or
                is_nd_array(type(name.array)) and not disable_ndarray):
            index = f"[{name.index}]"
        else:
            index = f"_{name.index}"
        return f"{array_name}{index}"
    if isinstance(name, TupleRef):
        tuple_name = verilog_name(name.tuple.name,
                                  disable_ndarray=disable_ndarray)
        index = name.index
        if not isinstance(name.root(), TempNamedRef):
            # Not a named temporary that will be flattened to a wire
            try:
                int(index)
                # python/coreir don't allow pure integer names
                index = f"_{index}"
            except ValueError:
                pass
        return f"{tuple_name}_{index}"
    raise NotImplementedError(name, type(name))
