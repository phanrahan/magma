import io
import sys


class Emitter:
    def __init__(self, sout: io.TextIOBase = sys.stdout):
        self._indent = 0
        self._sout = sout

    def push(self):
        self._indent += 1

    def pop(self):
        self._indent -= 1

    def emit(self, line: str):
        tab = f"{'    '*self._indent}"
        self._sout.write(f"{tab}{line}\n")
