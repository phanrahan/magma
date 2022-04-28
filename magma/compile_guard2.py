import enum
from typing import List

from magma.definition_context import get_definition_context


class CondType(enum.Enum):
    defined = enum.auto()
    undefined = enum.auto()


class CompileGuard2:
    def __init__(self, cond: str, cond_type: str = "defined"):
        """
        cond: ifdef condition, e.g.
            `ifdef <cond>

        cond_type:
            * "defined" -> ifdef
            * "undefined" -> ifndef
        """
        self._cond = cond
        self._cond_type = CondType[cond_type]
        self._ctx = None

    @property
    def cond(self) -> str:
        return self._cond

    @property
    def cond_type(self) -> CondType:
        return self._cond_type

    def __enter__(self):
        if self._ctx is not None:
            raise RuntimeError("Can not reuse compile_guard2")
        self._ctx = get_definition_context()
        self._ctx.compile_guard2_stack.push(self)

    def __exit__(self, typ, value, traceback):
        head = self._ctx.compile_guard2_stack.pop()
        assert head is self


compile_guard2 = CompileGuard2
