import hashlib
import string
from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, get_symbol_table
from magma.circuit import _definition_context_stack, Circuit, IO
from magma.passes.passes import CircuitPass
from magma.passes.insert_coreir_wires import Wire
from magma.verilog_utils import convert_values_to_verilog_str
from magma.t import Type, Direction, In
from magma.view import PortView, InstView
from magma.digital import Digital
from magma.bit import Bit
from magma.array import Array
from magma.tuple import Tuple
from magma.wire import wire
from magma.backend.coreir_utils import sanitize_name
from magma.ref import DefnRef, InstRef, ArrayRef, TupleRef


def _get_top_level_ref(ref):
    if isinstance(ref, ArrayRef):
        return _get_top_level_ref(ref.array.name)
    if isinstance(ref, TupleRef):
        return _get_top_level_ref(ref.tuple.name)
    return ref


def get_view_inst_parent(view):
    while not isinstance(view, InstView):
        assert isinstance(view, PortView), type(view)
        return get_view_inst_parent(view.parent)
    return view


def _make_inline_value(cls, inline_value_map, value):
    if isinstance(value, Array) and not issubclass(value.T, Digital):
        return "'{" + ", ".join(_make_inline_value(cls, inline_value_map, t)
                                for t in reversed(value)) + "}"
    if isinstance(value, Tuple):
        raise NotImplementedError("Inlining tuple to verilog")
    value_key = f"__magma_inline_value_{len(inline_value_map)}"
    inline_value_map[value_key] = value
    return f"{{{value_key}}}"


def _inline_verilog(cls, inline_str, inline_value_map, **kwargs):
    format_args = {}
    for key, arg in kwargs.items():
        if isinstance(arg, (Type, PortView)):
            # Strip extra curly braces for format
            arg = _make_inline_value(cls, inline_value_map, arg)
        format_args[key] = arg
    inline_str = inline_str.format(**format_args)

    class _InlineVerilog(Circuit):
        # Unique name (hash) since uniquify doesn't check inline_verilog
        name = f"{cls.name}_{len(cls.inline_verilog_modules)}"

        for key, value in inline_value_map.items():
            name += f"_{sanitize_name(str(value))}"
        io = IO()
        connect_references = {}
        for key, value in inline_value_map.items():
            if isinstance(value, PortView):
                T = value.T
            else:
                T = type(value)
            io += IO(**{key: In(T)})

        # Need to mark unused so coreir knows there's a module definition
        for key in inline_value_map:
            port = getattr(io, key)
            port.unused()
            connect_references[key] = port

        # if there's not inlined values, make a dummy input/instance so there's
        # a def
        if not inline_value_map:
            io += IO(I=In(Bit))
            io.I.unused()

        inline_verilog_strs = [(inline_str, connect_references)]

    cls.inline_verilog_modules.append(_InlineVerilog)

    with cls.open():
        inst = _InlineVerilog()
        if not inline_value_map:
            inst.I @= 0

        for key, value in inline_value_map.items():
            if isinstance(value, Type):
                if value.is_input():
                    value = value.value()
                if not isinstance(_get_top_level_ref(value.name), DefnRef):
                    if not hasattr(value, "_magma_inline_wire_"):
                        # Insert a wire so it can't be inlined out
                        temp_name = f"_magma_inline_wire"
                        temp_name += f"{cls.inline_verilog_wire_counter}"
                        temp = type(value).qualify(Direction.Undirected)(
                            name=temp_name
                        )
                        cls.inline_verilog_wire_counter += 1
                        temp @= value
                        temp.unused()
                        value._magma_inline_wire_ = temp
                    value = value._magma_inline_wire_
            else:
                assert isinstance(value, PortView)
                if value.port.is_input():
                    raise NotImplementedError()
                if not hasattr(value, "_magma_inline_wire_"):
                    # get first instance parent, then the parent of that will
                    # be the container where we insert a wire
                    parent = get_view_inst_parent(value).parent
                    if isinstance(parent, InstView):
                        defn = parent.circuit
                    else:
                        assert isinstance(parent, Circuit)
                        defn = type(parent)

                    with defn.open():
                        temp_name = "_magma_inline_wire"
                        temp_name += f"{cls.inline_verilog_wire_counter}"
                        temp = Wire(type(value.port))(name=temp_name)
                        cls.inline_verilog_wire_counter += 1
                        temp.I @= value.port
                        temp = PortView(temp.O, parent)
                        value._magma_inline_wire_ = temp
                    value = value._magma_inline_wire_
            wire(value, getattr(inst, key))


def _process_inline_verilog(cls, format_str, format_args, symbol_table):

    if symbol_table is None:
        _inline_verilog(cls, format_str, **format_args)
        return

    fieldnames = [fname
                  for _, fname, _, _ in string.Formatter().parse(format_str)
                  if fname]
    inline_value_map = {}
    for field in fieldnames:
        if field in format_args:
            continue
        try:
            value = eval(field, {}, symbol_table)
        except NameError:
            continue
        if isinstance(value, (Type, PortView)):
            # These have special handling, don't convert to string.
            value = _make_inline_value(cls, inline_value_map, value)
            # Stage for subsequent format call for regular kwargs
            value = value.replace("{", "{{").replace("}", "}}")
        format_str = format_str.replace(f"{{{field}}}", str(value))
    _inline_verilog(cls, format_str, inline_value_map, **format_args)


class ProcessInlineVerilogPass(CircuitPass):
    def __call__(self, cls):
        if cls.inline_verilog_generated:
            return
        cls.inline_verilog_wire_counter = 0
        cls.inline_verilog_modules = []
        with cls.open():
            for fields in cls._context_._inline_verilog:
                _process_inline_verilog(cls, *fields)
        if getattr(cls, "instances", []):
            cls._is_definition = True
        cls.inline_verilog_generated = True


def inline_verilog(format_str, **kwargs):
    exec(_SKIP_FRAME_DEBUG_STMT)
    symbol_table = get_symbol_table([inline_verilog], copy_locals=True)

    context = _definition_context_stack.peek()
    context.add_inline_verilog(format_str, kwargs, symbol_table)
