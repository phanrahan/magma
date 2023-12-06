import string
from typing import Iterable, Mapping, Tuple, Union

from ast_tools.stack import get_symbol_table

from magma.array import Array
from magma.circuit import Circuit
from magma.common import hash_expr
from magma.digital import Digital
from magma.generator import Generator
from magma.interface import IO
from magma.t import In, Kind, Type
from magma.view import PortView
from magma.wire_utils import wire_value_or_port_view, WiringError


ValueLike = Union[Type, PortView]
ValueLikeMap = Mapping[str, ValueLike]


class InlineVerilogError(RuntimeError):
    pass


def _make_inline_value(
        inline_value_map: Mapping[str, ValueLike], value: ValueLike
) -> str:
    if (
            (
                isinstance(value, Array)
                and not issubclass(value.T, Digital)
            )
            or isinstance(value, Tuple)
    ):
        key = ", ".join(
            _make_inline_value(inline_value_map, t)
            for t in reversed(value)
        )
        # NOTE(leonardt): previously we used a tick (') prefix, but this is only
        # needed in verilog for wire assignments. In the past, this was fine
        # because inline verilog modules used the ' prefix in the instance
        # statement which is the same as declaring and assigning a wire. Now, we
        # can inline values more generally, so we don't insert the ' and instead
        # the user can insert it one if it is inlining a value into a wire
        # assignment or instance port statement.
        return f"{{{key}}}"
    key = f"__magma_inline_value_{len(inline_value_map)}"
    inline_value_map[key] = value
    return f"{{{key}}}"


def _process_fstring_syntax(
        format_str: str,
        format_args: Mapping[str, ValueLike],
        inline_value_map: Mapping[str, ValueLike],
        symbol_table: Mapping) -> str:
    fieldnames = [
        fname
        for _, fname, _, _ in string.Formatter().parse(format_str)
        if fname
    ]
    for field in fieldnames:
        if field in format_args:
            continue
        try:
            value = eval(field, {}, symbol_table)
        except NameError:
            continue
        if isinstance(value, (Type, PortView)):
            # Magma values (more precisely value-like objects, i.e. values or
            # PortView objects) are interpolated into strings specially. We
            # handle that here by creating a wire instance to make sure the
            # values persist.
            value = _make_inline_value(inline_value_map, value)
            # Stage for subsequent format call for regular kwargs inside
            # _inline_verilog.
            value = value.replace("{", "{{").replace("}", "}}")
        format_str = format_str.replace(f"{{{field}}}", str(value))
    return format_str


def _process_expr(
        expr: str,
        format_args: ValueLikeMap,
) -> Tuple[str, ValueLikeMap]:
    symbol_table = get_symbol_table([inline_verilog], copy_locals=True)
    value_map = {}
    expr = _process_fstring_syntax(
        expr, format_args, value_map, symbol_table
    )
    format_args = format_args.copy()
    for key, arg in format_args.items():
        if isinstance(arg, (Type, PortView)):
            arg = _make_inline_value(value_map, arg)
        format_args[key] = arg
    expr = expr.format(**format_args)
    # Replace all __magma_inline_value_x with x. Note that the value_map is
    # assumed to be ordered, specifically, in the order of the arguments. We
    # need to iterate in reverse fashion to avoid clobbering later keys,
    # e.g. 's/__magma_inline_value_1/{1}/g' would convert
    # '__magma_inline_value_14' to '14'. It is sufficient to iterate in reverse
    # order.
    for i, key in reversed(list(enumerate(value_map.keys()))):
        expr = expr.replace(key, f"{{{str(i)}}}")
    return expr, value_map


def _get_arg_type(value: ValueLike) -> Kind:
    if isinstance(value, PortView):
        return value.T
    return type(value)


def _wire_ports(value_map: ValueLikeMap, inst: Circuit):
    for i, value in enumerate(value_map.values()):
        try:
            wire_value_or_port_view(getattr(inst, f"I{i}"), value)
        except WiringError:
            raise InlineVerilogError(
                f"Found reference to undriven input port: {repr(value)}"
            ) from None


class _InlineVerilog(Generator):
    def __init__(self, expr: str, arg_types: Iterable[Kind]):
        self.expr = expr
        self.io = IO(**{
            f"I{i}": In(T)
            for i, T in enumerate(arg_types)
        })
        self.primitive = True
        self.name = f"InlineVerilog_{hash_expr(expr)}"


InlineVerilog = _InlineVerilog


def inline_verilog(expr, **kwargs):
    expr, value_map = _process_expr(expr, kwargs)
    inst = _InlineVerilog(expr, map(_get_arg_type, value_map.values()))()
    _wire_ports(value_map, inst)
