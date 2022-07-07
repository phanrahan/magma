import os
import subprocess
from magma.compiler import Compiler
from magma.config import EnvConfig, config
from magma.backend.coreir.insert_coreir_wires import insert_coreir_wires
from magma.backend.coreir.insert_wrap_casts import insert_wrap_casts
from magma.frontend import coreir_ as coreir_frontend
from magma.is_definition import isdefinition
from magma.logging import root_logger
from magma.passes import InstanceGraphPass
from magma.passes.raise_logs_as_exceptions import raise_logs_as_exceptions_pass
from magma.symbol_table import SymbolTable
from magma.symbol_table_utils import MasterSymbolTable


_logger = root_logger()
config._register(
    fast_coreir_verilog_compile=EnvConfig(
        "MAGMA_FAST_COREIR_VERILOG_COMPILE", False),
)


def _get_coreir_symbol_table(basename):
    with open(f"{basename}_symbol_table.json") as f:
        data = f.read()
        return SymbolTable.from_json(data)


def _make_verilog_cmd(deps, basename, opts):
    cmd = "coreir"
    if deps:
        cmd += f" -l {','.join(deps)}"
    cmd += f" -i {basename}.json"
    if opts.get("split", ""):
        split = opts["split"]
        cmd += f" -o \"{split}/*.v\" -s"
    else:
        cmd += f" -o {basename}.v"
    if opts.get("inline", False):
        cmd += " --inline"
    if opts.get("verilator_debug", False):
        cmd += " --verilator_debug"
    if opts.get("disable_width_cast", False):
        cmd += " --disable-width-cast"
    if opts.get("disable_ndarray", False):
        cmd += " --disable-ndarray"
    if opts.get("verilator_compat", False):
        cmd += " --verilator_compat"
    if opts.get("verilog_prefix", ""):
        cmd += f" --verilog-prefix {opts['verilog_prefix']}"
    if opts.get("verilog_prefix_extern", False):
        cmd += " --verilog-prefix-extern"
    if opts.get("generate_symbols", False):
        cmd += f" --symbols {basename}_symbol_table.json"
    if opts.get("use_packed_arrays", False):
        cmd += " --use-packed-arrays"
    return cmd


def _make_opts(backend, opts):
    new_opts = {}
    user_namespace = opts.get("user_namespace", None)
    if user_namespace is not None:
        if backend.context.has_namespace(user_namespace):
            user_namespace = backend.context.get_namespace(user_namespace)
        else:
            user_namespace = backend.context.new_namespace(user_namespace)
        new_opts["user_namespace"] = user_namespace
    new_opts["generate_symbols"] = opts.get("generate_symbols", False)
    return new_opts


