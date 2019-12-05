from collections import OrderedDict
from hwtypes import BitVector
import os
import magma as m
from ..bit import VCC, GND, BitType, BitIn, BitOut, MakeBit, BitKind
from ..array import ArrayKind, ArrayType, Array
from ..tuple import TupleKind, TupleType, Tuple
from ..clock import wiredefaultclock, wireclock, ClockType, Clock, ResetType, \
    ClockKind, EnableKind, ResetKind, AsyncResetType, AsyncResetKind, ResetNKind, \
    AsyncResetNKind, AsyncResetNType, ResetType
from ..bitutils import seq2int
from ..backend.verilog import find
from ..logging import error
import coreir
from ..passes import InstanceGraphPass
from ..t import In, Kind
import logging
from .util import make_relative, get_codegen_debug_info
from ..interface import InterfaceKind
from ..passes import DefinitionPass
import inspect
from copy import copy
import json
from .. import singleton
from warnings import warn

from collections import defaultdict

from .coreir_utils import *


logger = logging.getLogger('magma').getChild('coreir_backend')
level = os.getenv("MAGMA_COREIR_BACKEND_LOG_LEVEL", "WARN")
# TODO: Factor this with magma.logging code for debug level validation
if level in ["DEBUG", "WARN", "INFO"]:
    logger.setLevel(getattr(logging, level))
elif level is not None:
    logger.warning("Unsupported value for MAGMA_COREIR_BACKEND_LOG_LEVEL:"
                   f" {level}")
# logger.setLevel(logging.DEBUG)

class keydefaultdict(defaultdict):
    # From https://stackoverflow.com/questions/2912231/is-there-a-clever-way-to-pass-the-key-to-defaultdicts-default-factory
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )  # pragma: no cover
        else:
            ret = self[key] = self.default_factory(key)
            return ret


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


_context_to_modules = {}


