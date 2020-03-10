from .circuit import _definition_context_stack
from .verilog_utils import value_to_verilog_name
from .t import Type
from .view import PortView
import inspect
from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, get_symbol_table


def inline_verilog(format_str, **kwargs):
    exec(_SKIP_FRAME_DEBUG_STMT)
    symbol_table = get_symbol_table()

    context = _definition_context_stack.peek()
    context.add_inline_verilog(format_str, kwargs, symbol_table)
