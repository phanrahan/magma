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
        super().finalize()


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
