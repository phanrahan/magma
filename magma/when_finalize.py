from magma.t import In, Out
from magma.interface import IO
from magma.ref import InstRef
from magma.bit import Bit
from magma.array import Array
from magma.tuple import Product, Tuple


def _build_port_maps(when_conds, conditional_values):
    """
    Return values
    * io_ports: map from port name to type used to build IO

    * port_wire_map: map from port name to value used to wire up instance

    * port_debug_map: map from port name to debug info for original wiring

    * reverse_map: map from value to port name used to lookup port
                   name string for a value in the generated verilog
    """
    io_ports = {}
    port_wire_map = {}
    port_debug_map = {}
    reverse_map = {}

    def add_port(port_name, value, dir, debug_info):
        io_ports[port_name] = dir(type(value))
        port_wire_map[port_name] = value
        port_debug_map[port_name] = debug_info
        reverse_map[value] = port_name

    for i, cond in enumerate(when_conds):
        if cond.cond is not None:
            # Add an input for the condition
            add_port(f"C{i}", cond.cond, In, None)
        for j, (input, output) in enumerate(cond.conditional_wires.items()):
            # Add an input for the conditional drivers
            add_port(f"C{i}I{j}", output, In,
                     cond.get_debug_info(input, output))

    for i, value in enumerate(conditional_values):
        # Add output for conditionally driven value
        add_port(f"O{i}", value, Out, None)
        if None in value._conditional_drivers:
            # Add input for default driver
            driver = value._conditional_drivers[None]
            add_port(f"O{i}None", driver, In,
                     cond.get_debug_info(value, driver))

    return (io_ports, port_wire_map, port_debug_map, reverse_map)


def _get_conditional_values(context):
    conditional_values = set()
    for cond in context.when_conds:
        for key in cond.conditional_wires.keys():
            conditional_values.add(key)
    return list(sorted(conditional_values, key=lambda x: str(x.name)))


def finalize_when_conds(context, when_conds):
    # TODO: Circular import, but if we do this directly as an MLIR translation,
    # we could avoid having to create an instance here
    from magma.circuit import Circuit

    _when_conds = when_conds

    class ConditionalDriversImpl(Circuit):
        conditional_values = _get_conditional_values(context)
        when_conds = _when_conds

        io_ports, port_wire_map, port_debug_map, reverse_map = \
            _build_port_maps(when_conds, conditional_values)

        io = IO(**io_ports)

        _is_conditional_driver_ = True

        # NOTE(leonardt): port_wire_map, port_debug_map, reverse_map,
        # conditional_values, when_conds are used downstream by the compiler
        # to reconstruct the original when statement structure
        #
        # We collect this information now then drive the value with an instance
        # so it provides the invariant that all valid inputs are driven
        #
        # The backend will indentify these instances using
        # _is_conditional_driver_ and emit inline systme verilog code instead
        # of an instance

    for value in ConditionalDriversImpl.conditional_values:
        # Clear to avoid warning in final wiring
        value.clear_conditional_drivers()

    inst = ConditionalDriversImpl()
    for key, value in ConditionalDriversImpl.port_wire_map.items():
        inst_port = getattr(inst, key)
        debug_info = ConditionalDriversImpl.port_debug_map[key]
        if value.is_output():
            inst_port.wire(value, debug_info)
        elif value.is_input():
            value.wire(inst_port, debug_info)
        else:
            # TODO(when): inout we could use either wire?
            raise NotImplementedError(type(value))
