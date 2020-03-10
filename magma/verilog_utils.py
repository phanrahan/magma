from string import Formatter
import magma as m
from magma.view import InstView, PortView
from .t import Type


def value_to_verilog_name(value):
    if isinstance(value, m.Array) and not issubclass(value.T, m.Digital):
        elems = ", ".join(value_to_verilog_name(t) for t in reversed(value))
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


def verilog_name(name, inst_sep="."):
    if isinstance(name, m.ref.DefnRef):
        return str(name)
    if isinstance(name, m.ref.InstRef):
        return f"{name.inst.name}{inst_sep}{str(name)}"
    if isinstance(name, m.ref.NamedRef):
        return str(name)
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


def process_inline_verilog(cls, format_str, format_args, frame):
    fieldnames = [fname
                  for _, fname, _, _ in Formatter().parse(format_str)
                  if fname]
    for field in fieldnames:
        if field in format_args:
            continue
        curr_frame = frame
        while curr_frame:
            try:
                value = eval(field, curr_frame.f_globals, curr_frame.f_locals)
            except NameError:
                prev_frame = curr_frame
                curr_frame = curr_frame.f_back
                # On deleting frames, see:
                # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
                del prev_frame
                continue
            # These have special handling, don't convert to string.
            value = convert_values_to_verilog_str(value)
            value = value.replace("{", "{{").replace("}", "}}")
            format_str = format_str.replace(f"{{{field}}}", value)
            break

    del frame
    cls._inline_verilog(format_str, **format_args)
