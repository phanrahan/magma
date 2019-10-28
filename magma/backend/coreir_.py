from collections import OrderedDict
from hwtypes import BitVector
import os
<<<<<<< HEAD
from ..bit import VCC, GND, Bit, BitIn, BitOut
from ..array import Array
from ..tuple import Tuple, Product
from ..clock import wiredefaultclock, wireclock, Clock, Enable, Reset, \
    AsyncReset, ResetN, AsyncResetN
=======
from ..bit import VCC, GND, BitType, BitIn, BitOut, MakeBit, BitKind
from ..array import ArrayKind, ArrayType, Array
from ..tuple import TupleKind, TupleType, Tuple
from ..clock import wiredefaultclock, wireclock, ClockType, Clock, ResetType, \
    ClockKind, EnableKind, ResetKind, AsyncResetType, AsyncResetKind, ResetNKind, \
    AsyncResetNKind, AsyncResetNType, ResetType
>>>>>>> master
from ..bitutils import seq2int
from ..backend.verilog import find
from ..logging import error
import coreir
from ..ref import ArrayRef, DefnRef, TupleRef, InstRef
from ..passes import InstanceGraphPass
from ..t import In
import logging
from .util import make_relative, get_codegen_debug_info
from ..interface import InterfaceKind
import inspect
import copy
import json
from .. import singleton
from warnings import warn

from collections import defaultdict

logger = logging.getLogger('magma').getChild('coreir_backend')
level = os.getenv("MAGMA_COREIR_BACKEND_LOG_LEVEL", "WARN")
# TODO: Factor this with magma.logging code for debug level validation
if level in ["DEBUG", "WARN", "INFO"]:
    logger.setLevel(getattr(logging, level))
elif level is not None:
    logger.warning("Unsupported value for MAGMA_COREIR_BACKEND_LOG_LEVEL:"
                   f" {level}")
# logger.setLevel(logging.DEBUG)

class CoreIRBackendError(RuntimeError):
    pass

class keydefaultdict(defaultdict):
    # From https://stackoverflow.com/questions/2912231/is-there-a-clever-way-to-pass-the-key-to-defaultdicts-default-factory
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )  # pragma: no cover
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def name_to_coreir_select(name):
    if isinstance(name, InstRef):
        return name.inst.name + "." + str(name.name)
    elif isinstance(name, DefnRef):
        return "self." + name.name
    elif isinstance(name, ArrayRef):
        return name_to_coreir_select(name.array.name) + "." + str(name.index)
    elif isinstance(name, TupleRef):
        index = name.index
        try:
            int(index)
            index = f"_{index}"
        except ValueError:
            pass
        return name_to_coreir_select(name.tuple.name) + "." + index
    else:
        raise NotImplementedError(name)


def magma_port_to_coreir(port):
    return name_to_coreir_select(port.name)

# Singleton context meant to be used with coreir/magma code
@singleton
class CoreIRContextSingleton:
    __instance = None

    def get_instance(self):
        return self.__instance

    def reset_instance(self):
        self.__instance = coreir.Context()

    def __init__(self):
        self.__instance = coreir.Context()
CoreIRContextSingleton()

