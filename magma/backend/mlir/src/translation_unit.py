from typing import Any
import weakref

import magma as m

from builtin import builtin
from hardware_module import HardwareModule
from mlir import MlirSymbol, push_block
from scoped_name_generator import ScopedNameGenerator


class TranslationUnit:
    def __init__(self, magma_top: m.DefineCircuitKind):
        self._magma_top = magma_top
        self._mlir_module = builtin.ModuleOp()
        self._hardware_modules = {}
        self._symbol_map = {}
        self._symbol_name_generator = ScopedNameGenerator()

    @property
    def magma_top(self) -> m.DefineCircuitKind:
        return self._magma_top

    @property
    def mlir_module(self) -> builtin.ModuleOp:
        return self._mlir_module

    def new_hardware_module(
            self, magma_defn_or_decl: m.circuit.CircuitKind) -> HardwareModule:
        return HardwareModule(magma_defn_or_decl, weakref.ref(self))

    def get_hardware_module(
            self, magma_defn_or_decl: m.circuit.CircuitKind) -> HardwareModule:
        key = self._make_key(magma_defn_or_decl)
        return self._hardware_modules[key]

    def set_hardware_module(
            self, magma_defn_or_decl: m.circuit.CircuitKind,
            hardware_module: HardwareModule):
        key = self._make_key(magma_defn_or_decl)
        if key in self._hardware_modules:
            raise ValueError(f"Hardware module '{key}' already exists")
        self._hardware_modules[key] = hardware_module

    def has_hardware_module(
            self, magma_defn_or_decl: m.circuit.CircuitKind) -> bool:
        key = self._make_key(magma_defn_or_decl)
        return key in self._hardware_modules

    def get_mapped_symbol(self, obj: m.Type) -> MlirSymbol:
        return self._symbol_map[obj]

    def get_or_make_mapped_symbol(self, obj: Any, **kwargs) -> MlirSymbol:
        try:
            return self._symbol_map[obj]
        except KeyError:
            pass
        self._symbol_map[obj] = symbol = self.new_symbol(**kwargs)
        return symbol

    def set_mapped_symbol(self, obj: Any, symbol: MlirSymbol):
        if obj in self._symbol_map:
            raise ValueError(f"{obj} already mapped")
        self._symbol_map[obj] = symbol

    def new_symbol(self, **kwargs) -> MlirSymbol:
        name = self._symbol_name_generator(**kwargs)
        return MlirSymbol(name)

    def compile(self):
        deps = m.passes.dependencies(self._magma_top, include_self=True)
        with push_block(self._mlir_module):
            for dep in deps:
                if self.has_hardware_module(dep):
                    continue
                hardware_module = self.new_hardware_module(dep)
                hardware_module.compile()
                if hardware_module.hw_module:
                    self.set_hardware_module(dep, hardware_module)

    @staticmethod
    def _make_key(magma_defn_or_decl: m.circuit.CircuitKind) -> str:
        return magma_defn_or_decl.name
