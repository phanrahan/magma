import collections
import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class MlirValue:
    name: str


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


class MlirContext:
    def __init__(self):
        self._name_gen = MlirNameGenerator()

    def new_value(
            self,
            name: Optional[str] = None,
            force: bool = False) -> MlirValue:
        name = self._name_gen(name, force)
        return MlirValue(name)
