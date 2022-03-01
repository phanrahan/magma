import abc
import collections
from typing import Optional


class ScopedNameGeneratorBase(abc.ABC):
    @abc.abstractmethod
    def __call__(self, name: Optional[str] = None, force: bool = False) -> str:
        raise NotImplementedError()


class ScopedNameGenerator(ScopedNameGeneratorBase):
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
            assert index == 0
            return name
        return name + str(index)
