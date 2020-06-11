from magma.array import Array
from magma.circuit import Circuit
from magma.digital import Digital
from magma.ref import (DefnRef, InstRef, NamedRef, ArrayRef, TupleRef,
                       PortViewRef)
from magma.t import Type, Direction
from magma.tuple import Tuple
from magma.view import InstView, PortView


def value_to_verilog_name(value):
    if isinstance(value, Array) and not issubclass(value.T, Digital):
        elems = ", ".join(value_to_verilog_name(t) for t in reversed(value))
        return f"'{{{elems}}}"
    elif isinstance(value, Tuple):
        raise NotImplementedError("Inlining unflattened tuple")
    elif isinstance(value, InstView):
        prefix = ""
        if value.parent is not None:
            prefix = value_to_verilog_name(value.parent) + "."
        return prefix + value.inst.name
    return verilog_name(value.name)


def verilog_name(name, inst_sep="_"):
    if isinstance(name, PortViewRef):
        curr = name.view.parent
        hierarchical_path = curr.inst.name + "."
        while isinstance(curr.parent, InstView):
            hierarchical_path = curr.parent.inst.name + "." + hierarchical_path
            curr = curr.parent
        return hierarchical_path + verilog_name(name.view.port.name)
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
        if name.root() is None:
            # Not a named temporary that will be flattened to a wire
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


def convert_values_to_verilog_str(cls, value):
    if isinstance(value, Type):
        if value.is_input():
            value = value.value()
        if not isinstance(_get_top_level_ref(value.name), DefnRef):
            if value not in cls.inline_verilog_wire_map:
                # Insert a wire so it can't be inlined out
                temp_name = f"_magma_inline_wire"
                temp_name += f"{cls.inline_verilog_wire_counter}"
                with cls.open():
                    temp = type(value).qualify(Direction.Undirected)(
                        name=temp_name
                    )
                    cls.inline_verilog_wire_counter += 1
                    temp @= value
                    temp.unused()
                    cls.inline_verilog_wire_map[value] = temp
            value = cls.inline_verilog_wire_map[value]
        return value_to_verilog_name(value)
    if isinstance(value, PortView):
        if value.port.is_input():
            raise NotImplementedError()
        if value not in cls.inline_verilog_wire_map:
            ref = _get_top_level_ref(value.port.name)
            if isinstance(ref, InstRef):
                defn = ref.inst.defn
            else:
                assert isinstance(ref, DefnRef)
                defn = ref.defn
            with defn.open():
                temp = type(value.port).qualify(Direction.Undirected)(
                    name=f"_magma_inline_wire{cls.inline_verilog_wire_counter}"
                )
                cls.inline_verilog_wire_counter += 1
                temp @= value.port
                temp.unused()
                temp = PortView(temp, value.parent)
                cls.inline_verilog_wire_map[value] = temp
            value = cls.inline_verilog_wire_map[value]
        return value_to_verilog_name(value)
    return str(value)
