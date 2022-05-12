import hashlib

from magma.generator import Generator2
from magma.interface import IO
from magma.t import Kind, In, Out


def _hash_expr(expr: str):
    hasher = hashlib.shake_128()
    hasher.update(expr.encode())
    return hasher.hexdigest(8)


class _InlineVerilogExpression(Generator2):
    def __init__(self, expr: str, T: Kind):
        self.expr = expr
        self.io = IO(O=Out(T.undirected_t))
        self.primitive = True
        self.name = f"InlineVerilogExpression_{_hash_expr(expr)}"


InlineVerilogExpression = _InlineVerilogExpression