class CoreIRBackend:
    context_to_modules_map = {}
    def __init__(self, context=None, check_context_is_default=True):
        if context is None:
            context = CoreIRContextSingleton().get_instance()
        elif check_context_is_default & (context != CoreIRContextSingleton().get_instance()):
            warn("Creating CoreIRBackend with non-singleton CoreIR context. "
                 "If you're sure you want to do this, set check_context_is_default "
                 "when initializing the CoreIRBackend.")
        if context not in CoreIRBackend.context_to_modules_map:
            CoreIRBackend.context_to_modules_map[context] = {}
        self.modules = CoreIRBackend.context_to_modules_map[context]
        self.context = context
        self.libs = keydefaultdict(self.context.get_lib)
        self.libs_used = set()
        self.__constant_cache = {}
        self.__unique_concat_id = -1

    def check_interface(self, definition):
        # for now only allow Bit, Array, or Tuple
        def check_type(port, errorMessage=""):
            if issubclass(port, Array):
                check_type(port.T, errorMessage.format("Array({}, {})").format(
                    str(port.N), "{}"))
            elif issubclass(port, Tuple):
                for (k, t) in zip(port.keys(), port.types()):
                    check_type(t, errorMessage.format("Tuple({}:{})".format(k, "{}")))
            elif issubclass(port, (Bit, Clock, Enable, Reset, AsyncReset, ResetN, AsyncResetN)):
                return
            else:
                raise CoreIRBackendError(errorMessage.format(str(port)))
        for name, port in definition.interface.ports.items():
            check_type(type(port), 'Error: Argument {} must be comprised only of Bit, Array, or Tuple')

    def get_type(self, port):
        if issubclass(port, Array):
            _type = self.context.Array(port.N, self.get_type(port.T))
        elif issubclass(port, Tuple):
            def to_string(k):
                """
                Unnamed tuples have integer keys (e.g. 0, 1, 2),
                we prefix them with "_" so they can be consumed by coreir's
                Record type (key names are constrained such that they can't be
                integers)
                """
                try:
                    int(k)
                    return f"_{k}"
                except ValueError:
                    return k
            _type = self.context.Record({
                to_string(k): self.get_type(t) for (k, t) in
                zip(port.keys(), port.types())
            })
        elif port.is_input():
            if issubclass(port, Clock):
                _type = self.context.named_types[("coreir", "clk")]
            elif issubclass(port, AsyncReset, AsyncResetN):
                _type = self.context.named_types[("coreir", "arst")]
            else:
                _type = self.context.Bit()
        elif port.is_output():
            if issubclass(port, Clock):
                _type = self.context.named_types[("coreir", "clkIn")]
            elif issubclass(port, AsyncReset, AsyncResetN):
                _type = self.context.named_types[("coreir", "arstIn")]
            else:
                _type = self.context.BitIn()
        else:
            _type = self.context.BitInOut()
        return _type

    coreirNamedTypeToPortDict = {
        "clk": Clock,
        "coreir.clkIn": Clock
    }

    def get_ports(self, coreir_type, renamed_ports):
        if (coreir_type.kind == "Bit"):
            return BitOut
        elif (coreir_type.kind == "BitIn"):
            return BitIn
        elif (coreir_type.kind == "Array"):
            return Array[len(coreir_type), self.get_ports(coreir_type.element_type, renamed_ports)]
        elif (coreir_type.kind == "Record"):
            elements = {}
            for item in coreir_type.items():
                name = item[0]
                # replace  the in port with I as can't reference that
                if name == "in":
                    name = "I"
                    renamed_ports[name] = "in"
                elements[name] = self.get_ports(item[1], renamed_ports)
            return type("anon", (Product, ), elements)
        elif (coreir_type.kind == "Named"):
            # exception to handle clock types, since other named types not handled
            if coreir_type.name in self.coreirNamedTypeToPortDict:
                return In(self.coreirNamedTypeToPortDict[coreir_type.name])
            else:
                raise NotImplementedError("not all named types supported yet")
        else:
            raise NotImplementedError("Trying to convert unknown coreir type to magma type")

    def get_ports_as_list(self, ports):
        return [item for i in range(ports.N) for item in [list(ports.keys())[i], ports.types()[i]]]

    def convert_interface_to_module_type(self, interface):
        args = OrderedDict()
        for name, port in interface.ports.items():
            args[name] = self.get_type(type(port))
        return self.context.Record(args)

    def compile_instance(self, instance, module_definition):
        name = instance.__class__.coreir_name
        lib = self.libs[instance.coreir_lib]
        logger.debug(f"Compiling instance {(instance.name, type(instance))}")
        if instance.coreir_genargs is None:
            if hasattr(instance, "wrappedModule") and \
               instance.wrappedModule.context == self.context:
                module = instance.wrappedModule
            else:
                module = lib.modules[name]
            args = {}
            for name, value in instance.kwargs.items():
                if name in {"name", "loc"}:
                    continue  # Skip
                elif isinstance(value, tuple):
                    args[name] = BitVector[value[1]](value[0])
                else:
                    args[name] = value
            args = self.context.new_values(args)
            return module_definition.add_module_instance(instance.name, module, args)
        else:
            generator = lib.generators[name]
            config_args = {}
            for name, value in instance.coreir_configargs.items():
                config_args[name] = value
            config_args = self.context.new_values(config_args)
            gen_args = {}
            for name, value in type(instance).coreir_genargs.items():
                if isinstance(value, AsyncReset) or isinstance(value, type) and issubclass(value, AsyncReset):
                    value = self.context.named_types["coreir", "arst"]
                elif isinstance(value, Clock) or isinstance(value, type) and issubclass(value, Clock):
                    value = self.context.named_types["coreir", "clk"]
                gen_args[name] = value
            gen_args = self.context.new_values(gen_args)
            return module_definition.add_generator_instance(instance.name,
                    generator, gen_args, config_args)

    def add_non_input_ports(self, non_input_ports, port):
        if not port.is_input():
            non_input_ports[port] = magma_port_to_coreir(port)
        if isinstance(port, (Tuple, Array)):
            for element in port:
                self.add_non_input_ports(non_input_ports, element)

    def compile_declaration(self, declaration):
        if declaration.coreir_lib is not None:
            self.libs_used.add(declaration.coreir_lib)
        # These libraries are already available by default in coreir, so we
        # don't need declarations
        if declaration.coreir_lib in ["coreir", "corebit", "commonlib"]:
            if declaration.coreir_genargs is None:
                return self.libs[declaration.coreir_lib].modules[declaration.coreir_name]
            else:
                return self.libs[declaration.coreir_lib].generators[declaration.coreir_name]
        if declaration.name in self.modules:
            logger.debug(f"    {declaration} already compiled, skipping")
            return
        module_type = self.convert_interface_to_module_type(declaration.interface)
        if isinstance(declaration.interface, InterfaceKind):
            module_type = self.context.Flip(module_type)

        kwargs = {}
        if hasattr(declaration, "coreir_config_param_types"):
            kwargs["cparams"] = \
                self.make_cparams(declaration.coreir_config_param_types)

        coreir_module = \
            self.context.global_namespace.new_module(declaration.coreir_name,
                                                     module_type, **kwargs)
        if get_codegen_debug_info() and declaration.debug_info:
            coreir_module.add_metadata("filename", json.dumps(make_relative(declaration.debug_info.filename)))
            coreir_module.add_metadata("lineno", json.dumps(str(declaration.debug_info.lineno)))
        return coreir_module

    def compile_definition_to_module_definition(self, definition, module_definition):
        if definition.coreir_lib is not None:
            self.libs_used.add(definition.coreir_lib)
        non_input_ports = {}
        for name, port in definition.interface.ports.items():
            logger.debug("{}, {}, {}".format(name, port, port.is_output()))
            self.add_non_input_ports(non_input_ports, port)

        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            wireclock(definition, instance)
            coreir_instance = self.compile_instance(instance, module_definition)
            if get_codegen_debug_info() and getattr(instance, "debug_info", False):
                coreir_instance.add_metadata("filename", json.dumps(make_relative(instance.debug_info.filename)))
                coreir_instance.add_metadata("lineno", json.dumps(str(instance.debug_info.lineno)))
            for name, port in instance.interface.ports.items():
                self.add_non_input_ports(non_input_ports, port)

        for instance in definition.instances:
            for name, port in instance.interface.ports.items():
                self.connect_non_outputs(module_definition, port,
                                         non_input_ports)

        for port in definition.interface.ports.values():
            self.connect_non_outputs(module_definition, port, non_input_ports)

    def connect_non_outputs(self, module_definition, port,
                      non_input_ports):
        # Recurse into non input types that may contain inout children
        if isinstance(port, Tuple) and not port.is_input() or \
                isinstance(port, Array) and not port.T.is_input():
            for elem in port:
                self.connect_non_outputs(module_definition, elem,
                                         non_input_ports)
        elif not port.is_output():
            self.connect(module_definition, port, port.value(),
                         non_input_ports)

    def make_cparams(self, param_types):
        cparams = {}
        for param, type_ in param_types.items():
            if type_ is int:
                type_ = self.context.Int()
            elif type_ is bool:
                type_ = self.context.Bool()
            elif type_ is str:
                type_ = self.context.String()
            elif type_ is BitVector:
                type_ = self.context.BitVector()
            else:
                raise NotImplementedError(type_)
            cparams[param] = type_
        return self.context.newParams(cparams)

    def compile_definition(self, definition):
        logger.debug(f"Compiling definition {definition}")
        if definition.name in self.modules:
            logger.debug(f"    {definition} already compiled, skipping")
            return self.modules[definition.name]
        self.check_interface(definition)
        module_type = self.convert_interface_to_module_type(definition.interface)
        kwargs = {}
        if hasattr(definition, "coreir_config_param_types"):
            kwargs["cparams"] = \
                self.make_cparams(definition.coreir_config_param_types)

        coreir_module = \
            self.context.global_namespace.new_module(definition.coreir_name,
                                                     module_type, **kwargs)
        if get_codegen_debug_info() and definition.debug_info:
            coreir_module.add_metadata("filename", json.dumps(make_relative(definition.debug_info.filename)))
            coreir_module.add_metadata("lineno", json.dumps(str(definition.debug_info.lineno)))

        # If this module was imported from verilog, do not go through the
        # general module construction flow. Instead just attach the verilog
        # source as metadata and return the module. Also, we attach any
        # contained instances as CoreIR instances.
        if hasattr(definition, "verilogFile") and definition.verilogFile:
            verilog_metadata = {"verilog_string": definition.verilogFile}
            coreir_module.add_metadata("verilog", json.dumps(verilog_metadata))
            module_definition = coreir_module.new_definition()
            coreir_module.definition = module_definition
            for instance in definition.instances:
                self.compile_instance(instance, module_definition)
            return coreir_module

        module_definition = coreir_module.new_definition()
        self.compile_definition_to_module_definition(definition, module_definition)
        coreir_module.definition = module_definition
        return coreir_module

    def connect(self, module_definition, port, value, non_input_ports):
        self.__unique_concat_id

        # allow clocks or arrays of clocks to be unwired as CoreIR can wire them up
        def is_clock_or_nested_clock(p):
            if isinstance(p, Clock) or isinstance(p, type) and issubclass(p, Clock):
                return True
            elif isinstance(p, Array) or isinstance(p, type) and issubclass(p, Array):
                return is_clock_or_nested_clock(p.T)
            elif isinstance(p, Tuple) or isinstance(p, type) and issubclass(p, Tuple):
                for item in p.types():
                    if is_clock_or_nested_clock(item):
                        return True
            return False

        if value is None and is_clock_or_nested_clock(port):
            return
        elif value is None:
            if port.is_inout():
                # Skip inouts because they might be connected as an input
                return
            raise Exception(f"Got None for port '{port.debug_name}', is it "
                            "connected to anything?")
        elif isinstance(value, coreir.Wireable):
            source = value

        elif isinstance(value, Array) and all(x in {VCC, GND} for x in value):
            source = self.get_constant_instance(value, len(value),
                    module_definition)
        elif value.anon() and isinstance(value, Array):
            for p, v in zip(port, value):
                self.connect(module_definition, p, v, non_input_ports)
            return
        elif isinstance(value, Tuple) and value.anon():
            for p, v in zip(port, value):
                self.connect(module_definition, p, v, non_input_ports)
            return
        elif value is VCC or value is GND:
            source = self.get_constant_instance(value, None, module_definition)
        else:
            # logger.debug((value, non_input_ports))
            # logger.debug((id(value), [id(key) for key in non_input_ports]))
            source = module_definition.select(non_input_ports[value])
        sink = module_definition.select(magma_port_to_coreir(port))
        module_definition.connect(source, sink)
        if get_codegen_debug_info() and getattr(port, "debug_info", False):
            module_definition.add_metadata(source, sink, "filename", json.dumps(make_relative(port.debug_info.filename)))
            module_definition.add_metadata(source, sink, "lineno", json.dumps(str(port.debug_info.lineno)))


    __unique_constant_id = -1
    def get_constant_instance(self, constant, num_bits, module_definition):
        if module_definition not in self.__constant_cache:
            self.__constant_cache[module_definition] = {}

        bit_type_to_constant_map = {
            GND: 0,
            VCC: 1
        }
        if constant in bit_type_to_constant_map:
            value = bit_type_to_constant_map[constant]
        elif isinstance(constant, Array):
            value = BitVector[len(constant)]([bit_type_to_constant_map[x] for x in constant])
        else:
            raise NotImplementedError(constant)
        if (value, num_bits) not in self.__constant_cache[module_definition]:
            self.__unique_constant_id += 1
            if num_bits is None:
                config = self.context.new_values({"value": bool(value)})
                name = "bit_const_{}_{}".format(value, num_bits)
                corebit_const_module = self.libs['corebit'].modules["const"]
                module_definition.add_module_instance(name, corebit_const_module, config)
            else:
                gen_args = self.context.new_values({"width": num_bits})
                config = self.context.new_values({"value": value})
                # name = "const_{}_{}".format(constant, self.__unique_constant_id)
                name = "const_{}_{}".format(value, num_bits)
                const_generator = self.libs['coreir'].generators["const"]
                module_definition.add_generator_instance(name, const_generator, gen_args, config)
            # return module_definition.select("{}.out".format(name))
            self.__constant_cache[module_definition][(value, num_bits)] = module_definition.select("{}.out".format(name))
        return self.__constant_cache[module_definition][(value, num_bits)]

    def compile_dependencies(self, defn):
        pass_ = InstanceGraphPass(defn)
        pass_.run()
        dependency_names = [key.name for key, _ in pass_.tsortedgraph]
        logger.debug(f"tsortedgraph: {dependency_names}")
        for key, _ in pass_.tsortedgraph:
            if key == defn:
                continue
            if key.name in self.modules:
                continue
            if key.is_definition:
                # don't try to compile if already have definition
                if hasattr(key, 'wrappedModule') and \
                   key.wrappedModule.context == self.context:
                    self.modules[key.name] = key.wrappedModule
                    self.libs_used |= key.coreir_wrapped_modules_libs_used
                else:
                    self.modules[key.name] = self.compile_definition(key)
                    key.wrappedModule = self.modules[key.name]
                    key.coreir_wrapped_modules_libs_used = \
                        copy.copy(self.libs_used)
                    logger.debug(f"Compiled module {key.name}, libs used = {self.libs_used}")
            else:
                self.modules[key.name] = self.compile_declaration(key)

    def compile(self, defn_or_declaration):
        logger.debug(f"Compiling: {defn_or_declaration.name}")
        if defn_or_declaration.is_definition:
            self.compile_dependencies(defn_or_declaration)
            # don't try to compile if already have definition
            if hasattr(defn_or_declaration, 'wrappedModule') and \
               defn_or_declaration.wrappedModule.context == self.context:
                self.modules[defn_or_declaration.name] = defn_or_declaration.wrappedModule
                self.libs_used |= defn_or_declaration.coreir_wrapped_modules_libs_used
            else:
                self.modules[defn_or_declaration.name] = self.compile_definition(defn_or_declaration)
                defn_or_declaration.wrappedModule = self.modules[defn_or_declaration.name]
                defn_or_declaration.coreir_wrapped_modules_libs_used = \
                    copy.copy(self.libs_used)
        else:
            self.modules[defn_or_declaration.name] = self.compile_declaration(defn_or_declaration)
        return self.modules

    def flatten_and_save(self, module, filename, namespaces=["global"], flatten=True, verifyConnectivity=True):
        passes = ["rungenerators", "wireclocks-coreir"]
        if verifyConnectivity:
            passes += ["verifyconnectivity --noclkrst"]
        if flatten:
            passes += ["flattentypes", "flatten"]
        self.context.run_passes(passes, namespaces)
        module.save_to_file(filename)

def compile(main, file_name=None, context=None, check_context_is_default=True):
    backend = CoreIRBackend(context, check_context_is_default)
    backend.compile(main)
    if file_name is not None:
        return backend.modules[main.coreir_name].save_to_file(file_name)
    else:
        return backend.modules[main.coreir_name]
