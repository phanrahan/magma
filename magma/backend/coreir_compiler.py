import subprocess
from ..compiler import Compiler
from ..frontend import coreir_ as coreir_frontend
from .coreir_ import InsertWrapCasts
from ..passes import DefinitionPass, InstanceGraphPass


def _compile_to_coreir(main, file_name, opts):
    # Underscore so our coreir module doesn't conflict with coreir bindings
    # package.
    backend = coreir_frontend.GetCoreIRBackend()
    InsertWrapCasts(main).run()
    backend.compile(main)
    passes = opts.get("passes", [])
    if "markdirty" not in passes:
        passes.append("markdirty")
    namespaces = opts.get("namespaces", ["global"])
    backend.context.run_passes(passes, namespaces)

    backend.modules[main.coreir_name].save_to_file(file_name + ".json")
    if opts.get("output_verilog", False):
        deps = opts.get("coreir_libs", set())
        pass_ = InstanceGraphPass(main)
        pass_.run()
        for key, _ in pass_.tsortedgraph:
            if key.coreir_lib:
                deps.add(key.coreir_lib)
            elif hasattr(key, 'wrappedModule'):
                deps |= key.coreir_wrapped_modules_libs_used
        for namespace in namespaces:
            deps.add(namespace)
        # TODO(rsetaluri): Expose compilation to verilog in pycoreir rather than
        # calling the binary from the command line.
        lib_arg = ""
        if deps:
            lib_arg = f"-l {','.join(deps)}"
        cmd = f"coreir {lib_arg} -i {file_name}.json"
        if opts.get("split", ""):
            split = opts["split"]
            cmd += f" -o \"{split}/*.v\" -s"
        else:
            cmd += f" -o {file_name}.v"
        if opts.get("inline", False):
            cmd += " --inline"
        if opts.get("verilator_debug", False):
            cmd += " --verilator_debug"
        assert not subprocess.run(cmd, shell=True).returncode, \
            "Running coreir failed"


class CoreIRCompiler(Compiler):
    def compile(self):
        _compile_to_coreir(self.main, self.basename, self.opts)
