import contextlib
import logging as py_logging
from typing import Any, List, Mapping
import weakref

from magma.common import Stack, Finalizable, FinalizableDelegator
from magma.logging import (
    stage_logger,
    unstage_logger,
    push_log_capturer,
    pop_log_capturer,
)
from magma.placer import PlacerBase


_VERILOG_FILE_OPEN = """
integer \\_file_{filename} ;
initial \\_file_{filename} = $fopen(\"{filename}\", \"{mode}\");
"""

_VERILOG_FILE_CLOSE = """
final $fclose(\\_file_{filename} );
"""

_DEFAULT_VERILOG_LOG_STR = """
`ifndef MAGMA_LOG_LEVEL
    `define MAGMA_LOG_LEVEL 1
`endif"""


def _inline_verilog(
        context: 'DefinitionContext',
        format_str: str,
        format_args: Mapping,
        symbol_table: Mapping,
        inline_wire_prefix: str = "_magma_inline_wire"):
    # NOTE(rsetaluri): These are hacks to avoid a circular dependency.
    from magma.inline_verilog import inline_verilog_impl
    with definition_context_manager(context):
        inline_verilog_impl(
            format_str, format_args, symbol_table, inline_wire_prefix)


class VerilogDisplayManager(Finalizable):
    def __init__(self, context: weakref.ReferenceType):
        self._context = context
        self._files = []
        self._displays = []
        self._insert_default_log_level = False

    @property
    def context(self) -> 'DefinitionContext':
        return self._context()

    def add_file(self, file):
        self._files.append(file)

    def insert_default_log_level(self):
        self._insert_default_log_level = True

    def add_display(self, display):
        self._displays.append(display)

    def finalize(self):
        if self._insert_default_log_level:
            _inline_verilog(self.context, _DEFAULT_VERILOG_LOG_STR, {}, {})
        # Finalization needs to finalize (i) opens, (ii) displays, and (iii)
        # closes, in that order.
        for file in self._files:
            string = _VERILOG_FILE_OPEN.format(
                filename=file.filename, mode=file.mode)
            _inline_verilog(self.context, string, {}, {})
        for display in self._displays:
            _inline_verilog(self.context, *display.get_inline_verilog())
        for file in self._files:
            string = _VERILOG_FILE_CLOSE.format(filename=file.filename)
            _inline_verilog(self.context, string, {}, {})


_definition_context_stack = Stack()


def _get_definition_context_stack() -> Stack:
    global _definition_context_stack
    return _definition_context_stack


class DefinitionContext(FinalizableDelegator):
    def __init__(self, placer: PlacerBase):
        super().__init__()
        self._placer = placer
        self._builders = []
        self._logs = []
        self._metadata = {}
        self.add_child("display", VerilogDisplayManager(weakref.ref(self)))
        self._conditional_values = set()
        self._when_conds = []

    @property
    def placer(self) -> PlacerBase:
        return self._placer

    def add_builder(self, builder):
        self._builders.append(builder)

    @property
    def logs(self) -> List:
        return self._logs.copy()

    def add_log(self, log):
        self._logs.append(log)

    def add_logs(self, logs):
        self._logs.extend(logs)

    def get_metadata(self, key: str) -> Any:
        return self._metadata[key]

    def set_metadata(self, key: str, value: Any):
        self._metadata[key] = value

    def set_default_metadata(self, key: str, default: Any) -> Any:
        return self._metadata.setdefault(key, default)

    def place_instances(self, defn):
        self._placer = self._placer.finalize(defn)
        for builder in self._builders:
            inst = builder.finalize()
            self._placer.place(inst)

    def finalize(self, defn):
        if not self._when_conds:
            return super().finalize()
        # TODO(when): Avoid circular import
        import magma as m
        input_ports = {}
        input_drivers = {}
        input_reverse_map = {}
        for i, cond in enumerate(self._when_conds):
            if cond.cond is not None:
                input_ports[f"C{i}"] = m.In(type(cond.cond))
                input_drivers[f"C{i}"] = cond.cond
                input_reverse_map[cond.cond] = f"C{i}"
            for j, (_, output) in enumerate(cond.conditional_wires):
                input_ports[f"C{i}I{j}"] = m.In(type(output))
                input_drivers[f"C{i}I{j}"] = output
                input_reverse_map[output] = f"C{i}I{j}"

        output_ports = {}
        output_sinks = {}
        output_reverse_map = {}
        for i, value in enumerate(self._conditional_values):
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
            for i, value in enumerate(self._conditional_values):
                if None in value._conditional_drivers:
                    body.add_statement(Assign(
                        output_reverse_map[value],
                        input_reverse_map[value._conditional_drivers[None]]
                    ))
            for cond in self._when_conds:
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
                for input, output in cond.conditional_wires:
                    if input not in output_reverse_map:
                        # Overridden
                        continue
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
        super().finalize()

    def add_conditional_value(self, value):
        self._conditional_values.add(value)

    def remove_conditional_value(self, value):
        self._conditional_values.remove(value)

    def add_when_cond(self, cond):
        self._when_conds.append(cond)


def push_definition_context(
        ctx: DefinitionContext, use_staged_logger: bool = False):
    push_log_capturer(ctx)
    if use_staged_logger:
        stage_logger()
    _get_definition_context_stack().push(ctx)


def pop_definition_context(
        use_staged_logger: bool = False) -> DefinitionContext:
    if use_staged_logger:
        unstage_logger()
    pop_log_capturer()
    return _get_definition_context_stack().pop()


def get_definition_context() -> DefinitionContext:
    return _get_definition_context_stack().peek()


@contextlib.contextmanager
def definition_context_manager(
        ctx: DefinitionContext, use_staged_logger: bool = False):
    push_definition_context(ctx, use_staged_logger)
    try:
        yield
    finally:
        if use_staged_logger:
            unstage_logger()
        popped_ctx = pop_definition_context(use_staged_logger)
        assert popped_ctx is ctx


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
