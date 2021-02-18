from magma.circuit import get_current_definition_context


class compile_guard:
    def __init__(self, guard_str: str):
        self.guard_str = guard_str

    def __enter__(self):
        print(get_current_definition_context())
        return self

    def __exit__(self, type, value, traceback):
        pass
