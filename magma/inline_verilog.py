from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, get_symbol_table

from magma.circuit import _definition_context_stack
from magma.inline_verilog_impl import inline_verilog_impl
from magma.passes.passes import CircuitPass


class ProcessInlineVerilogPass(CircuitPass):
    def __call__(self, _):
        pass


def inline_verilog(
        format_str: str,
        inline_wire_prefix: str = "_magma_inline_wire",
        **kwargs):
    exec(_SKIP_FRAME_DEBUG_STMT)
    format_args = kwargs
    context = _definition_context_stack.peek()
    symbol_table = get_symbol_table([inline_verilog], copy_locals=True)
    inline_verilog_impl(
        context, format_str, format_args, symbol_table, inline_wire_prefix)
