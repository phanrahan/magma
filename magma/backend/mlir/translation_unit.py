import pathlib
from typing import Any, Dict, Iterable
import weakref

from magma.backend.mlir.builtin import builtin
from magma.backend.mlir.compile_to_mlir_opts import CompileToMlirOpts
from magma.backend.mlir.errors import MlirCompilerInternalError
from magma.backend.mlir.hardware_module import HardwareModule
from magma.backend.mlir.hw import hw
from magma.backend.mlir.mlir import MlirSymbol, push_block
from magma.backend.mlir.scoped_name_generator import ScopedNameGenerator
from magma.backend.mlir.sv import sv
from magma.bind2 import is_bound_module
from magma.circuit import CircuitKind, DefineCircuitKind
from magma.common import find_by_value, only
from magma.passes import dependencies
from magma.t import Type


def _set_module_attrs(mlir_module: builtin.ModuleOp, opts: CompileToMlirOpts):
    lowering_options = [
        f"locationInfoStyle={opts.location_info_style}",
    ]
    if opts.explicit_bitcast:
        lowering_options.append("explicitBitcast")
    if opts.disallow_expression_inlining_in_ports:
        lowering_options.append("disallowExpressionInliningInPorts")
    if opts.disallow_local_variables:
        lowering_options.append("disallowLocalVariables")
    if opts.omit_version_comment:
        lowering_options.append("omitVersionComment")
    if lowering_options:
        mlir_module.attr_dict["circt.loweringOptions"] = builtin.StringAttr(
            f"{','.join(lowering_options)}"
        )


def _prepare_for_split_verilog(
        hardware_modules: Iterable[HardwareModule],
        bind_ops: Iterable[sv.BindOp],
        symbol_map: Dict[Any, MlirSymbol],
        basename: str,
        suffix: str,
):
    filename = pathlib.Path(f"{basename}.{suffix}")
    bound_module_to_filename = {}
    for hardware_module in hardware_modules:
        if hardware_module.hw_module is None:
            continue
        magma_defn_or_decl = hardware_module.magma_defn_or_decl
        if is_bound_module(magma_defn_or_decl):
            name = magma_defn_or_decl.name
            bound_module_to_filename[magma_defn_or_decl] = output_filename = (
                filename.parent / f"{name}.{suffix}"
            )
        else:
            output_filename = filename
        hardware_module.hw_module.attr_dict["output_file"] = (
            hw.OutputFileAttr(str(output_filename))
        )
    for bind_op in bind_ops:
        magma_inst = only(find_by_value(symbol_map, bind_op.instance.name))
        output_filename = bound_module_to_filename[type(magma_inst)]
        bind_op.attr_dict["output_file"] = (
            hw.OutputFileAttr(str(output_filename))
        )


class TranslationUnit:
    def __init__(self, magma_top: DefineCircuitKind, opts: CompileToMlirOpts):
        self._magma_top = magma_top
        self._opts = opts
        self._mlir_module = builtin.ModuleOp()
        _set_module_attrs(self._mlir_module, opts)
        self._hardware_modules = {}
        self._symbol_map = {}
        self._symbol_name_generator = ScopedNameGenerator(
            disallow_duplicates=self._opts.disallow_duplicate_symbols,
        )
        self._external_bind_files = []
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

    def add_external_bind_file(self, filename: str):
        self._external_bind_files.append(filename)

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
        if self._opts.split_verilog:
            if self._opts.basename is None:
                raise ValueError(
                    "Must specify basename if split_verilog is set"
                )
            _prepare_for_split_verilog(
                self._hardware_modules.values(),
                filter(
                    lambda op: isinstance(op, sv.BindOp),
                    self._mlir_module.block.operations
                ),
                self._symbol_map,
                self._opts.basename,
                ("sv" if self._opts.sv else "v"),
            )
        self._process_bound_modules()

    @staticmethod
    def _make_key(magma_defn_or_decl: CircuitKind) -> str:
        return magma_defn_or_decl.name

    def _process_bound_modules(self):
        filelist_filename = self._opts.basename + "_bind_files.list"
        has_native_bound_modules = False
        for hardware_module in self._hardware_modules.values():
            if hardware_module.hw_module is None:
                continue
            if not is_bound_module(hardware_module.magma_defn_or_decl):
                continue
            has_native_bound_modules = True
            hardware_module.hw_module.attr_dict["output_filelist"] = (
                hw.FileListAttr(filelist_filename)
            )
        if not self._external_bind_files:
            return
        if has_native_bound_modules:
            raise MlirCompilerInternalError(
                "Mix of native and external (likely CoreIR compiled) bind "
                "modules not supported."
            )
        with open(filelist_filename, "w") as f:
            f.write("\n".join(self._external_bind_files))
