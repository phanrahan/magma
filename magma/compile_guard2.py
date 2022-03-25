import enum
from typing import List

from magma.common import Stack


_compile_guard2_stack = Stack()


def get_compile_guard2s() -> List['CompileGuard2']:
    global _compile_guard2_stack
    return _compile_guard2_stack.raw()


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

    @property
    def cond(self) -> str:
        return self._cond

    @property
    def cond_type(self) -> CondType:
        return self._cond_type

    def __enter__(self):
        global _compile_guard2_stack
        _compile_guard2_stack.push(self)

    def __exit__(self, typ, value, traceback):
        global _compile_guard2_stack
        head = _compile_guard2_stack.pop()
        assert head is self


compile_guard2 = CompileGuard2
