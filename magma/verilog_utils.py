from magma.array import Array
from magma.circuit import Circuit
from magma.digital import Digital
from magma.ref import DefnRef, InstRef, NamedRef, ArrayRef, TupleRef
from magma.t import Type, Direction
from magma.tuple import Tuple
from magma.view import InstView, PortView


def value_to_verilog_name(value):
    if isinstance(value, Array) and not issubclass(value.T, Digital):
        elems = ", ".join(value_to_verilog_name(t) for t in reversed(value))
        return f"'{{{elems}}}"
    elif isinstance(value, Tuple):
        raise NotImplementedError("Inlining unflattened tuple")
    elif isinstance(value, PortView):
        parent_name = value_to_verilog_name(value.parent)
        return f"{parent_name}.{verilog_name(value.port.name)}"
    elif isinstance(value, InstView):
        prefix = ""
        if isinstance(value.parent, Circuit):
            prefix = value.parent.name + "."
        else:
            prefix = value_to_verilog_name(value.parent) + "."
        return prefix + value.inst.name
    return verilog_name(value.name)


def verilog_name(name, inst_sep="_"):
    if isinstance(name, DefnRef):
        return str(name)
    if isinstance(name, InstRef):
        return f"{name.inst.name}{inst_sep}{str(name)}"
    if isinstance(name, NamedRef):
        return str(name)
    if isinstance(name, ArrayRef):
        array_name = verilog_name(name.array.name)
        if issubclass(name.array.T, Digital):
            index = f"[{name.index}]"
        else:
            index = f"_{name.index}"
        return f"{array_name}{index}"
    if isinstance(name, TupleRef):
        tuple_name = verilog_name(name.tuple.name)
        index = name.index
        try:
            int(index)
            # python/coreir don't allow pure integer names
            index = f"_{index}"
        except ValueError:
            pass
        return f"{tuple_name}_{index}"
    raise NotImplementedError(name, type(name))


def _get_top_level_ref(ref):
    if isinstance(ref, ArrayRef):
        return _get_top_level_ref(ref.array.name)
    if isinstance(ref, TupleRef):
        return _get_top_level_ref(ref.tuple.name)
    return ref


def _sanitize(name):
    return name.replace(".", "_").replace("[", "_").replace("]", "")


def convert_values_to_verilog_str(value):
    if isinstance(value, Type):
        if value.is_input() or value.is_inout():
            raise NotImplementedError()
        if not isinstance(_get_top_level_ref(value.name), DefnRef):
            if not hasattr(value, "_magma_inline_wire_"):
                # Insert a wire so it can't be inlined out
                temp = type(value).qualify(Direction.Undirected)(
                    name=_sanitize(str(value)) + "_magma_inline_wire"
                )
                temp @= value
                temp.unused()
                value._magma_inline_wire_ = temp
            value = value._magma_inline_wire_
        return value_to_verilog_name(value)
    if isinstance(value, PortView):
        if value.port.is_input() or value.port.is_inout():
            raise NotImplementedError()
        if not hasattr(value, "_magma_inline_wire_"):
            ref = _get_top_level_ref(value.port.name)
            if isinstance(ref, InstRef):
                defn = ref.inst.defn
            else:
                assert isinstance(ref, DefnRef)
                defn = ref.defn
            with defn.open():
                temp = type(value.port).qualify(Direction.Undirected)(
                    name=_sanitize(str(value.port)) + "_magma_inline_wire"
                )
                temp @= value.port
                temp.unused()
                temp = PortView(temp, value.parent)
                value._magma_inline_wire_ = temp
        value = value._magma_inline_wire_
        return value_to_verilog_name(value)
    return str(value)
