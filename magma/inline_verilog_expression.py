import hashlib

from magma.generator import Generator2
from magma.interface import IO
from magma.t import Kind, In, Out
from magma.type_utils import type_to_sanitized_string


def _hash_expr(expr: str):
    hasher = hashlib.shake_128()
    hasher.update(expr.encode())
    return hasher.hexdigest(8)


class _InlineVerilogExpression(Generator2):
    def __init__(self, expr: str, T: Kind):
        self.expr = expr
        self.io = IO(O=Out(T.undirected_t))
        self.primitive = True
        type_str = type_to_sanitized_string(T)
        self.name = f"InlineVerilogExpression_{type_str}_{_hash_expr(expr)}"


InlineVerilogExpression = _InlineVerilogExpression
