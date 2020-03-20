from coreir import Context
from ..array import Array
from ..tuple import Tuple
from ..clock import AsyncReset, AsyncResetN, Clock
from ..conversions import convertbit
from ..config import config, EnvConfig
from ..logging import root_logger
from ..t import In, Out
from .. import singleton
from ..circuit import Circuit
from ..interface import IO
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
    def define_wrap(self, wrap_type, in_type, out_type):
        class Wrap(Circuit):
            name = f"coreir_wrap{wrap_type}".replace("(", "").replace(")", "")
            io = IO(**{"in": In(in_type), "out": Out(out_type)})
            coreir_genargs = {"type": wrap_type}
            coreir_name = "wrap"
            coreir_lib = "coreir"

            def simulate(self, value_store, state_store):
                input_val = value_store.get_value(getattr(self, "in"))
                value_store.set_value(self.out, input_val)
        return Wrap

    def wrap_if_named_type(self, port, definition):
        if isinstance(port, (Array, Tuple)):
            for t in port:
                self.wrap_if_named_type(t, definition)
            return
        if not port.is_input():
            return
        if not (isinstance(port, (AsyncReset, AsyncResetN, Clock)) or
                isinstance(port.trace(), (AsyncReset, AsyncResetN, Clock))):
            return
        value = port.trace()
        if value is None or issubclass(type(value), type(port).flip()):
            return
        if isinstance(port, (AsyncReset, AsyncResetN, Clock)):
            T = type(port).flip()
        else:
            T = type(value).flip()

        with definition.open():
            port.unwire(value)
            inst = self.define_wrap(T, type(port), type(value))()
            wire(getattr(inst, "in"), convertbit(value, type(port)))
            wire(inst.out, convertbit(port, type(value)))

    def __call__(self, definition):
        # copy, because wrapping might add instances
        instances = definition.instances[:]
        for instance in definition.instances:
            if type(instance).coreir_name == "wrap" or \
                    type(instance).coreir_name == "unwrap":
                continue
            for port in instance.interface.ports.values():
                self.wrap_if_named_type(port, definition)
        for port in definition.interface.ports.values():
            self.wrap_if_named_type(port, definition)


def compile(main, file_name=None, context=None):
    InsertWrapCasts(main).run()
    backend = CoreIRBackend(context)
    backend.compile(main)
    if file_name is not None:
        return backend.modules[main.coreir_name].save_to_file(file_name)
    else:
        return backend.modules[main.coreir_name]
