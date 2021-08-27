import enum

from magma.passes.passes import CircuitPass, pass_lambda
from magma.compile_exception import MagmaCompileException


_HAS_ERROR_KEY = "_has_errors_"


def _has_errors(ckt):
    return getattr(ckt, _HAS_ERROR_KEY, False)


class FindErrorsPass(CircuitPass):

    class ErrorReportingMode(enum.Enum):
        FIRST = enum.auto()
        ALL = enum.auto()
        COLLECT = enum.auto()

    def __init__(self, main,
                 mode: ErrorReportingMode = ErrorReportingMode.FIRST):
        super().__init__(main)
        self._mode = mode
        self._errors = []

    def __call__(self, ckt):
        if not _has_errors(ckt):
            return
        self._handle_error(ckt)

    @property
    def errors(self):
        if self._mode == FindErrorsPass.ErrorReportingMode.FIRST:
            return None
        collect = (self._mode == FindErrorsPass.ErrorReportingMode.ALL or
                   self._mode == FindErrorsPass.ErrorReportingMode.COLLECT)
        if collect:
            return self._errors.copy()
        raise NotImplementedError(self._mode)

    def _handle_error(self, ckt):
        if self._mode == FindErrorsPass.ErrorReportingMode.FIRST:
            assert not self._errors
            raise MagmaCompileException(
                f"Found circuit with errors: {ckt.name}")
        collect = (self._mode == FindErrorsPass.ErrorReportingMode.ALL or
                   self._mode == FindErrorsPass.ErrorReportingMode.COLLECT)
        if collect:
            self._errors.append(ckt)
            return
        raise NotImplementedError(self._mdoe)

    def done(self):
        # If mode == ALL, then raise an error with all the circuit names. In the
        # case of COLLECT or FIRST, do nothing.
        if self._mode == FindErrorsPass.ErrorReportingMode.ALL:
            msg = (f"Found circuits with errors: "
                   f"{ckt.name for ckt in self._errors}")
            raise Exception(msg)


find_errors_pass = pass_lambda(FindErrorsPass)
