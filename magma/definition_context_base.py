import abc
from typing import Any

from magma.placer import PlacerBase


class DefinitionContextBase(abc.ABC):
    def __init__(self, placer: PlacerBase):
        self._placer = placer
        self._metadata = {}

    @property
    def placer(self) -> PlacerBase:
        return self._placer

    def get_metadata(self, key: str) -> Any:
        return self._metadata[key]

    def set_metadata(self, key: str, value: Any):
        self._metadata[key] = value

    def set_default_metadata(self, key: str, default: Any) -> Any:
        return self._metadata.setdeafult(key, default)

    @abc.abstractmethod
    def finalize(self):
        raise NotImplementedError()
