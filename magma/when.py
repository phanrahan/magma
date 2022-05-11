from magma.common import Stack


WHEN_COND_STACK = Stack()
_PREV_WHEN_COND = None


def reset_context():
    global WHEN_COND_STACK, _PREV_WHEN_COND
    WHEN_COND_STACK.clear()
    _PREV_WHEN_COND = None


class WhenCtx:
    def __init__(self, cond, prev_cond=None):
        self._cond = cond
        self._parent = WHEN_COND_STACK.safe_peek()
        if self._parent is not None:
            self.parent.add_child(self)
        self._prev_cond = prev_cond
        self._children = []

        global _PREV_WHEN_COND
        # Reset when to avoid a nested `elsewhen` or `otherwise` continuing a
        # chain
        _PREV_WHEN_COND = None

        self._is_otherwise = cond is None
        self._conditional_wires = {}

    def __enter__(self):
        WHEN_COND_STACK.push(self)
        # TODO(when): Circular import
        from magma.definition_context import get_definition_context
        get_definition_context().add_when_cond(self)

    def __exit__(self, exc_type, exc_value, traceback):
        WHEN_COND_STACK.pop()
        if not self._is_otherwise:
            global _PREV_WHEN_COND
            _PREV_WHEN_COND = self
        else:
            assert _PREV_WHEN_COND is None

    @property
    def parent(self):
        return self._parent

    @property
    def cond(self):
        return self._cond

    @property
    def prev_cond(self):
        return self._prev_cond

    @property
    def conditional_wires(self):
        return self._conditional_wires

    def add_conditional_wire(self, input, output):
        self._conditional_wires[input] = output

    def remove_conditional_wire(self, input):
        del self._conditional_wires[input]

    def has_conditional_wires(self):
        return (bool(self._conditional_wires) or
                any(child.has_conditional_wires() for child in self._children))

    def add_child(self, child):
        return self._children.append(child)


when = WhenCtx


def _check_prev_when_cond(name):
    global _PREV_WHEN_COND
    if _PREV_WHEN_COND is None:
        raise SyntaxError(f"Cannot use {name} without a previous when")
    prev_cond = _PREV_WHEN_COND
    # Remove it so it can't be used in nesting
    _PREV_WHEN_COND = None
    return prev_cond


def elsewhen(cond):
    return WhenCtx(cond, _check_prev_when_cond('elsewhen'))


def otherwise():
    return WhenCtx(None, _check_prev_when_cond('otherwise'))


def finalize_when_conds(context, when_conds):
    # TODO(when): Avoid circular import
    import magma as m
    input_ports = {}
    input_drivers = {}
    input_reverse_map = {}
    for i, cond in enumerate(when_conds):
        if cond.cond is not None:
            input_ports[f"C{i}"] = m.In(type(cond.cond))
            input_drivers[f"C{i}"] = cond.cond
            input_reverse_map[cond.cond] = f"C{i}"
        for j, output in enumerate(cond.conditional_wires.values()):
            input_ports[f"C{i}I{j}"] = m.In(type(output))
            input_drivers[f"C{i}I{j}"] = output
            input_reverse_map[output] = f"C{i}I{j}"

    output_ports = {}
    output_sinks = {}
    output_reverse_map = {}
    for i, value in enumerate(context._conditional_values):
        output_ports[f"O{i}"] = m.Out(type(value))
        output_sinks[f"O{i}"] = value
        output_reverse_map[value] = f"O{i}"
        if None in value._conditional_drivers:
            driver = value._conditional_drivers[None]
            input_ports[f"O{i}None"] = m.In(type(driver))
            input_drivers[f"O{i}None"] = driver
            input_reverse_map[driver] = f"O{i}None"

    class ConditionalDrivers(m.Circuit):
        io = m.IO(**input_ports) + m.IO(**output_ports)

        when_cond_map = {}
        body = Body()
        for i, value in enumerate(context._conditional_values):
            if None in value._conditional_drivers:
                body.add_statement(Assign(
                    output_reverse_map[value],
                    input_reverse_map[value._conditional_drivers[None]]
                ))
        for cond in when_conds:
            if cond.cond is None:
                stmts = when_cond_map[cond.prev_cond].false_stmts
            elif cond.prev_cond is not None:
                stmt = IfStatement(input_reverse_map[cond.cond])
                when_cond_map[cond] = stmt
                when_cond_map[cond.prev_cond].false_stmts.append(stmt)
                stmts = stmt.true_stmts
            elif cond.parent is not None:
                stmt = IfStatement(input_reverse_map[cond.cond])
                when_cond_map[cond] = stmt
                when_cond_map[cond.parent].true_stmts.append(stmt)
                stmts = stmt.true_stmts
            else:
                stmt = IfStatement(input_reverse_map[cond.cond])
                body.add_statement(stmt)
                when_cond_map[cond] = stmt
                stmts = stmt.true_stmts
            for input, output in cond.conditional_wires.items():
                output_port = output_reverse_map[input]
                input_port = input_reverse_map[output]
                stmts.append(Assign(output_port, input_port))
        verilog = "always @(*) begin\n"
        verilog += body.codegen()
        verilog += "end"

    inst = ConditionalDrivers()
    for key, value in input_drivers.items():
        getattr(inst, key).wire(value)
    for key, value in output_sinks.items():
        value.wire(getattr(inst, key))


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
