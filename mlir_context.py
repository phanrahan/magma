import collections
from typing import Optional

from mlir_type import MlirType
from mlir_value import MlirValue


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

    def anonymous_value(self, type: MlirType) -> MlirValue:
        return MlirValue(type)

    def named_value(
            self,
            type: MlirType,
            name: Optional[str] = None,
            force: bool = False) -> MlirValue:
        name = self._name_gen(name, force)
        return MlirValue(type, name=name)


class Contextual:
    def __init__(self, ctx: MlirContext):
        self._ctx = MlirContext

    @property
    def ctx(self) -> MlirContext:
        return self._ctx
