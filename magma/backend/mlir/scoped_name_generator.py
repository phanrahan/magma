import abc
import collections
from typing import Optional


class ScopedNameGeneratorBase(abc.ABC):
    @abc.abstractmethod
    def __call__(self, name: Optional[str] = None, force: bool = False) -> str:
        raise NotImplementedError()


class ScopedNameGenerator(ScopedNameGeneratorBase):
    def __init__(self, disallow_duplicates: bool):
        self._disallow_duplicates = disallow_duplicates
        self._indices = collections.Counter()

    def __call__(self, name: Optional[str] = None, force: bool = False) -> str:
        if name is None:
            name = ""
        return self._call_impl(name, force)

    def _call_impl(self, name: str, force: bool) -> str:
        index = self._indices[name]
        self._indices[name] += 1
        if force:
            if not self._disallow_duplicates:
                return name
            if index != 0:
                raise RuntimeError(f"Found duplicate name {name}")
        return name + str(index)
