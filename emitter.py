class Emitter:
    def __init__(self):
        self._indent = 0

    def push(self):
        self._indent += 1

    def pop(self):
        self._indent -= 1

    def emit(self, line: str):
        tab = f"{'    '*self._indent}"
        print (f"{tab}{line}")
