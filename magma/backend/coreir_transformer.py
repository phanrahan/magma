from abc import ABC, abstractmethod
from copy import copy
import json
import logging
import os
from ..array import Array
from ..clock import wiredefaultclock, wireclock
from coreir import Wireable
from .coreir_utils import (add_non_input_ports, attach_debug_info,
                           check_magma_interface, constant_to_value,
                           get_inst_args, get_module_of_inst,
                           is_clock_or_nested_clock, is_const,
                           magma_interface_to_coreir_module_type,
                           magma_port_to_coreir_port, make_cparams, map_genarg)
from ..interface import InterfaceKind
from ..is_definition import isdefinition
from ..logging import root_logger
from ..passes import InstanceGraphPass
from ..tuple import Tuple
from .util import get_codegen_debug_info


# NOTE(rsetaluri): We do not need to set the level of this logger since it has
# already been done in backend/coreir_.py.
_logger = root_logger().getChild("coreir_backend")


class TransformerBase(ABC):
    def __init__(self, backend):
        self.backend = backend
        self.ran = False
        self._children = None

    def run(self):
        if self.ran:
            raise RuntimeError("Can only run transformer once")
        self._children = self.children()
        for child in self._children:
            child.run()
        self.run_self()
        self.ran = True

    @abstractmethod
    def children(self):
        raise NotImplementedError()

    def run_self(self):
        pass


class LeafTransformer(TransformerBase):
    def children(self):
        return []


class DefnOrDeclTransformer(TransformerBase):
    def __init__(self, backend, defn_or_decl):
        super().__init__(backend)
        self.defn_or_decl = defn_or_decl
        self.coreir_module = None

    def children(self):
        if self.defn_or_decl.name in self.backend.modules:
            _logger.debug(f"{self.defn_or_decl} already compiled, skipping")
            self.coreir_module = self.backend.modules[self.defn_or_decl.name]
            return []
        if not isdefinition(self.defn_or_decl):
            return [DeclarationTransformer(self.backend, self.defn_or_decl)]
        wrapped = getattr(self.defn_or_decl, "wrappedModule", None)
        if wrapped and wrapped.context is self.backend.context:
            return [WrappedTransformer(self.backend, self.defn_or_decl)]
        return [DefinitionTransformer(self.backend, self.defn_or_decl)]

    def run_self(self):
        if self.coreir_module:
            return
        self.coreir_module = self._children[0].coreir_module
        self.backend.modules[self.defn_or_decl.name] = self.coreir_module
        if isdefinition(self.defn_or_decl):
            self.defn_or_decl.wrappedModule = self.coreir_module
            libs = copy(self.backend.libs_used)
            self.defn_or_decl.coreir_wrapped_modules_libs_used = libs


class InstanceTransformer(LeafTransformer):
    def __init__(self, backend, inst, defn, wire_clocks=True):
        super().__init__(backend)
        self.inst = inst
        self.defn = defn
        self.wire_clocks = wire_clocks
        self.coreir_inst_gen = None

    def run_self(self):
        self.coreir_inst_gen = self.run_self_impl()

    def run_self_impl(self):
        _logger.debug(f"Compiling instance {(self.inst.name, type(self.inst))}")
        if self.wire_clocks:
            wiredefaultclock(self.defn, self.inst)
            wireclock(self.defn, self.inst)
        defn = type(self.inst)
        lib = self.backend.libs[self.inst.coreir_lib]
        if self.inst.coreir_genargs is None:
            module = get_module_of_inst(self.backend.context, self.inst, lib)
            args = get_inst_args(self.inst)
            args = self.backend.context.new_values(args)
            return lambda m: m.add_module_instance(self.inst.name, module, args)
        generator = lib.generators[defn.coreir_name]
        config_args = {k: v for k, v in self.inst.coreir_configargs.items()}
        config_args = self.backend.context.new_values(config_args)
        gen_args = {k: map_genarg(self.backend.context, v)
                    for k, v in defn.coreir_genargs.items()}
        gen_args = self.backend.context.new_values(gen_args)
        return lambda m: m.add_generator_instance(
            self.inst.name, generator, gen_args, config_args)


class WrappedTransformer(LeafTransformer):
    def __init__(self, backend, defn):
        super().__init__(backend)
        self.defn = defn
        self.coreir_module = self.defn.wrappedModule
        self.backend.libs_used |= self.defn.coreir_wrapped_modules_libs_used


