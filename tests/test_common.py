import contextlib

from magma.common import nest_context_managers


def test_nest_context_managers_basic():
    stack = []

    @contextlib.contextmanager
    def ctx_mgr(value):
        stack.append(value)
        try:
            yield
        finally:
            stack.pop(value)

    with nest_context_managers(ctx_mgr(0), ctx_mgr(1)):
        assert stack == [0, 1]
