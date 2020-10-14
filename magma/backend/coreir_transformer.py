from abc import ABC, abstractmethod
from copy import copy
import json
import logging
import os
from ..digital import Digital
from ..array import Array
from ..bits import Bits
from coreir import Wireable
from .coreir_utils import (attach_debug_info, check_magma_interface,
                           constant_to_value, get_inst_args,
                           get_module_of_inst,
                           magma_interface_to_coreir_module_type,
                           magma_port_to_coreir_port, make_cparams, map_genarg,
                           magma_name_to_coreir_select, Slice)
from ..interface import InterfaceKind
from ..is_definition import isdefinition
from ..logging import root_logger
from ..passes import InstanceGraphPass
from ..tuple import Tuple
from .util import get_codegen_debug_info
from magma.clock import (wire_default_clock, is_clock_or_nested_clock,
                         get_default_clocks)
from magma.config import get_debug_mode
from magma.protocol_type import MagmaProtocol, MagmaProtocolMeta
from magma.ref import PortViewRef, ArrayRef


# NOTE(rsetaluri): We do not need to set the level of this logger since it has
# already been done in backend/coreir_.py.
_logger = root_logger().getChild("coreir_backend")


def _make_unconnected_error_str(port):
    error_str = port.debug_name
    if port.trace() is not None:
        error_str += ": Connected"
    elif isinstance(port, (Tuple, Array)):
        child_str = ""
        for child in port:
            child = _make_unconnected_error_str(child)
            child = "\n    ".join(child.splitlines())
            child_str += f"\n    {child}"
        if "Connected" not in child_str:
            # Handle case when no children are connected (simplify)
            error_str += ": Unconnected"
        else:
            error_str += child_str
    elif port.trace() is None:
        error_str += ": Unconnected"
    return error_str


def _collect_drivers(value):
    """
    Iterate over value to collect the child drivers, packing slices together
    """
    drivers = []
    start_idx = 0
    for i in range(1, len(value)):
        # If the next value item is not a reference to an array of bits where
        # the array matches the previous item and the index is incremented by
        # one, append the current slice to drivers (may introduce slices of
        # length 1)
        if not (
            isinstance(value[i].name, ArrayRef) and
            issubclass(value[i].name.array.T, Digital) and
            isinstance(value[i - 1].name, ArrayRef) and
            value[i].name.array is value[i - 1].name.array and
            value[i].name.index == value[i - 1].name.index + 1
        ):
            drivers.append(value[start_idx:i])
            start_idx = i
    drivers.append(value[start_idx:])
    return drivers


def _unwrap(x):
    if isinstance(x, MagmaProtocol):
        return x._get_magma_value_()
    if isinstance(x, MagmaProtocolMeta):
        return x._to_magma_()
    return x


class TransformerBase(ABC):
    def __init__(self, backend, opts):
        self.backend = backend
        self.opts = opts
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
    def __init__(self, backend, opts, defn_or_decl):
        super().__init__(backend, opts)
        self.defn_or_decl = defn_or_decl
        self.coreir_module = None

    def children(self):
        if self.defn_or_decl.name in self.backend.modules:
            _logger.debug(f"{self.defn_or_decl} already compiled, skipping")
            self.coreir_module = self.backend.modules[self.defn_or_decl.name]
            return []
        if not isdefinition(self.defn_or_decl):
            return [DeclarationTransformer(self.backend,
                                           self.opts,
                                           self.defn_or_decl)]
        wrapped = getattr(self.defn_or_decl, "wrappedModule", None)
        if wrapped and wrapped.context is self.backend.context:
            return [WrappedTransformer(self.backend,
                                       self.opts,
                                       self.defn_or_decl)]
        return [DefinitionTransformer(self.backend,
                                      self.opts,
                                      self.defn_or_decl)]

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
    def __init__(self, backend, opts, inst, defn):
        super().__init__(backend, opts)
        self.inst = inst
        self.defn = defn
        self.coreir_inst_gen = None

    def run_self(self):
        self.coreir_inst_gen = self.run_self_impl()

    def run_self_impl(self):
        _logger.debug(
            f"Compiling instance {(self.inst.name, type(self.inst).name)}"
        )
        defn = type(self.inst)
        if hasattr(self.inst, "namespace"):
            lib = self.backend.libs[self.inst.namespace]
        else:
            lib = self.backend.libs[self.inst.coreir_lib]
            if self.inst.coreir_lib == "global":
                lib = self.opts.get("user_namespace", lib)
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
    def __init__(self, backend, opts, defn):
        super().__init__(backend, opts)
        self.defn = defn
        self.coreir_module = self.defn.wrappedModule
        self.backend.libs_used |= self.defn.coreir_wrapped_modules_libs_used