class CoreIRBackend:
    def __init__(self, context=None, check_context_is_default=True):
        # TODO(rsetaluri): Improve this logic.
        if context is None:
            context = CoreIRContextSingleton().get_instance()
        elif check_context_is_default and context != CoreIRContextSingleton().get_instance():
            warn("Creating CoreIRBackend with non-singleton CoreIR context. "
                 "If you're sure you want to do this, set check_context_is_default "
                 "when initializing the CoreIRBackend.")
        self.modules = _context_to_modules.setdefault(context, {})
        self.context = context
        self.libs = keydefaultdict(self.context.get_lib)
        self.libs_used = set()
        self.__constant_cache = {}

    def connect_non_outputs(self, module_defn, port, non_input_ports):
        # Recurse into non input types that may contain inout children.
        if isinstance(port, TupleType) and not port.isinput() or \
           isinstance(port, ArrayType) and not port.T.isinput():
            for elem in port:
                self.connect_non_outputs(module_defn, elem, non_input_ports)
        elif not port.isoutput():
            self.connect(module_defn, port, port.value(), non_input_ports)

    def connect(self, module_definition, port, value, non_input_ports):
        # Allow clocks or arrays of clocks to be unwired as CoreIR can wire them
        # up.
        if value is None and is_clock_or_nested_clock(port):
            return
        elif value is None:
            if port.isinout():
                # Skip inouts because they might be connected as an input.
                return
            raise Exception(f"Got None for port '{port.debug_name}', is it "
                            f"connected to anything?")
        elif isinstance(value, coreir.Wireable):
            source = value
        elif isinstance(value, ArrayType) and all(x in {VCC, GND} for x in value):
            source = self.get_constant_instance(value, len(value), module_definition)
        elif value.anon() and isinstance(value, ArrayType):
            for p, v in zip(port, value):
                self.connect(module_definition, p, v, non_input_ports)
            return
        elif isinstance(value, TupleType) and value.anon():
            for p, v in zip(port, value):
                self.connect(module_definition, p, v, non_input_ports)
            return
        elif value is VCC or value is GND:
            source = self.get_constant_instance(value, None, module_definition)
        else:
            source = module_definition.select(non_input_ports[value])
        sink = module_definition.select(magma_port_to_coreir_port(port))
        module_definition.connect(source, sink)
        if get_codegen_debug_info() and getattr(port, "debug_info", False):
            attach_debug_info(module_definition, port.debug_info, source, sink)

    def get_constant_instance(self, constant, num_bits, module_definition):
        if module_definition not in self.__constant_cache:
            self.__constant_cache[module_definition] = {}

        bit_type_to_constant_map = {
            GND: 0,
            VCC: 1
        }
        if constant in bit_type_to_constant_map:
            value = bit_type_to_constant_map[constant]
        elif isinstance(constant, ArrayType):
            value = BitVector[len(constant)]([bit_type_to_constant_map[x] for x in constant])
        else:
            raise NotImplementedError(constant)
        if (value, num_bits) not in self.__constant_cache[module_definition]:
            if num_bits is None:
                config = self.context.new_values({"value": bool(value)})
                name = "bit_const_{}_{}".format(value, num_bits)
                corebit_const_module = self.libs['corebit'].modules["const"]
                module_definition.add_module_instance(name, corebit_const_module, config)
            else:
                gen_args = self.context.new_values({"width": num_bits})
                config = self.context.new_values({"value": value})
                name = f"const_{value}_{num_bits}"
                const_generator = self.libs['coreir'].generators["const"]
                module_definition.add_generator_instance(name, const_generator, gen_args, config)
            # return module_definition.select("{}.out".format(name))
            self.__constant_cache[module_definition][(value, num_bits)] = module_definition.select("{}.out".format(name))
        return self.__constant_cache[module_definition][(value, num_bits)]

    def compile_decl(self, decl):
        if decl.coreir_lib is not None:
            self.libs_used.add(decl.coreir_lib)
        # These libraries are already available by default in coreir, so we
        # don't need declarations.
        if decl.coreir_lib in ["coreir", "corebit", "commonlib"]:
            if decl.coreir_genargs is None:
                return self.libs[decl.coreir_lib].modules[decl.coreir_name]
            return self.libs[decl.coreir_lib].generators[decl.coreir_name]
        if decl.name in self.modules:
            logger.debug(f"{decl} already compiled, skipping")
            return self.modules[decl.name]
        module_type = magma_interface_to_coreir_module_type(
            self.context, decl.interface)
        if isinstance(decl.interface, InterfaceKind):
            module_type = self.context.Flip(module_type)
        kwargs = {}
        if hasattr(decl, "coreir_config_param_types"):
            param_types = decl.coreir_config_param_types
            kwargs["cparams"] = make_cparams(self.context, param_types)
        coreir_module = self.context.global_namespace.new_module(
            decl.coreir_name, module_type, **kwargs)
        if get_codegen_debug_info() and decl.debug_info:
            attach_debug_info(coreir_module, decl.debug_info)
        return coreir_module

    def compile_inst(self, inst, module_defn):
        defn = type(inst)
        lib = self.libs[inst.coreir_lib]
        logger.debug(f"Compiling instance {(inst.name, type(inst))}")
        if inst.coreir_genargs is None:
            module = get_module_of_inst(self.context, inst, lib)
            args = get_inst_args(inst)
            args = self.context.new_values(args)
            return module_defn.add_module_instance(inst.name, module, args)
        generator = lib.generators[defn.coreir_name]
        config_args = {k: v for k, v in inst.coreir_configargs.items()}
        config_args = self.context.new_values(config_args)
        gen_args = {k: map_genarg(self.context, v) for k, v in defn.coreir_genargs.items()}
        gen_args = self.context.new_values(gen_args)
        return module_defn.add_generator_instance(
            inst.name, generator, gen_args, config_args)

    def compile_defn_to_coreir_defn(self, defn, module_defn):
        if defn.coreir_lib is not None:
            self.libs_used.add(defn.coreir_lib)
        non_input_ports = {}
        for name, port in defn.interface.ports.items():
            logger.debug(f"{name}, {port}, {port.isoutput()}")
            add_non_input_ports(non_input_ports, port)
        for inst in defn.instances:
            wiredefaultclock(defn, inst)
            wireclock(defn, inst)
            coreir_inst = self.compile_inst(inst, module_defn)
            if get_codegen_debug_info() and getattr(inst, "debug_info", False):
                attach_debug_info(coreir_inst, inst.debug_info)
            for name, port in inst.interface.ports.items():
                add_non_input_ports(non_input_ports, port)
        for inst in defn.instances:
            for name, port in inst.interface.ports.items():
                self.connect_non_outputs(module_defn, port, non_input_ports)
        for port in defn.interface.ports.values():
            self.connect_non_outputs(module_defn, port, non_input_ports)

    def compile_defn(self, defn):
        logger.debug(f"Compiling definition {defn}")
        if defn.name in self.modules:
            logger.debug(f"{defn} already compiled, skipping")
            return self.modules[defn.name]
        check_magma_interface(defn.interface)
        module_type = magma_interface_to_coreir_module_type(
            self.context, defn.interface)
        kwargs = {}
        if hasattr(defn, "coreir_config_param_types"):
            param_types = defn.coreir_config_param_types
            kwargs["cparams"] = make_cparams(self.context, param_types)
        coreir_module = self.context.global_namespace.new_module(
            defn.coreir_name, module_type, **kwargs)
        if get_codegen_debug_info() and defn.debug_info:
            attach_debug_info(coreir_module, defn.debug_info)
        # If this module was imported from verilog, do not go through the
        # general module construction flow. Instead just attach the verilog
        # source as metadata and return the module. Also, we attach any
        # contained instances as CoreIR instances.
        if hasattr(defn, "verilogFile") and defn.verilogFile:
            verilog_metadata = {"verilog_string": defn.verilogFile}
            coreir_module.add_metadata("verilog", json.dumps(verilog_metadata))
            coreir_defn = coreir_module.new_definition()
            coreir_module.definition = coreir_defn
            for instance in defn.instances:
                self.compile_inst(instance, coreir_defn)
            return coreir_module
        coreir_defn = coreir_module.new_definition()
        self.compile_defn_to_coreir_defn(defn, coreir_defn)
        coreir_module.definition = coreir_defn
        return coreir_module

    def compile_dependencies(self, defn):
        pass_ = InstanceGraphPass(defn)
        pass_.run()
        dependency_names = [key.name for key, _ in pass_.tsortedgraph]
        logger.debug(f"tsortedgraph: {dependency_names}")
        for key, _ in pass_.tsortedgraph:
            if key is defn or key.name in self.modules:
                continue
            compiled = self.compile_defn_or_decl(key)
            self.modules[key.name] = compiled

    def compile_defn_or_decl(self, defn_or_decl):
        if not defn_or_decl.is_definition:
            return self.compile_decl(defn_or_decl)
        self.compile_dependencies(defn_or_decl)
        wrapped = getattr(defn_or_decl, "wrappedModule", None)
        if wrapped and wrapped.context is self.context:
            self.libs_used |= defn_or_decl.coreir_wrapped_modules_libs_used
            return wrapped
        compiled = self.compile_defn(defn_or_decl)
        defn_or_decl.wrappedModule = compiled
        defn_or_decl.coreir_wrapped_modules_libs_used = copy(self.libs_used)
        return compiled

    def compile(self, defn_or_decl):
        logger.debug(f"Compiling: {defn_or_decl.name}")
        compiled = self.compile_defn_or_decl(defn_or_decl)
        self.modules[defn_or_decl.name] = compiled
        return self.modules


