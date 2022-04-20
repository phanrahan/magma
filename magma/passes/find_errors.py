import enum
import logging as py_logging

from magma.passes.passes import DefinitionPass, pass_lambda
from magma.compile_exception import MagmaCompileException


def _has_errors(ckt):
    levels = (level for level, _, _, _ in ckt.logs)
    return any(level >= py_logging.ERROR for level in levels)


class FindErrorsPass(DefinitionPass):

    class ErrorReportingMode(enum.Enum):
        FIRST = enum.auto()
        ALL = enum.auto()
        COLLECT = enum.auto()

    def __init__(
            self, main,
            mode: ErrorReportingMode = ErrorReportingMode.FIRST
    ):
        super().__init__(main)
        self._mode = mode
        self._ckts_with_errors = []

    def __call__(self, ckt):
        # This is an optimization so that we don't check for errors if we only
        # care to find the first circuit with errors, and we've already found
        # one such circuit.
        skip_check = (
            self._mode == FindErrorsPass.ErrorReportingMode.FIRST and
            self._ckts_with_errors
        )
        if skip_check or not _has_errors(ckt):
            return
        self._ckts_with_errors.append(ckt)

    def done(self):
        if not self._ckts_with_errors:
            return
        if self._mode == FindErrorsPass.ErrorReportingMode.FIRST:
            ckt = self._ckts_with_errors[0]
            raise MagmaCompileException(
                f"Found circuit with errors: {ckt.name}"
            )
        if self._mode == FindErrorsPass.ErrorReportingMode.ALL:
            msg = (
                f"Found circuits with errors: "
                f"{ckt.name for ckt in self._ckts_with_errors}"
            )
            raise MagmaCompileException(msg)


find_errors_pass = pass_lambda(FindErrorsPass)
