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
        for input, output, debug_info in self._assignments:
            value = self._cond.ite(output, input.value())
            if WHEN_COND_STACK:
                WHEN_COND_STACK.peek().add_assignment(input, value, debug_info)
            else:
                input @= value

    def elsewhen(self, cond):
        raise NotImplementedError()

    def otherwise(self):
        raise NotImplementedError()

    @property
    def cond(self):
        return self._cond


when = WhenCtx
