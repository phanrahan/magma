from magma.t import In, Out
from magma.interface import IO


def _build_port_maps(when_conds, conditional_values):
    """
    Return values
    * io_ports: map from port name to type used to build IO

    * port_wire_map: map from port name to value used to wire up instance

    * reverse_map: map from value to port name used to lookup port
                   name string for a value in the generated verilog
    """
    io_ports = {}
    port_wire_map = {}
    reverse_map = {}

    def add_port(port_name, value, dir):
        io_ports[port_name] = dir(type(value))
        port_wire_map[port_name] = value
        reverse_map[value] = port_name

    for i, cond in enumerate(when_conds):
        if cond.cond is not None:
            # Add an input for the condition
            add_port(f"C{i}", cond.cond, In)
        for j, output in enumerate(cond.conditional_wires.values()):
            # Add an input for the conditional drivers
            add_port(f"C{i}I{j}", output, In)

    for i, value in enumerate(conditional_values):
        # Add output for conditionally driven value
        add_port(f"O{i}", value, Out)
        if None in value._conditional_drivers:
            # Add input for default driver
            driver = value._conditional_drivers[None]
            add_port(f"O{i}None", driver, In)

    return (io_ports, port_wire_map, reverse_map)


def _get_conditional_values(context):
    conditional_values = set()
    for cond in context.when_conds:
        for key in cond.conditional_wires.keys():
            conditional_values.add(key)
    return conditional_values


def finalize_when_conds(context, when_conds):
    conditional_values = _get_conditional_values(context)

    io_ports, port_wire_map, reverse_map = _build_port_maps(when_conds,
                                                            conditional_values)

    # TODO: Circular import
    from magma.circuit import Circuit

    class ConditionalDrivers(Circuit):
        io = IO(**io_ports)

        when_cond_map = {}
        body = Body()
        for i, value in enumerate(conditional_values):
            if None in value._conditional_drivers:
                body.add_statement(Assign(
                    reverse_map[value],
                    reverse_map[value._conditional_drivers[None]]
                ))
        for cond in when_conds:
            if cond.cond is None:
                stmts = when_cond_map[cond.prev_cond].false_stmts
            elif cond.prev_cond is not None:
                stmt = IfStatement(reverse_map[cond.cond])
                when_cond_map[cond] = stmt
                when_cond_map[cond.prev_cond].false_stmts.append(stmt)
                stmts = stmt.true_stmts
            elif cond.parent is not None:
                stmt = IfStatement(reverse_map[cond.cond])
                when_cond_map[cond] = stmt
                when_cond_map[cond.parent].true_stmts.append(stmt)
                stmts = stmt.true_stmts
            else:
                stmt = IfStatement(reverse_map[cond.cond])
                body.add_statement(stmt)
                when_cond_map[cond] = stmt
                stmts = stmt.true_stmts
            for input, output in cond.conditional_wires.items():
                output_port = reverse_map[input]
                input_port = reverse_map[output]
                stmts.append(Assign(output_port, input_port))
        verilog = "always @(*) begin\n"
        verilog += body.codegen()
        verilog += "end"

    inst = ConditionalDrivers()
    for key, value in port_wire_map.items():
        if value.is_output():
            getattr(inst, key).wire(value)
        elif value.is_input():
            value.wire(getattr(inst, key))
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
