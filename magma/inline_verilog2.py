import hashlib

from magma.generator import Generator2
from magma.interface import IO
from magma.logging import root_logger


_logger = root_logger().getChild("inline_verilog2")


# TODO(rsetaluri): Make this re-usable from magma/inline_verilog_exrpession.py.
def _hash_expr(expr: str):
    hasher = hashlib.shake_128()
    hasher.update(expr.encode())
    return hasher.hexdigest(8)


def _clean_kwargs(kwargs):
    try:
        kwargs.pop("inline_wire_prefix")
        _logger.warning("bad")
    except KeyError:
        pass


class _InlineVerilog2(Generator2):
    def __init__(self, expr: str):
        import magma as m
        self.expr = expr
        self.io = IO()
        self.primitive = True
        self.name = f"InlineVerilog2_{_hash_expr(expr)}"


InlineVerilog2 = _InlineVerilog2


def inline_verilog2(expr, **kwargs):
    _clean_kwargs(kwargs)
    _InlineVerilog2(expr)()
