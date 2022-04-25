import contextlib
import hashlib
import string
from typing import Mapping, Optional, Union

from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, get_symbol_table

from magma.array import Array
from magma.bit import Bit
from magma.circuit import Circuit
from magma.clock import ClockTypes
from magma.definition_context import DefinitionContext, get_definition_context
from magma.digital import Digital
from magma.interface import IO
from magma.passes.passes import CircuitPass
from magma.primitives.wire import Wire
from magma.ref import DefnRef, InstRef, ArrayRef, TupleRef
from magma.t import Type, Direction, In
from magma.tuple import Tuple
from magma.view import PortView, InstView
from magma.wire import wire


ValueLike = Union[Type, PortView]


class InlineVerilogError(RuntimeError):
    pass


def _get_view_inst_parent(view):
    while not isinstance(view, InstView):
        assert isinstance(view, PortView), type(view)
        return _get_view_inst_parent(view.parent)
    return view


def _make_inline_value(
        inline_value_map: Mapping[str, ValueLike], value: ValueLike) -> str:
    if isinstance(value, Array) and not issubclass(value.T, Digital):
        key = ", ".join(
            _make_inline_value(inline_value_map, t)
            for t in reversed(value)
        )
        return f"'{{{key}}}"
    if isinstance(value, Tuple):
        raise NotImplementedError(value)
    key = f"__magma_inline_value_{len(inline_value_map)}"
    inline_value_map[key] = value
    return f"{{{key}}}"


def _make_temporary(
        defn,
        value: Type,
        idx: int,
        inline_wire_prefix: str,
        parent: Optional[InstView] = None) -> ValueLike:

    def _insert_wire():
        temp_name = f"{inline_wire_prefix}{idx}"
        temp = Wire(type(value).undirected_t)(name=temp_name)
        temp.I @= value
        return temp

    # Insert a wire so that the value can't be inlined. If @defn is not None
    # then it needs to be `open()`'ed.
    ctx = contextlib.nullcontext() if defn is None else defn.open()
    with ctx:
        temp = _insert_wire()
    if parent is not None:
        return PortView(temp.O, parent)
    return temp.O


def _insert_temporary_wires(
        context: DefinitionContext,
        value: ValueLike,
        inline_wire_prefix: str):
    """
    Insert a temporary Wire instance so the signal isn't inlined out.

    We have to do this for DefnRef because the coreir inline.cpp logic
    sometimes inserts temporary wires for DefnRef that eventually get inlined.
    """
    wire_map = context.set_default_metadata("inline_verilog_wire_map", {})
    if isinstance(value, Type):
        if value.is_input():
            orig_value = value
            value = value.value()
            if value is None:
                raise InlineVerilogError(
                    f"Found reference to undriven input port: "
                    f"{repr(orig_value)}")

        key = value
        is_undriven_clock = (isinstance(value, ClockTypes) and value.is_input()
                             and not value.driven())
        if is_undriven_clock:
            # Share wire for undriven clocks so we don't
            # generate a separate wire for the eventual
            # driver from the automatic clock wiring logic
            key = type(value)
        if key not in wire_map:
            temp = _make_temporary(None, value,
                                   len(wire_map),
                                   inline_wire_prefix)
            wire_map[key] = temp
        value = wire_map[key]
    else:
        assert isinstance(value, PortView)
        if value.port.is_input():
            # For now we can't handle input port views, since this might return
            # a connection to the interface (e.g. self.I), then we'd need to
            # walk up to the parent instance and select the corresponding input
            # port, then trace that, which may need to happen recursively until
            # we find the driver in the current definition.
            # We don't have any existing use case for this, and a work around
            # exists which requires the user to effectively use the driver we
            # would find, rather than selecting the hierarchical input port
            # (this should work for simple cases, but might be annoying for
            # deep hierarchies where the driver could come from a far away
            # place, at which point we can add this feature)
            raise NotImplementedError()
        if value not in wire_map:
            # get first instance parent, then the parent of that will
            # be the container where we insert a wire
            parent = _get_view_inst_parent(value).parent
            if isinstance(parent, InstView):
                defn = parent.circuit
            else:
                assert isinstance(parent, Circuit)
                defn = type(parent)
            temp = _make_temporary(defn, value.port,
                                   len(wire_map),
                                   inline_wire_prefix, parent)
            wire_map[value] = temp
        value = wire_map[value]
    return value


