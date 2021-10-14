import io
import sys


class PrinterBase:
    def __init__(self, tab: int = 4, sout: io.TextIOBase = sys.stdout):
        self._tab = tab
        self._indent = 0
        self._sout = sout
        self._flushed = True

    def push(self):
        self._indent += 1

    def pop(self):
        if self._indent == 0:
            raise RuntimeError("Can not match deindent")
        self._indent -= 1

    def _make_indent(self) -> str:
        return f"{' ' * (self._indent * self._tab)}"

    def flush(self):
        self._sout.write("\n")
        self._flushed = True

    def print(self, s: str):
        tab = self._make_indent() if self._flushed else ""
        self._sout.write(f"{tab}{s}")
        self._flushed = False

    def print_line(self, line: str):
        self._sout.write(f"{self._make_indent()}{line}\n")
        self._flusehd = True
