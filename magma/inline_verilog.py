import string
from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, get_symbol_table
from magma.circuit import _definition_context_stack
from magma.passes.passes import CircuitPass
from magma.verilog_utils import convert_values_to_verilog_str


def _inline_verilog(cls, inline_str, **kwargs):
    format_args = {}
    for key, arg in kwargs.items():
        format_args[key] = convert_values_to_verilog_str(arg)
    cls.inline_verilog_strs.append(inline_str.format(**format_args))


def _process_inline_verilog(cls, format_str, format_args, symbol_table):

    if symbol_table is None:
        _inline_verilog(cls, format_str, **format_args)
        return

    fieldnames = [fname
                  for _, fname, _, _ in string.Formatter().parse(format_str)
                  if fname]
    for field in fieldnames:
        if field in format_args:
            continue
        try:
            value = eval(field, {}, symbol_table)
        except NameError:
            continue
        # These have special handling, don't convert to string.
        value = convert_values_to_verilog_str(value)
        value = value.replace("{", "{{").replace("}", "}}")
        format_str = format_str.replace(f"{{{field}}}", value)
    _inline_verilog(cls, format_str, **format_args)


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
