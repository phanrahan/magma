from .circuit import _definition_context_stack
from .verilog_utils import value_to_verilog_name
from .t import Type
from .view import PortView


def inline_verilog(format_str, **kwargs):
    context = _definition_context_stack.peek()
    context.add_inline_verilog(format_str, kwargs)
