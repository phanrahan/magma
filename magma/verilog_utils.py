from magma.array import Array
from magma.circuit import Circuit
from magma.digital import Digital
from magma.ref import DefnRef, InstRef, NamedRef, ArrayRef, TupleRef
from magma.t import Type
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


def verilog_name(name, inst_sep="."):
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


def convert_values_to_verilog_str(value):
    if isinstance(value, Type):
        # TODO: For now we assumed values aren't used elswhere, this
        # forces it to be connected to an instance, so temporaries will
        # appear in the code
        if value.is_inout() and not value.driven():
            raise NotImplementedError()
        if value.is_input() and not value.driven():
            # TODO: Could be driven after, but that will just override
            # this wiring so it's okay for now
            value.undriven()
        elif value.is_output() and not value.wired():
            value.unused()
        elif not (value.is_input() or value.is_output() or value.is_inout()):
            value.unused()
        return value_to_verilog_name(value)
    if isinstance(value, PortView):
        return value_to_verilog_name(value)
    return str(value)
