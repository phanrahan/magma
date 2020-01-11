import magma as m
from magma.view import InstView, PortView


def verilog_name(name):
    if isinstance(name, PortView):
        return f"{verilog_name(name.parent)}.{verilog_name(name.port.name)}"
    if isinstance(name, InstView):
        prefix = ""
        if isinstance(name.parent, m.Circuit):
            prefix = name.parent.name + "."
        else:
            prefix = verilog_name(name.parent) + "."
        return prefix + name.inst.name
    elif isinstance(name, m.ref.DefnRef):
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
