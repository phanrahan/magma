from abc import ABC, abstractmethod
from enum import Enum, auto
from ..bit import Bit
from ..bits import Bits
from ..circuit import DeclareCircuit, DefineCircuit
from ..digital import Digital
from ..logging import root_logger


_logger = root_logger()


class ImportMode(Enum):
    DECLARE = auto()
    DEFINE = auto()

    def func(self):
        if self is ImportMode.DECLARE:
            return DeclareCircuit
        return DefineCircuit


class VerilogImportError(Exception):
    pass


class MultiplePortDeclarationError(VerilogImportError):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        name = self.args[0]
        return f"Multiple declarations of port '{name}'"


class MultipleModuleDeclarationError(VerilogImportError):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        name = self.args[0]
        return f"Multiple definitions of module '{name}'"


class MixedPortDeclarationsError(VerilogImportError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Can not parse mixed declared and undeclared types"


class VerilogImporter(ABC):
    def __init__(self, type_map):
        self._type_map = type_map
        self._magma_modules = []

    def reset(self, type_map=None, external_modules=None):
        if type_map is not None:
            self._type_map = type_map
        self._magma_modules = []

    def map_type(self, name, magma_type):
        if name not in self._type_map:
            return magma_type
        target_type = self._type_map[name]
        if issubclass(magma_type, Digital) and \
           issubclass(target_type, Digital) and \
           magma_type.direction == target_type.direction:
            return target_type
        if issubclass(magma_type, Bits) and \
           issubclass(target_type, Bits) and \
           magma_type.N == target_type.N and \
           magma_type.T.direction == target_type.T.direction:
            return target_type
        raise NotImplementedError(f"Conversion between {magma_type} and "
                                  f"{target_type} not supported")

    def add_module(self, module):
        self._magma_modules.append(module)

    @abstractmethod
    def import_(self, src, mode):
        raise NotImplementedError()