class CoreIRCompiler(Compiler):
    def __init__(self, main, basename, opts):
        super().__init__(main, basename, opts)
        self.namespaces = self.opts.get("namespaces", ["global"])
        self.passes = opts.get("passes", [])
        if "markdirty" not in self.passes:
            self.passes.append("markdirty")
        self.deps = self._deps()
        self.backend = coreir_frontend.GetCoreIRBackend()

    def compile(self):
        result = {}
        result["symbol_table"] = symbol_table = SymbolTable()
        insert_coreir_wires(self.main)
        insert_wrap_casts(self.main)
        raise_logs_as_exceptions_pass(self.main)
        backend = self.backend
        opts = _make_opts(backend, self.opts)
        opts["symbol_table"] = symbol_table
        backend.compile(self.main, opts)
        backend.context.run_passes(self.passes, self.namespaces)
        if isdefinition(self.main):
            result["coreir_module"] = backend.get_module(self.main)
        output_json = (self.opts.get("output_intermediate", False) or
                       not self.opts.get("output_verilog", False) or
                       not config.fast_coreir_verilog_compile)
        if output_json:
            filename = f"{self.basename}.json"
            if isdefinition(self.main):
                backend.context.set_top(backend.get_module(self.main))
            backend.context.save_to_file(filename, include_default_libs=False)
        if self.opts.get("output_verilog", False):
            fn = (self._fast_compile_verilog
                  if config.fast_coreir_verilog_compile
                  else self._compile_verilog)
            fn()
            self._compile_verilog_epilogue()
            if self.opts.get("generate_symbols", False):
                coreir_symbol_table = _get_coreir_symbol_table(self.basename)
                if not self.opts.get("merge_symbol_tables", True):
                    result["coreir_symbol_table"] = coreir_symbol_table
                else:
                    master = MasterSymbolTable([
                        symbol_table, coreir_symbol_table])
                    result["master_symbol_table"] = master
            return result
        has_header_or_footer = (self.opts.get("header_file", "") or
                                self.opts.get("header_str", "") or
                                self.opts.get("footer_str", ""))
        if has_header_or_footer:
            _logger.warning("[coreir-compiler] header/footer only supported "
                            "when output_verilog=True, ignoring")
        return result

    def _compile_verilog(self):
        cmd = _make_verilog_cmd(self.deps, self.basename, self.opts)
        ret = subprocess.run(cmd, shell=True).returncode
        if ret:
            raise RuntimeError(f"CoreIR cmd '{cmd}' failed with code {ret}")

    def _fast_compile_verilog(self):
        top = self.backend.get_module(self.main)
        filename = f"{self.basename}.v"
        opts = dict(
            libs=self.deps,
            split=self.opts.get("split", ""),
            inline=self.opts.get("inline", False),
            verilator_debug=self.opts.get("verilator_debug", False),
            disable_width_cast=self.opts.get("disable_width_cast", False),
        )
        if self.opts.get("verilog_prefix", False):
            raise NotImplementedError()
        if self.opts.get("use_packed_arrays", False):
            raise NotImplementedError()
        ret = self.backend.context.compile_to_verilog(top, filename, **opts)
        if not ret:
            raise RuntimeError(f"CoreIR compilation to verilog failed")

    def _compile_verilog_epilogue(self):
        self._process_header_footer()

        bind_files = []
        # TODO(leonardt): We need fresh bind_files for each compile call.
        for name, file in self.backend.bound_modules().items():
            bind_files.append(f"{name}.sv")
            filename = os.path.join(os.path.dirname(self.basename), name)
            with open(f"{filename}.sv", "w") as f:
                f.write(file)

        if bind_files:
            bind_listings_file = self.basename + "_bind_files.list"
            with open(bind_listings_file, "w") as f:
                f.write("\n".join(bind_files))

        if self.opts.get("sv", False):
            if self.opts.get("split", False):
                _logger.warning("sv not supported with split, ignoring")
            else:
                args = (f"{self.basename}.v", f"{self.basename}.sv")
                subprocess.run(["mv", *args])

    def _deps(self):
        deps = self.opts.get("coreir_libs", set())
        pass_ = InstanceGraphPass(self.main)
        pass_.run()
        for key, _ in pass_.tsortedgraph:
            if key.coreir_lib:
                deps.add(key.coreir_lib)
            elif hasattr(key, "wrappedModule"):
                deps |= key.coreir_wrapped_modules_libs_used
        deps |= set(self.namespaces)
        return deps

    def _process_header_footer(self):
        header = ""
        if self.opts.get("header_file", ""):
            with open(self.opts["header_file"], "r") as header_file:
                header = header_file.read() + "\n"
        if self.opts.get("header_str", ""):
            header += self.opts["header_str"] + "\n"
        footer = self.opts.get("footer_str", "")
        if not header and not footer:
            return
        if self.opts.get("split", ""):
            _logger.warning("header/footer not supported with split, ignoring")
            return
        with open(f"{self.basename}.v", "r") as verilog_file:
            verilog = verilog_file.read()
        with open(f"{self.basename}.v", "w") as verilog_file:
            verilog_file.write(header + verilog + "\n" + footer)