class DefinitionTransformer(TransformerBase):
    def __init__(self, backend, opts, defn):
        super().__init__(backend, opts)
        self.defn = defn
        self.coreir_module = None
        self.decl_tx = DeclarationTransformer(self.backend,
                                              self.opts,
                                              self.defn)
        self.inst_txs = {
            inst: InstanceTransformer(self.backend, self.opts, inst, self.defn)
            for inst in self.defn.instances
        }
        self.clocks = get_default_clocks(defn)

    def children(self):
        pass_ = InstanceGraphPass(self.defn)
        pass_.run()
        deps = [k for k, _ in pass_.tsortedgraph if k is not self.defn]
        children = [DefnOrDeclTransformer(self.backend, self.opts, dep)
                    for dep in deps]
        children += [self.decl_tx]
        children += self.inst_txs.values()
        return children

    def run_self(self):
        _logger.debug(f"Compiling definition {self.defn}")
        self.coreir_module = self.decl_tx.coreir_module
        if self.defn.inline_verilog_strs:
            inline_verilog = "\n\n".join(x[0] for x in
                                         self.defn.inline_verilog_strs)
            connect_references = {}
            for _, inline_value_map in self.defn.inline_verilog_strs:
                for key, value in inline_value_map.items():
                    connect_references[key] = magma_port_to_coreir_port(value)
            self.coreir_module.add_metadata("inline_verilog", json.dumps(
                {"str": inline_verilog,
                 "connect_references": connect_references}
            ))
        for name, module in self.defn.compiled_bind_modules.items():
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
        for name, port in self.defn.interface.ports.items():
            _logger.debug(f"{name}, {port}, {port.is_output()}")
        for inst, coreir_inst in coreir_insts.items():
            if get_codegen_debug_info() and getattr(inst, "debug_info", False):
                attach_debug_info(coreir_inst, inst.debug_info)
        for inst in coreir_insts:
            for name, port in inst.interface.ports.items():
                self.connect_non_outputs(coreir_defn, port)
        for port in self.defn.interface.ports.values():
            self.connect_non_outputs(coreir_defn, port)
        return coreir_defn

    def connect_non_outputs(self, module_defn, port):
        # Recurse into non input types that may contain inout children.
        if isinstance(port, Tuple) and not port.is_input() or \
           isinstance(port, Array) and not port.T.is_input():
            for elem in port:
                self.connect_non_outputs(module_defn, elem)
        elif not port.is_output():
            self.connect(module_defn, port, port.trace())

    def get_source(self, port, value, module_defn):
        port = _unwrap(port)
        value = _unwrap(value)
        if isinstance(value, Wireable):
            return value
        if isinstance(value, Slice):
            return module_defn.select(value.get_coreir_select())
        if isinstance(value, Bits) and value.const():
            return self.const_instance(value, len(value), module_defn)
        if value.anon() and isinstance(value, Array):
            drivers = _collect_drivers(value)
            offset = 0
            for d in drivers:
                d = _unwrap(d)
                if len(d) == 1:
                    # _collect_drivers will introduce a slice of length 1 for
                    # non-slices, so we index them here with 0 to unpack the
                    # extra array dimension
                    self.connect(module_defn, port[offset], d[0])
                else:
                    self.connect(module_defn,
                                 Slice(port, offset, offset + len(d)),
                                 Slice(d[0].name.array, d[0].name.index,
                                       d[-1].name.index + 1))
                offset += len(d)

            return None
        if isinstance(value, Tuple) and value.anon():
            for p, v in zip(port, value):
                self.connect(module_defn, p, v)
            return None
        if value.const():
            return self.const_instance(value, None, module_defn)
        if isinstance(value.name, PortViewRef):
            return module_defn.select(
                magma_name_to_coreir_select(value.name))
        return module_defn.select(magma_port_to_coreir_port(value))

    def connect(self, module_defn, port, value):
        if value is None and is_clock_or_nested_clock(type(port)):
            if not wire_default_clock(port, self.clocks):
                # No default clock
                return
            value = port.trace()
        if value is None:
            if port.is_inout():
                return  # skip inouts because they might be conn. as an input.
            if getattr(self.defn, "_ignore_undriven_", False):
                return
            error_str = f"Found unconnected port: {port.debug_name}\n"
            error_str += _make_unconnected_error_str(port)
            raise Exception(error_str)
        source = self.get_source(port, value, module_defn)
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
    def __init__(self, backend, opts, decl):
        super().__init__(backend, opts)
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
        if self.decl.coreir_lib in ["coreir", "corebit", "commonlib",
                                    "memory"]:
            lib = self.backend.libs[self.decl.coreir_lib]
            if self.decl.coreir_genargs is None:
                return lib.modules[self.decl.coreir_name]
            return lib.generators[self.decl.coreir_name]
        if self.decl.name in self.backend.modules:
            _logger.debug(f"{self.decl} already compiled, skipping")
            return self.backend.modules[self.decl.name]
        if get_debug_mode():
            check_magma_interface(self.decl.interface)
        module_type = magma_interface_to_coreir_module_type(
            self.backend.context, self.decl.interface)
        if isinstance(self.decl.interface, InterfaceKind):
            module_type = self.backend.context.Flip(module_type)
        kwargs = {}
        if hasattr(self.decl, "coreir_config_param_types"):
            param_types = self.decl.coreir_config_param_types
            kwargs["cparams"] = make_cparams(self.backend.context, param_types)
        if hasattr(self.decl, "namespace"):
            # Allows users to choose namespace explicitly with
            # class MyCircuit(m.Circuit):
            #     namespace = "foo"
            # overrides user_namespace setting
            namespace = self.backend.libs[self.decl.namespace]
        else:
            namespace = self.opts.get("user_namespace",
                                      self.backend.context.global_namespace)
        coreir_module = namespace.new_module(
            self.decl.coreir_name, module_type, **kwargs)
        if get_codegen_debug_info() and self.decl.debug_info:
            attach_debug_info(coreir_module, self.decl.debug_info)
        for key, value in self.decl.coreir_metadata.items():
            coreir_module.add_metadata(key, json.dumps(value))
        return coreir_module
