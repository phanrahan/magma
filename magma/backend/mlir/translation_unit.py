from typing import Any, Dict
import weakref

from magma.backend.mlir.builtin import builtin
from magma.backend.mlir.compile_to_mlir_opts import CompileToMlirOpts
from magma.backend.mlir.hardware_module import HardwareModule
from magma.backend.mlir.mlir import MlirSymbol, push_block
from magma.backend.mlir.scoped_name_generator import ScopedNameGenerator
from magma.circuit import CircuitKind, DefineCircuitKind
from magma.passes import dependencies
from magma.t import Type


class TranslationUnit:
    def __init__(self, magma_top: DefineCircuitKind, opts: CompileToMlirOpts):
        self._magma_top = magma_top
        self._opts = opts
        self._mlir_module = builtin.ModuleOp()
        self._hardware_modules = {}
        self._symbol_map = {}
        self._symbol_name_generator = ScopedNameGenerator(
            disallow_duplicates=self._opts.disallow_duplicate_symbols,
        )
        self._bind_files = []
        self._xmr_paths = {}

    @property
    def magma_top(self) -> DefineCircuitKind:
        return self._magma_top

    @property
    def mlir_module(self) -> builtin.ModuleOp:
        return self._mlir_module

    @property
    def xmr_paths(self) -> Dict:
        return self._xmr_paths

    def new_hardware_module(
            self, magma_defn_or_decl: CircuitKind) -> HardwareModule:
        return HardwareModule(magma_defn_or_decl, weakref.ref(self), self._opts)

    def get_hardware_module(
            self, magma_defn_or_decl: CircuitKind) -> HardwareModule:
        key = self._make_key(magma_defn_or_decl)
        return self._hardware_modules[key]

    def set_hardware_module(
            self, magma_defn_or_decl: CircuitKind,
            hardware_module: HardwareModule):
        key = self._make_key(magma_defn_or_decl)
        if key in self._hardware_modules:
            raise ValueError(f"Hardware module '{key}' already exists")
        self._hardware_modules[key] = hardware_module

    def has_hardware_module(
            self, magma_defn_or_decl: CircuitKind) -> bool:
        key = self._make_key(magma_defn_or_decl)
        return key in self._hardware_modules

    def get_mapped_symbol(self, obj: Type) -> MlirSymbol:
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

    def add_bind_file(self, filename: str):
        self._bind_files.append(filename)

    def compile(self):
        deps = dependencies(self._magma_top, include_self=True)
        with push_block(self._mlir_module):
            for dep in deps:
                if self.has_hardware_module(dep):
                    continue
                hardware_module = self.new_hardware_module(dep)
                hardware_module.compile()
                if hardware_module.hw_module:
                    self.set_hardware_module(dep, hardware_module)
        self._write_listings_file()

    @staticmethod
    def _make_key(magma_defn_or_decl: CircuitKind) -> str:
        return magma_defn_or_decl.name

    def _write_listings_file(self):
        if not self._bind_files:
            return
        filename = self._opts.basename + "_bind_files.list"
        with open(filename, "w") as f:
            listing = "\n".join(self._bind_files)
            f.write(listing)
