import collections
from typing import Optional


class MlirNameGenerator:
    def __init__(self):
        self._indices = collections.Counter()

    def __call__(self, name: Optional[str] = None, force: bool = False) -> str:
        if name is None:
            name = ""
        return self._call_impl(name, force)

    def _call_impl(self, name: str, force: bool) -> str:
        index = self._indices[name]
        self._indices[name] += 1
        if force:
            if index != 0:
                raise RuntimeError()
            return f"%{name}"
        return f"%{name}{index}"
