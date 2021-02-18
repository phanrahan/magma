from magma.circuit import get_current_definition_context


class compile_guard:
    def __init__(self, guard_str: str):
        self.guard_str = guard_str
        self.context = None

    def __enter__(self):
        self.context = get_current_definition_context()
        if self.context.placer.active_compile_guard is not None:
            raise NotImplementedError("Nested compile guards")
        self.context.placer.active_compile_guard = self
        return self

    def __exit__(self, type, value, traceback):
        self.context.placer.active_compile_guard = None
