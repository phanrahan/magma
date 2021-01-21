from magma.config import config, EnvConfig
from magma.backend.coreir.coreir_runtime import coreir_context, module_map
from magma.backend.coreir.coreir_transformer import DefnOrDeclTransformer
from magma.backend.coreir.insert_wrap_casts import insert_wrap_casts
from magma.logging import root_logger


config._register(
    coreir_backend_log_level=EnvConfig(
        "MAGMA_COREIR_BACKEND_LOG_LEVEL", "WARN"),
)

_logger = root_logger().getChild("coreir_backend")
_logger.setLevel(config.coreir_backend_log_level)


class CoreIRBackend:
    def __init__(self, context=None):
        self._init(context)

    def _init(self, context):
        singleton = coreir_context()
        if context is None:
            context = singleton
        if context is not singleton:
            _logger.warning("Creating CoreIRBackend with non-singleton CoreIR "
                            "context.")
        self._modules = module_map().setdefault(context, {})
        self._context = context
        self._lib_cache = {}
        self._included_libs = set()
        self.constant_cache = {}
        self.sv_bind_files = {}

    def add_module(self, magma_module, coreir_module):
        self._modules[magma_module.coreir_name] = coreir_module

    def get_module(self, magma_module):
        # NOTE(rsetaluri): Throws KeyError if @magma_module has not been added.
        return self._modules[magma_module.coreir_name]

    def include_lib_or_libs(self, lib_or_libs):
        try:
            self._included_libs |= lib_or_libs
        except TypeError:  # single element
            self._included_libs.add(lib_or_libs)

    def included_libs(self):
        return self._included_libs.copy()

    def get_lib(self, lib):
        try:
            return self._lib_cache[lib]
        except KeyError:
            ret = self._lib_cache[lib] = self.context.get_lib(lib)
            return ret

    @property
    def context(self):
        return self._context

    def reset(self):
        self._init(context=None)

    def compile(self, defn_or_decl, opts=None):
        _logger.debug(f"Compiling: {defn_or_decl.name}")
        opts = opts if opts is not None else {}
        transformer = DefnOrDeclTransformer(self, opts, defn_or_decl)
        transformer.run()
        return self._modules


def compile(main, file_name=None, context=None):
    insert_wrap_casts(main)
    backend = CoreIRBackend(context)
    backend.compile(main)
    if file_name is None:
        return backend.get_module(main)
    return backend.get_module(main).save_to_file(file_name)
