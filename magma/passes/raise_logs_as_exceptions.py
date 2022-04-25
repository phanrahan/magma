import enum
import logging as py_logging

from magma.passes.passes import DefinitionPass, pass_lambda
from magma.compile_exception import MagmaCompileException


def _has_log_above_threshold(ckt, threshold):
    levels = (level for level, _, _, _ in ckt.logs)
    return any(level >= threshold for level in levels)


class RaiseLogsAsExceptionsPass(DefinitionPass):

    class Mode(enum.Enum):
        FIRST = enum.auto()
        ALL = enum.auto()
        COLLECT = enum.auto()

    def __init__(
            self, main,
            mode: Mode = Mode.FIRST,
            threshold: int = py_logging.ERROR,
            exception_type: type = MagmaCompileException
    ):
        super().__init__(main)
        self._mode = mode
        self._threshold = threshold
        self._exception_type = exception_type
        self._ckts_with_errors = []

    def __call__(self, ckt):
        # This is an optimization so that we don't check for errors if we only
        # care to find the first circuit with errors, and we've already found
        # one such circuit.
        skip_check = (
            self._mode == RaiseLogsAsExceptionsPass.Mode.FIRST and
            self._ckts_with_errors
        )
        if skip_check or not _has_log_above_threshold(ckt, self._threshold):
            return
        self._ckts_with_errors.append(ckt)

    def done(self):
        if not self._ckts_with_errors:
            return
        if self._mode == RaiseLogsAsExceptionsPass.Mode.FIRST:
            ckt = self._ckts_with_errors[0]
            raise self._exception_type(
                f"Found circuit with errors: {ckt.name}"
            )
        if self._mode == RaiseLogsAsExceptionsPass.Mode.ALL:
            msg = (
                f"Found circuits with errors: "
                f"', '.join({ckt.name for ckt in self._ckts_with_errors})"
            )
            raise self._exception_type(msg)


raise_logs_as_exceptions_pass = pass_lambda(RaiseLogsAsExceptionsPass)
