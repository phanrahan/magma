from magma.config import config, EnvConfig
from magma.backend.coreir.coreir_runtime import coreir_context, module_map
from magma.backend.coreir.coreir_transformer import DefnOrDeclTransformer
from magma.backend.coreir.insert_wrap_casts import insert_wrap_casts
from magma.backend.util import keydefaultdict
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
        self.modules = module_map().setdefault(context, {})
        self.context = context
        self.libs = keydefaultdict(self.context.get_lib)
        self.libs_used = set()
        self.constant_cache = {}
        self.sv_bind_files = {}

    def reset(self):
        self._init(context=None)

    def compile(self, defn_or_decl, opts=None):
        _logger.debug(f"Compiling: {defn_or_decl.name}")
        opts = opts if opts is not None else {}
        transformer = DefnOrDeclTransformer(self, opts, defn_or_decl)
        transformer.run()
        self.modules[defn_or_decl.name] = transformer.coreir_module
        return self.modules


def compile(main, file_name=None, context=None):
    insert_wrap_casts(main)
    backend = CoreIRBackend(context)
    backend.compile(main)
    if file_name is not None:
        return backend.modules[main.coreir_name].save_to_file(file_name)
    else:
        return backend.modules[main.coreir_name]
