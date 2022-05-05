from magma.common import Stack


WHEN_COND_STACK = Stack()
_PREV_WHEN_COND = None


def reset_context():
    global WHEN_COND_STACK, _PREV_WHEN_COND
    WHEN_COND_STACK.clear()
    _PREV_WHEN_COND = None


class WhenCtx:
    def __init__(self, cond, base_cond=None, prev_conds=None,
                 is_otherwise=False):
        self._cond = cond
        self._assignments = []
        if base_cond is None:
            base_cond = cond
        self._base_cond = base_cond
        if prev_conds is None:
            prev_conds = []
        self._prev_conds = prev_conds

        global _PREV_WHEN_COND
        # Reset when to avoid a nested `elsewhen` or `otherwise` continuing a
        # chain
        _PREV_WHEN_COND = None

        self._is_otherwise = is_otherwise

    def __enter__(self):
        WHEN_COND_STACK.push(self)

    def __exit__(self, exc_type, exc_value, traceback):
        WHEN_COND_STACK.pop()
        if not self._is_otherwise:
            global _PREV_WHEN_COND
            _PREV_WHEN_COND = self
        else:
            assert _PREV_WHEN_COND is None

    @property
    def cond(self):
        return self._cond


when = WhenCtx


def _check_prev_when_cond(name):
    global _PREV_WHEN_COND
    if _PREV_WHEN_COND is None:
        raise SyntaxError(f"Cannot use {name} without a previous when")
    prev_cond = _PREV_WHEN_COND
    # Remove it so it can't be used in nesting
    _PREV_WHEN_COND = None
    return prev_cond


def _make_inv_cond_and_next_conds(prev_cond):
    inv_cond = ~prev_cond._base_cond
    for prev in prev_cond._prev_conds:
        inv_cond &= ~prev
    next_conds = prev_cond._prev_conds + [prev_cond._base_cond]
    return inv_cond, next_conds


def elsewhen(cond):
    prev_cond = _check_prev_when_cond('elsewhen')
    inv_cond, next_conds = _make_inv_cond_and_next_conds(prev_cond)
    return WhenCtx(inv_cond & cond, cond, next_conds)


def otherwise():
    prev_cond = _check_prev_when_cond('otherwise')
    inv_cond, next_conds = _make_inv_cond_and_next_conds(prev_cond)
    return WhenCtx(inv_cond, True, next_conds, is_otherwise=True)