class DefinitionTransformer(TransformerBase):
    def __init__(self, backend, defn):
        super().__init__(backend)
        self.defn = defn
        self.coreir_module = None
        self.decl_tx = DeclarationTransformer(self.backend, self.defn)
        self.inst_txs = {
            inst: InstanceTransformer(self.backend, inst, self.defn)
            for inst in self.defn.instances
        }

    def children(self):
        pass_ = InstanceGraphPass(self.defn)
        pass_.run()
        deps = [k for k, _ in pass_.tsortedgraph if k is not self.defn]
        children = [DefnOrDeclTransformer(self.backend, dep) for dep in deps]
        children += [self.decl_tx]
        children += self.inst_txs.values()
        return children

    def run_self(self):
        _logger.debug(f"Compiling definition {self.defn}")
        self.coreir_module = self.decl_tx.coreir_module
        if self.defn.inline_verilog_strs:
            inline_verilog = "\n\n".join(self.defn.inline_verilog_strs)
            self.coreir_module.add_metadata("inline_verilog",
                                            json.dumps(inline_verilog))
        for name, module in self.defn.bind_modules.items():
            self.backend.sv_bind_files[name] = module

        self.coreir_module.definition = self.get_coreir_defn()

    def get_coreir_defn(self):
        coreir_defn = self.coreir_module.new_definition()
        coreir_insts = {inst: self.inst_txs[inst].coreir_inst_gen(coreir_defn)
                        for inst in self.defn.instances}
        # If this module was imported from verilog, do not go through the
        # general module construction flow. Instead just attach the verilog
        # source as metadata and return the module.
        if hasattr(self.defn, "verilogFile") and self.defn.verilogFile:
            metadata = json.dumps({"verilog_string": self.defn.verilogFile})
            self.coreir_module.add_metadata("verilog", metadata)
            return coreir_defn
        if self.defn.coreir_lib is not None:
            self.backend.libs_used.add(self.defn.coreir_lib)
        non_input_ports = {}
        for name, port in self.defn.interface.ports.items():
            _logger.debug(f"{name}, {port}, {port.is_output()}")
            add_non_input_ports(non_input_ports, port)
        for inst, coreir_inst in coreir_insts.items():
            if get_codegen_debug_info() and getattr(inst, "debug_info", False):
                attach_debug_info(coreir_inst, inst.debug_info)
            for name, port in inst.interface.ports.items():
                add_non_input_ports(non_input_ports, port)
        for inst in coreir_insts:
            for name, port in inst.interface.ports.items():
                self.connect_non_outputs(coreir_defn, port, non_input_ports)
        for port in self.defn.interface.ports.values():
            self.connect_non_outputs(coreir_defn, port, non_input_ports)
        return coreir_defn

    def connect_non_outputs(self, module_defn, port, non_input_ports):
        # Recurse into non input types that may contain inout children.
        if isinstance(port, Tuple) and not port.is_input() or \
           isinstance(port, Array) and not port.T.is_input():
            for elem in port:
                self.connect_non_outputs(module_defn, elem, non_input_ports)
        elif not port.is_output():
            self.connect(module_defn, port, port.trace(), non_input_ports)

    def connect(self, module_defn, port, value, non_input_ports):
        # Allow Clock or Array[Clock] to be unwired as CoreIR can wire them up.
        if value is None and is_clock_or_nested_clock(type(port)):
            return
        if value is None:
            if port.is_inout():
                return  # skip inouts because they might be conn. as an input.
            if getattr(self.defn, "_ignore_undriven_", False):
                return
            raise Exception(f"Found unconnected port: {port.debug_name}")

        def get_source():
            if isinstance(value, Wireable):
                return value
            if isinstance(value, Array) and is_const(value):
                return self.const_instance(value, len(value), module_defn)
            if value.anon() and isinstance(value, Array):
                for p, v in zip(port, value):
                    self.connect(module_defn, p, v, non_input_ports)
                return None
            if isinstance(value, Tuple) and value.anon():
                for p, v in zip(port, value):
                    self.connect(module_defn, p, v, non_input_ports)
                return None
            if value.const():
                return self.const_instance(value, None, module_defn)
            return module_defn.select(non_input_ports[value])
        source = get_source()
        if not source:
            return
        sink = module_defn.select(magma_port_to_coreir_port(port))
        module_defn.connect(source, sink)
        if get_codegen_debug_info() and getattr(port, "debug_info", False):
            attach_debug_info(module_defn, port.debug_info, source, sink)

    def const_instance(self, constant, num_bits, module_defn):
        cache_entry = self.backend.constant_cache.setdefault(module_defn, {})
        value = constant_to_value(constant)
        key = (value, num_bits)
        if key in cache_entry:
            return cache_entry[key]
        if num_bits is None:
            config = self.backend.context.new_values({"value": bool(value)})
            name = f"bit_const_{value}_{num_bits}"
            mod = self.backend.libs["corebit"].modules["const"]
            module_defn.add_module_instance(name, mod, config)
        else:
            config = self.backend.context.new_values({"value": value})
            name = f"const_{value}_{num_bits}"
            gen = self.backend.libs["coreir"].generators["const"]
            gen_args = self.backend.context.new_values({"width": num_bits})
            module_defn.add_generator_instance(name, gen, gen_args, config)
        cache_entry[key] = module_defn.select(f"{name}.out")
        return cache_entry[key]


class DeclarationTransformer(LeafTransformer):
    def __init__(self, backend, decl):
        super().__init__(backend)
        self.decl = decl
        self.coreir_module = None

    def run_self(self):
        self.coreir_module = self.run_self_impl()

    def run_self_impl(self):
        self.decl = self.decl
        _logger.debug(f"Compiling declaration {self.decl}")
        if self.decl.coreir_lib is not None:
            self.backend.libs_used.add(self.decl.coreir_lib)
        # These libraries are already available by default in coreir, so we
        # don't need declarations.
        if self.decl.coreir_lib in ["coreir", "corebit", "commonlib"]:
            lib = self.backend.libs[self.decl.coreir_lib]
            if self.decl.coreir_genargs is None:
                return lib.modules[self.decl.coreir_name]
            return lib.generators[self.decl.coreir_name]
        if self.decl.name in self.backend.modules:
            _logger.debug(f"{self.decl} already compiled, skipping")
            return self.backend.modules[self.decl.name]
        check_magma_interface(self.decl.interface)
        module_type = magma_interface_to_coreir_module_type(
            self.backend.context, self.decl.interface)
        if isinstance(self.decl.interface, InterfaceKind):
            module_type = self.backend.context.Flip(module_type)
        kwargs = {}
        if hasattr(self.decl, "coreir_config_param_types"):
            param_types = self.decl.coreir_config_param_types
            kwargs["cparams"] = make_cparams(self.backend.context, param_types)
        coreir_module = self.backend.context.global_namespace.new_module(
            self.decl.coreir_name, module_type, **kwargs)
        if get_codegen_debug_info() and self.decl.debug_info:
            attach_debug_info(coreir_module, self.decl.debug_info)
        return coreir_module
