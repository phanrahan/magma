from coreir import Context
from ..array import Array
from ..tuple import Tuple
from ..clock import AsyncReset, AsyncResetN
from ..config import config, EnvConfig
from ..logging import root_logger
from ..t import In, Out
from .. import singleton
from ..circuit import DeclareCircuit
from .coreir_transformer import DefnOrDeclTransformer
from ..passes import DefinitionPass
from .util import keydefaultdict
from ..wire import wire


config._register(
    coreir_backend_log_level=EnvConfig(
        "MAGMA_COREIR_BACKEND_LOG_LEVEL", "WARN"),
)

_logger = root_logger().getChild("coreir_backend")
_logger.setLevel(config.coreir_backend_log_level)


# Singleton context meant to be used with coreir/magma code
@singleton
class CoreIRContextSingleton:
    __instance = None

    def get_instance(self):
        return self.__instance

    def reset_instance(self):
        self.__instance = Context()

    def __init__(self):
        self.__instance = Context()


CoreIRContextSingleton()

_context_to_modules = {}


class CoreIRBackend:
    def __init__(self, context=None):
        singleton = CoreIRContextSingleton().get_instance()
        if context is None:
            context = singleton
        if context is not singleton:
            _logger.warning("Creating CoreIRBackend with non-singleton CoreIR "
                            "context.")
        self.modules = _context_to_modules.setdefault(context, {})
        self.context = context
        self.libs = keydefaultdict(self.context.get_lib)
        self.libs_used = set()
        self.constant_cache = {}
        self.sv_bind_files = {}

    def compile(self, defn_or_decl):
        _logger.debug(f"Compiling: {defn_or_decl.name}")
        transformer = DefnOrDeclTransformer(self, defn_or_decl)
        transformer.run()
        self.modules[defn_or_decl.name] = transformer.coreir_module
        return self.modules


class InsertWrapCasts(DefinitionPass):
    def sim(self, value_store, state_store):
        input_val = value_store.get_value(getattr(self, "in"))
        value_store.set_value(self.out, input_val)

    def define_wrap(self, wrap_type, in_type, out_type):
        name = f"coreir_wrap{wrap_type}".replace("(", "").replace(")", "")
        return DeclareCircuit(name,
                              "in",
                              In(in_type),
                              "out",
                              Out(out_type),
                              coreir_genargs={"type": wrap_type},
                              coreir_name="wrap",
                              coreir_lib="coreir",
                              simulate=self.sim)

    def wrap_if_arst(self, port, definition):
        if isinstance(port, (Array, Tuple)):
            for t in port:
                self.wrap_if_arst(t, definition)
        elif port.is_input():
            if isinstance(port, (AsyncReset, AsyncResetN)) or \
                    isinstance(port.value(), (AsyncReset, AsyncResetN)):
                value = port.value()
                if value is not None and not issubclass(
                        type(value), type(port).flip()):
                    port.unwire(value)
                    if isinstance(port, (AsyncReset, AsyncResetN)):
                        inst = self.define_wrap(
                            type(port).flip(), type(port), type(value))()
                    else:
                        inst = self.define_wrap(
                            type(value).flip(), type(port), type(value))()
                    definition.place(inst)
                    getattr(inst, "in") <= value
                    wire(inst.out, port)

    def __call__(self, definition):
        # copy, because wrapping might add instances
        instances = definition.instances[:]
        for instance in definition.instances:
            if type(instance).coreir_name == "wrap" or \
                    type(instance).coreir_name == "unwrap":
                continue
            for port in instance.interface.ports.values():
                self.wrap_if_arst(port, definition)
        for port in definition.interface.ports.values():
            self.wrap_if_arst(port, definition)


def compile(main, file_name=None, context=None):
    InsertWrapCasts(main).run()
    backend = CoreIRBackend(context)
    backend.compile(main)
    if file_name is not None:
        return backend.modules[main.coreir_name].save_to_file(file_name)
    else:
        return backend.modules[main.coreir_name]
