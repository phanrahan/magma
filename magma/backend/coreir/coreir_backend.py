from magma.config import config, EnvConfig
from magma.backend.coreir.coreir_runtime import coreir_context, compiler_cache
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
        self._context = context
        self._lib_cache = {}
        self._included_libs = set()
        self._bound_modules = {}
        self._uniquifier = None

    @property
    def context(self):
        return self._context

    @property
    def uniquifier(self):
        if self._uniquifier is None:
            raise ValueError("Uniquifier has not been set")
        return self._uniquifier

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

    def bind_module(self, name, module):
        self._bound_modules[name] = module

    def bound_modules(self):
        return self._bound_modules.copy()

    def reset(self):
        self._init(context=None)

    def set_uniquifier(self, uniquifier):
        self._uniquifier = uniquifier

    def compile(self, defn_or_decl, opts=None):
        _logger.debug(f"Compiling: {defn_or_decl.name}")
        opts = opts if opts is not None else {}
        transformer = DefnOrDeclTransformer(self, opts, defn_or_decl)
        transformer.run()
        return transformer.coreir_module


def compile(main, file_name=None, context=None):
    insert_wrap_casts(main)
    backend = CoreIRBackend(context)
    coreir_module = backend.compile(main)
    if file_name is None:
        return coreir_module
    return coreir_module.save_to_file(file_name)
