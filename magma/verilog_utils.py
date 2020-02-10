import magma as m
from magma.view import InstView, PortView


def value_to_verilog_name(value):
    if isinstance(value, m.Array) and not issubclass(value.T, m.Digital):
        elems = ", ".join(value_to_verilog_name(t) for t in value)
        return f"'{{{elems}}}"
    elif isinstance(value, m.Tuple):
        raise NotImplementedError("Inlining unflattened tuple")
    elif isinstance(value, PortView):
        parent_name = value_to_verilog_name(value.parent)
        return f"{parent_name}.{verilog_name(value.port.name)}"
    elif isinstance(value, InstView):
        prefix = ""
        if isinstance(value.parent, m.Circuit):
            prefix = value.parent.name + "."
        else:
            prefix = value_to_verilog_name(value.parent) + "."
        return prefix + value.inst.name
    return verilog_name(value.name)


def verilog_name(name):
    if isinstance(name, m.ref.DefnRef):
        return str(name)
    if isinstance(name, m.ref.InstRef):
        return f"{name.inst.name}.{str(name)}"
    if isinstance(name, m.ref.ArrayRef):
        array_name = verilog_name(name.array.name)
        return f"{array_name}_{name.index}"
    if isinstance(name, m.ref.TupleRef):
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
