from magma.t import In, Out
from magma.interface import IO
from magma.ref import InstRef
from magma.bit import Bit
from magma.array import Array


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
        if dir is Out:
            # Assign to reg then wire up at end for verilog assign
            # semantics
            port_name += "_reg"
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


def _emit_default_drivers(conditional_values, body, reverse_map):
    """
    Emit default assignments (i.e. values driven before a when statement)
    """
    for i, value in enumerate(conditional_values):
        if None in value._conditional_drivers:
            body.add_statement(Assign(
                reverse_map[value],
                reverse_map[value._conditional_drivers[None]]
            ))
        elif (isinstance(value.name, InstRef) and
              value.name.inst._is_magma_memory_):
            # Default values for memory ports are 0 (e.g. for
            # conditional reads/writes)
            body.add_statement(Assign(reverse_map[value], "0"))



def _make_if(cond, when_cond_map):
    stmt = IfStatement(cond)
    when_cond_map[cond] = stmt
    when_cond_map[cond.prev_cond].false_stmts.append(stmt)
    return stmt


def finalize_when_conds(context, when_conds):
    conditional_values = _get_conditional_values(context)

    io_ports, port_wire_map, port_debug_map, reverse_map = \
        _build_port_maps(when_conds, conditional_values)

    # TODO: Circular import, but if we do this directly as an MLIR translation,
    # we could avoid having to create an instance here
    from magma.circuit import Circuit

    class ConditionalDriversImpl(Circuit):
        io = IO(**io_ports)

        when_cond_map = {}
        body = Body()
        _emit_default_drivers(conditional_values, body, reverse_map)
        for cond in when_conds:
            if cond.cond is None:
                # Else case, we append to previous false_stmts
                stmts = when_cond_map[cond.prev_cond].false_stmts
            else:
                stmt = IfStatement(reverse_map[cond.cond])
                when_cond_map[cond] = stmt
                stmts = stmt.true_stmts
                if cond.prev_cond is not None:
                    # elif, we append if statement inside previous false_stmts
                    when_cond_map[cond.prev_cond].false_stmts.append(stmt)
                elif cond.parent is not None:
                    # nested, we insert inside parents true_stmts
                    when_cond_map[cond.parent].true_stmts.append(stmt)
                else:
                    # we insert into top level
                    body.add_statement(stmt)
            for input, output in cond.conditional_wires.items():
                stmts.append(Assign(reverse_map[input], reverse_map[output]))
        verilog = ""
        # TODO(leonardt): We need to emit a reg declaration so we can assign in
        # a behavioral block, then wire up at the end.
        # For now, we only support Bit/Bits, since otherwise we need to have
        # CoreIR manage the verilog serialization.  Rather than "re-implement"
        # that here or add it to CoreIR, we should wait for MLIR
        for i, value in enumerate(conditional_values):
            width_str = ""
            if isinstance(value, Bit):
                pass
            elif (isinstance(value, Array) and
                  issubclass(value.T, Bit)):
                width_str = f"[{len(value) - 1}:0]"
            else:
                raise NotImplementedError(value)

            verilog += f"reg {width_str} O{i}_reg;\n"
        verilog += "always @(*) begin\n"
        verilog += body.codegen()
        verilog += "end\n"
        for i, value in enumerate(conditional_values):
            verilog += f"assign O{i} = O{i}_reg;\n"

    for value in conditional_values:
        # Clear to avoid warning in final wiring
        value.clear_conditional_drivers()

    inst = ConditionalDriversImpl()
    for key, value in port_wire_map.items():
        if value.is_output():
            getattr(inst, key).wire(value, port_debug_map[key])
        elif value.is_input():
            value.wire(getattr(inst, key), port_debug_map[key])
        else:
            raise NotImplementedError(type(value))


def _codegen_stmts(stmts, tab=""):
    s = ""
    for stmt in stmts:
        s += f"{tab}"
        s += f"\n{tab}".join(stmt.codegen().splitlines())
        s += "\n"
    return s


class Body:
    def __init__(self):
        self._statements = []

    def add_statement(self, stmt):
        self._statements.append(stmt)

    def codegen(self):
        return _codegen_stmts(self._statements, tab="    ")


class IfStatement:
    def __init__(self, cond):
        self._cond = cond
        self.true_stmts = []
        self.false_stmts = []

    def codegen(self):
        s = f"if ({self._cond}) begin\n"
        s += _codegen_stmts(self.true_stmts, tab="    ")
        if self.false_stmts:
            s += "end else begin\n"
            s += _codegen_stmts(self.false_stmts, tab="    ")
        s += "end"
        return s


class Assign:
    def __init__(self, input, output):
        self._input = input
        self._output = output

    def codegen(self):
        return f"{self._input} = {self._output};"