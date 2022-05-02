from magma.common import Stack


WHEN_COND_STACK = Stack()


class WhenCtx:
    def __init__(self, cond, base_cond=None, prev_conds=None):
        self._cond = cond
        self._assignments = []
        if base_cond is None:
            base_cond = cond
        self._base_cond = base_cond
        if prev_conds is None:
            prev_conds = []
        self._prev_conds = prev_conds

    def __enter__(self):
        WHEN_COND_STACK.push(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        WHEN_COND_STACK.pop()

    def elsewhen(self, cond):
        inv_cond = ~self._base_cond
        for prev in self._prev_conds:
            inv_cond &= ~prev
        return WhenCtx(inv_cond & cond, cond, self._prev_conds +
                       [self._base_cond])

    def otherwise(self):
        inv_cond = ~self._base_cond
        for prev in self._prev_conds:
            inv_cond &= ~prev
        # TODO(when): Enforce this context isn't used again
        return WhenCtx(inv_cond, True, self._prev_conds + [self._base_cond])

    @property
    def cond(self):
        return self._cond


when = WhenCtx
