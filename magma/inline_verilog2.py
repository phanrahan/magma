from typing import Iterable, Mapping, Tuple

from ast_tools.stack import get_symbol_table

from magma.circuit import Circuit
from magma.generator import Generator2
from magma.interface import IO
from magma.t import In, Kind, Type
from magma.view import PortView
from magma.wire_utils import wire_value_or_port_view, WiringError
# TODO(rsetaluri): Make these common.
from magma.inline_verilog import (
    _process_fstring_syntax,
    _make_inline_value,
    ValueLike,
    InlineVerilogError,
)
from magma.inline_verilog_expression import _hash_expr


ValueLikeMap = Mapping[str, ValueLike]


def _process_expr(expr: str, format_args: ValueLikeMap) -> Tuple[str, ValueLikeMap]:
    symbol_table = get_symbol_table([inline_verilog2], copy_locals=True)
    value_map = {}
    expr = _process_fstring_syntax(
        expr, format_args, value_map, symbol_table
    )
    # TODO(rsetaluri): Reuse this from magma/inline_verilog.py.
    format_args = format_args.copy()
    for key, arg in format_args.items():
        if isinstance(arg, (Type, PortView)):
            arg = _make_inline_value(value_map, arg)
        format_args[key] = arg
    expr = expr.format(**format_args)
    # Replace all __magma_inline_value_x with x.
    for i, key in enumerate(value_map.keys()):
        expr = expr.replace(key, f"{{{str(i)}}}")
    return expr, value_map


def _wire_ports(value_map: ValueLikeMap, inst: Circuit):
    for i, value in enumerate(value_map.values()):
        try:
            wire_value_or_port_view(getattr(inst, f"I{i}"), value)
        except WiringError:
            raise InlineVerilogError(
                f"Found reference to undriven input port: {repr(value)}"
            ) from None


class _InlineVerilog2(Generator2):
    def __init__(self, expr: str, arg_types: Iterable[Kind]):
        import magma as m
        self.expr = expr
        self.io = IO(**{
            f"I{i}": In(T)
            for i, T in enumerate(arg_types)
        })
        self.primitive = True
        self.name = f"InlineVerilog2_{_hash_expr(expr)}"


InlineVerilog2 = _InlineVerilog2


def inline_verilog2(expr, **kwargs):
    expr, value_map = _process_expr(expr, kwargs)
    inst = _InlineVerilog2(expr, map(type, value_map.values()))()
    _wire_ports(value_map, inst)
