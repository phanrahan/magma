import hashlib
import string
from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, get_symbol_table
from magma.circuit import _definition_context_stack, Circuit, IO
from magma.passes.passes import CircuitPass
from magma.passes.insert_coreir_wires import Wire
from magma.verilog_utils import convert_values_to_verilog_str
from magma.t import Type, Direction, In
from magma.view import PortView, InstView
from magma.digital import Digital
from magma.array import Array
from magma.tuple import Tuple
from magma.wire import wire
from magma.backend.coreir_utils import sanitize_name
from magma.ref import DefnRef, InstRef, ArrayRef, TupleRef

def _get_top_level_ref(ref):
    if isinstance(ref, ArrayRef):
        return _get_top_level_ref(ref.array.name)
    if isinstance(ref, TupleRef):
        return _get_top_level_ref(ref.tuple.name)
    return ref


def _make_inline_value(cls, inline_value_map, value):
    if isinstance(value, Array) and not issubclass(value.T, Digital):
        return "'{{" + ", ".join(_make_inline_value(cls, inline_value_map, t) for t
                                 in reversed(value)) + "}}"
    if isinstance(value, Tuple):
        raise NotImplementedError("Inlining tuple to verilog")
    value_key = f"__magma_inline_value_{len(inline_value_map)}"
    if not value.is_output():
        input_ = value
        if isinstance(value, PortView):
            input_ = value.port
        if input_.driven():
            # Use the driver rather than driving the output port because we
            # would override it
            driver = input_.trace()
            if isinstance(value, PortView):
                top_level_ref = _get_top_level_ref(driver.name)
                if isinstance(top_level_ref, DefnRef):
                    # Insert a wire and use that instead (otherwise we would have to
                    # select off the parent instance, and recursively walk back)
                    with top_level_ref.defn.open():
                        wire_inst = Wire(type(driver))()
                        wire_inst.I @= driver
                        driver = wire_inst.O

            if isinstance(value, PortView):
                value = PortView[type(driver)](driver, value.parent)
            else:
                value = driver
    inline_value_map[value_key] = value
    return f"{{{{{value_key}}}}}" 


def _inline_verilog(cls, inline_str, inline_value_map, **kwargs):
    format_args = {}
    for key, arg in kwargs.items():
        if isinstance(arg, (Type, PortView)):
            # Strip extra curly braces for format
            arg = _make_inline_value(cls, inline_value_map, arg)[1:-1]
        format_args[key] = arg

    inline_str = inline_str.format(**format_args)

    class _InlineVerilog(Circuit):
        # Unique name (hash) since uniquify doesn't check inline_verilog 
        name = f"InlineVerilog{hashlib.md5(inline_str.encode()).hexdigest()}"
        for key, value in inline_value_map.items():
            name += f"_{key}_{sanitize_name(str(value))}"
        io = IO()
        connect_references = {}
        for key, value in inline_value_map.items():
            if isinstance(value, PortView):
                T = value.T
            else:
                T = type(value)
            io += IO(**{key: T.flip()})

        for key in inline_value_map:
            port = getattr(io, key)
            # Force it to have a defn so coreir can select
            if port.is_input():
                port.undriven()
            else:
                port.unused()
            connect_references[key] = port

        inline_verilog_strs = [(inline_str, connect_references)]

    with cls.open():
        inst = _InlineVerilog()

        for key, value in inline_value_map.items():
            print(key, value, value.is_input(), value.driven())
            if value.is_input():
                wire(getattr(inst, key), value)
            else:
                wire(value, getattr(inst, key))


def _process_inline_verilog(cls, format_str, format_args, symbol_table):

    if symbol_table is None:
        _inline_verilog(cls, format_str, **format_args)
        return

    fieldnames = [fname
                  for _, fname, _, _ in string.Formatter().parse(format_str)
                  if fname]
    inline_value_map = {}
    for field in fieldnames:
        if field in format_args:
            continue
        try:
            value = eval(field, {}, symbol_table)
        except NameError:
            continue
        if isinstance(value, (Type, PortView)):
            # These have special handling, don't convert to string.
            value = _make_inline_value(cls, inline_value_map, value)
        format_str = format_str.replace(f"{{{field}}}", str(value))
    _inline_verilog(cls, format_str, inline_value_map, **format_args)


class ProcessInlineVerilogPass(CircuitPass):
    def __call__(self, cls):
        if cls.inline_verilog_generated:
            return
        with cls.open():
            for fields in cls._context_._inline_verilog:
                _process_inline_verilog(cls, *fields)
        if getattr(cls, "instances", []):
            cls._is_definition = True
        cls.inline_verilog_generated = True


def inline_verilog(format_str, **kwargs):
    exec(_SKIP_FRAME_DEBUG_STMT)
    symbol_table = get_symbol_table([inline_verilog], copy_locals=True)

    context = _definition_context_stack.peek()
    context.add_inline_verilog(format_str, kwargs, symbol_table)
