from magma.common import hash_expr
from magma.generator import Generator2
from magma.interface import IO
from magma.t import Kind, In, Out
from magma.type_utils import type_to_sanitized_string


class _InlineVerilogExpression(Generator2):
    def __init__(self, expr: str, T: Kind):
        self.expr = expr
        self.io = IO(O=Out(T.undirected_t))
        self.primitive = True
        type_str = type_to_sanitized_string(T)
        self.name = f"InlineVerilogExpression_{type_str}_{hash_expr(expr)}"


InlineVerilogExpression = _InlineVerilogExpression
