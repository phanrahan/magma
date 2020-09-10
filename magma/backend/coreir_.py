from coreir import Context
from ..array import Array
from ..tuple import Tuple
from ..clock import AsyncReset, AsyncResetN, Clock
from ..conversions import convertbit
from ..config import config, EnvConfig
from ..logging import root_logger
from ..t import In, Out, Direction
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


_context_to_modules = {}


# Singleton context meant to be used with coreir/magma code
@singleton
class CoreIRContextSingleton:
    __instance = None

    def get_instance(self):
        return self.__instance

    def reset_instance(self):
        old_instance = self.__instance
        self.__instance = Context()
        if old_instance in _context_to_modules:
            del _context_to_modules[old_instance]
        # Force freeing of C++ memory
        old_instance.delete()

    def __init__(self):
        self.__instance = Context()


CoreIRContextSingleton()


class CoreIRBackend:
    def __init__(self, context=None):
        self._init(context)

    def _init(self, context):
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

    def reset(self):
        self._init(context=None)

    def compile(self, defn_or_decl, opts=None):
        _logger.debug(f"Compiling: {defn_or_decl.name}")
        opts = opts if opts is not None else {}
        transformer = DefnOrDeclTransformer(self, opts, defn_or_decl)
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
        if isinstance(port, Tuple):
            wrapped = False
            for t in port:
                wrapped |= self.wrap_if_named_type(t, definition)
            return wrapped
        if isinstance(port, Array):
            wrapped = self.wrap_if_named_type(port[0], definition)
            if not wrapped:
                return False
            # TODO: Magma doesn't support length zero array, so slicing a
            # length 1 array off the end doesn't work as expected in normal
            # Python, so we explicilty slice port.ts
            for t in port.ts[1:]:
                self.wrap_if_named_type(t, definition)
            return True
        if not port.driven():
            return False
        value = port.value()
        if not (isinstance(port, (AsyncReset, AsyncResetN, Clock)) or
                isinstance(value, (AsyncReset, AsyncResetN, Clock))):
            return self.wrap_if_named_type(value, definition)
        undirected_t = type(port).qualify(Direction.Undirected)
        if issubclass(type(value), undirected_t):
            return self.wrap_if_named_type(value, definition)
        port_is_clock_type = isinstance(port, (AsyncReset, AsyncResetN, Clock))
        if port_is_clock_type:
            T = Out(type(port))
        else:
            T = In(type(value))

        with definition.open():
            port.unwire(value)
            in_type, out_type = type(port), type(value)
            if not port_is_clock_type:
                # value is the clock type, flip wrap types
                out_type, in_type = in_type, out_type
            inst = self.define_wrap(T, in_type, out_type)()
            wire(convertbit(value, in_type), getattr(inst, "in"))
            wire(inst.out, convertbit(port, out_type))
        return True

    def __call__(self, definition):
        # copy, because wrapping might add instances
        instances = definition.instances[:]
        for instance in instances:
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
