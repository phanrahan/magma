from magma.common import Stack


WHEN_COND_STACK = Stack()


class WhenCtx:
    def __init__(self, cond):
        self._cond = cond
        self._assignments = []

    def __enter__(self):
        WHEN_COND_STACK.push(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        WHEN_COND_STACK.pop()

    def elsewhen(self, cond):
        raise NotImplementedError()

    def otherwise(self):
        raise NotImplementedError()

    @property
    def cond(self):
        return self._cond


when = WhenCtx
