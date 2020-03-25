from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, get_symbol_table
from magma.circuit import _definition_context_stack


def inline_verilog(format_str, **kwargs):
    exec(_SKIP_FRAME_DEBUG_STMT)
    symbol_table = get_symbol_table([inline_verilog])

    context = _definition_context_stack.peek()
    context.add_inline_verilog(format_str, kwargs, symbol_table)