class InsertWrapCasts(DefinitionPass):
    def sim(self, value_store, state_store):
        input_val = value_store.get_value(getattr(self, "in"))
        value_store.set_value(self.out, input_val)

    def define_wrap(self, wrap_type, in_type, out_type):
        return m.DeclareCircuit(
            f'coreir_wrap{wrap_type}'.replace("(", "").replace(")", ""),
            "in", m.In(in_type), "out", m.Out(out_type),
            coreir_genargs={"type": wrap_type},
            coreir_name="wrap",
            coreir_lib="coreir",
            simulate=self.sim
        )

    def wrap_if_arst(self, port, definition):
        if isinstance(port, (ArrayType, TupleType)):
            for t in port:
                self.wrap_if_arst(t, definition)
        elif port.isinput():
            if isinstance(port, (AsyncResetType, AsyncResetNType)) or \
                    isinstance(port.value(), (AsyncResetType, AsyncResetNType)):
                value = port.value()
                print(port, value)
                if value is not None and not isinstance(type(value),
                                                        type(type(port))):
                    port.unwire(value)
                    if isinstance(port, (AsyncResetType, AsyncResetNType)):
                        inst = self.define_wrap(type(port).flip(), type(port),
                                                type(value))()
                    else:
                        inst = self.define_wrap(type(value).flip(), type(port),
                                                type(value))()
                    definition.place(inst)
                    getattr(inst, "in") <= value
                    m.wire(inst.out, port)

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


def compile(main, file_name=None, context=None, check_context_is_default=True):
    InsertWrapCasts(main).run()
    backend = CoreIRBackend(context, check_context_is_default)
    backend.compile(main)
    if file_name is not None:
        return backend.modules[main.coreir_name].save_to_file(file_name)
    else:
        return backend.modules[main.coreir_name]
