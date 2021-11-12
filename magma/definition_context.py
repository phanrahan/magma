import logging as py_logging

from magma.definition_context_base import DefinitionContextBase
from magma.logging import root_logger, stage_logger, unstage_logger
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


class DefinitionContext(DefinitionContextBase):
    def __init__(self, placer: PlacerBase):
        super().__init__(placer)
        stage_logger()
        self._displays = []
        self._insert_default_log_level = False
        self._files = []
        self._builders = []
        self.metadata = {}

    def add_builder(self, builder):
        self._builders.append(builder)

    def add_file(self, file):
        self._files.append(file)

    def _finalize_file_opens(self):
        for file in self._files:
            string = _VERILOG_FILE_OPEN.format(
                filename=file.filename, mode=file.mode)
            self._inline_verilog(string, {}, {})

    def _finalize_file_close(self):
        for file in self._files:
            string = _VERILOG_FILE_CLOSE.format(filename=file.filename)
            self._inline_verilog(string, {}, {})

    def _inline_verilog(
            self,
            format_str,
            format_args,
            symbol_table,
            inline_wire_prefix="_magma_inline_wire"):
        # NOTE(rsetaluri): These are hacks to avoid a circular dependency.
        from magma.circuit import _DefinitionContextManager
        from magma.inline_verilog_impl import inline_verilog_impl
        with _DefinitionContextManager(self):
            inline_verilog_impl(
                self, format_str, format_args, symbol_table, inline_wire_prefix)

    def insert_default_log_level(self):
        self._insert_default_log_level = True

    def add_display(self, display):
        self._displays.append(display)

    def _finalize_displays(self):
        for display in self._displays:
            self._inline_verilog(*display.get_inline_verilog())

    def place_instances(self, defn):
        self._placer = self._placer.finalize(defn)
        for builder in self._builders:
            inst = builder.finalize()
            self.placer.place(inst)

    def finalize(self, defn):
        if self._insert_default_log_level:
            self._inline_verilog(_DEFAULT_VERILOG_LOG_STR, {}, {})
        self._finalize_file_opens()  # so displays can refer to open files
        self._finalize_displays()
        self._finalize_file_close()  # close after displays
        logs = unstage_logger()
        defn._has_errors_ = any(log[1] is py_logging.ERROR for log in logs)