def _build_io(inline_value_map: Mapping[str, ValueLike]) -> IO:
    if not inline_value_map:
        # Add dummy port so IO is not empty.
        io = IO(I=In(Bit))
        io.I.unused()
        return io
    io = IO()
    for key, value in inline_value_map.items():
        if isinstance(value, PortView):
            T = value.T
        else:
            T = type(value)
        io += IO(**{key: In(T)})
    return io


def _inline_verilog(
        context: DefinitionContext,
        format_str: str,
        format_args: Mapping[str, ValueLike],
        inline_value_map: Mapping[str, ValueLike],
        inline_wire_prefix: str):
    inline_verilog_modules = context.set_default_metadata(
        "inline_verilog_modules", [])
    format_args = format_args.copy()
    for key, arg in format_args.items():
        if isinstance(arg, (Type, PortView)):
            arg = _make_inline_value(inline_value_map, arg)
        format_args[key] = arg
    inline_str = format_str.format(**format_args)

    # Because modules/instances are sorted lexigraphically in the generated
    # verilog, in order for the inline verilog in the output to be in
    # statement-order, we need to generate a lexicographically increasing string
    # based on the order of the inline verilog statement in the python. A trick
    # to do this with numbers is, for every 10 modules, to insert a prefix 9 so
    # that it comes after the previous 1-9 digits.
    i = len(inline_verilog_modules)
    prefix = "9" * (i // 10)
    suffix = i % 10

    class _InlineVerilog(Circuit):
        name = f"{context.placer.name}_inline_verilog_{prefix}{suffix}"
        io = _build_io(inline_value_map)
        # Since each inline value (key) maps to a port, we populate the
        # connect_references dictionary with a map from key to port.
        connect_references = {}
        for key in inline_value_map:
            port = getattr(io, key)
            port.unused()  # these are needed so CoreIR knows it's a definition
            connect_references[key] = port
        inline_verilog_strs = [(inline_str, connect_references)]

    inline_verilog_modules.append(_InlineVerilog)
    inst_name = f"{context.placer.name}_inline_verilog_inst_{prefix}{suffix}"
    inst = _InlineVerilog(name=inst_name)
    # If there no interpolated values, _build_io adds a dummy port to avoid an
    # empty IO. We drive that with 0 here to avoid a hanging input.
    if not inline_value_map:
        inst.I @= 0

    for key, value in inline_value_map.items():
        value = _insert_temporary_wires(context, value, inline_wire_prefix)
        wire(value, getattr(inst, key))


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


def _process_inline_verilog(
        context: DefinitionContext,
        format_str: str,
        format_args: Mapping[str, ValueLike],
        symbol_table: Mapping,
        inline_wire_prefix: str):
    inline_value_map = {}
    if symbol_table is not None:
        format_str = _process_fstring_syntax(
            format_str, format_args, inline_value_map, symbol_table)
    _inline_verilog(
        context, format_str, format_args, inline_value_map, inline_wire_prefix)


def inline_verilog_impl(
        format_str: str,
        format_args: Mapping[str, ValueLike],
        symbol_table: Mapping,
        inline_wire_prefix: str):
    context = get_definition_context()
    _process_inline_verilog(
        context, format_str, format_args, symbol_table, inline_wire_prefix)


def inline_verilog(
        format_str: str,
        inline_wire_prefix: str = "_magma_inline_wire",
        **kwargs):
    exec(_SKIP_FRAME_DEBUG_STMT)
    format_args = kwargs
    symbol_table = get_symbol_table([inline_verilog], copy_locals=True)
    inline_verilog_impl(
        format_str, format_args, symbol_table, inline_wire_prefix)


class ProcessInlineVerilogPass(CircuitPass):
    def __call__(self, _):
        pass
