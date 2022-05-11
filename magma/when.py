from magma.common import Stack


WHEN_COND_STACK = Stack()
_PREV_WHEN_COND = None


def reset_context():
    global WHEN_COND_STACK, _PREV_WHEN_COND
    WHEN_COND_STACK.clear()
    _PREV_WHEN_COND = None


class WhenCtx:
    def __init__(self, cond, prev_cond=None):
        self._cond = cond
        self._parent = WHEN_COND_STACK.safe_peek()
        self._prev_cond = prev_cond

        global _PREV_WHEN_COND
        # Reset when to avoid a nested `elsewhen` or `otherwise` continuing a
        # chain
        _PREV_WHEN_COND = None

        self._is_otherwise = cond is None
        self._conditional_wires = []

    def __enter__(self):
        WHEN_COND_STACK.push(self)
        # TODO(when): Circular import
        from magma.definition_context import get_definition_context
        get_definition_context().add_when_cond(self)

    def __exit__(self, exc_type, exc_value, traceback):
        WHEN_COND_STACK.pop()
        if not self._is_otherwise:
            global _PREV_WHEN_COND
            _PREV_WHEN_COND = self
        else:
            assert _PREV_WHEN_COND is None

    @property
    def parent(self):
        return self._parent

    @property
    def cond(self):
        return self._cond

    @property
    def prev_cond(self):
        return self._prev_cond

    @property
    def conditional_wires(self):
        return self._conditional_wires

    def add_conditional_wire(self, input, output):
        self._conditional_wires.append((input, output))


when = WhenCtx


def _check_prev_when_cond(name):
    global _PREV_WHEN_COND
    if _PREV_WHEN_COND is None:
        raise SyntaxError(f"Cannot use {name} without a previous when")
    prev_cond = _PREV_WHEN_COND
    # Remove it so it can't be used in nesting
    _PREV_WHEN_COND = None
    return prev_cond


def elsewhen(cond):
    return WhenCtx(cond, _check_prev_when_cond('elsewhen'))


def otherwise():
    return WhenCtx(None, _check_prev_when_cond('otherwise'))
