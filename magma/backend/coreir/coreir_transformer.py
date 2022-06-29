from abc import ABC, abstractmethod
import json

import coreir as pycoreir

from magma.digital import Digital
from magma.array import Array
from magma.backend.check_wiring_context import check_wiring_context
from magma.backend.coreir.coreir_utils import (
    attach_debug_info, check_magma_interface, constant_to_value, get_inst_args,
    get_module_of_inst, magma_interface_to_coreir_module_type,
    magma_port_to_coreir_port, make_cparams, map_genarg,
    magma_name_to_coreir_select, Slice)
from magma.compile_exception import UnconnectedPortException
from magma.inline_verilog_expression import InlineVerilogExpression
from magma.interface import InterfaceKind
from magma.is_definition import isdefinition
from magma.linking import (
    get_linked_modules, has_default_linked_module, get_default_linked_module)
from magma.logging import root_logger
from magma.passes import dependencies
from magma.tuple import Tuple
from magma.backend.util import get_codegen_debug_info
from magma.clock import is_clock_or_nested_clock
from magma.passes.clock import (
    drive_all_undriven_clocks_in_value, get_all_output_clocks_in_defn)
from magma.config import get_debug_mode
from magma.protocol_type import MagmaProtocol, MagmaProtocolMeta
from magma.ref import PortViewRef, ArrayRef
from magma.symbol_table import SYMBOL_TABLE_EMPTY


# NOTE(rsetaluri): We do not need to set the level of this logger since it has
# already been done in backend/coreir/coreir_backend.py.
_logger = root_logger().getChild("coreir_backend")


_generator_callbacks = {}


def _is_generator(ckt_or_inst):
    return ckt_or_inst.coreir_genargs is not None


def _coreir_longname(magma_defn_or_decl, coreir_module_or_generator):
    # NOTE(rsetaluri): This is a proxy to exposing a pycoreir/coreir-c API to
    # get a module's longname. This logic should be identical right now. Another
    # caveat is that we don't elaborate the CoreIR generator at the magma level,
    # so it's longname needs to be dynamically reconstructed anyway.
    namespace = coreir_module_or_generator.namespace.name
    prefix = "" if namespace == "global" else f"{namespace}_"
    longname = prefix + coreir_module_or_generator.name
    if isinstance(coreir_module_or_generator, pycoreir.Module):
        return longname
    assert isinstance(coreir_module_or_generator, pycoreir.Generator)
    param_keys = coreir_module_or_generator.params.keys()
    for k in param_keys:
        v = magma_defn_or_decl.coreir_genargs[k]
        longname += f"__{k}{v}"
    return longname


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
            value[i].name.anon() or
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
    __MISSING = object()

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

    def get_opt(self, key, default=__MISSING):
        if default is TransformerBase.__MISSING:
            return self.opts[key]
        return self.opts.get(key, default)


class LeafTransformer(TransformerBase):
    def children(self):
        return []


class DefnOrDeclTransformer(TransformerBase):
    def __init__(self, backend, opts, defn_or_decl):
        super().__init__(backend, opts)
        self.defn_or_decl = defn_or_decl
        self.coreir_module = None

    def children(self):
        if _is_generator(self.defn_or_decl):
            return [GeneratorTransformer(
                self.backend, self.opts, self.defn_or_decl)]
        try:
            coreir_module = self.backend.get_module(self.defn_or_decl)
            _logger.debug(f"{self.defn_or_decl} already compiled, skipping")
            self.coreir_module = coreir_module
            return []
        except KeyError:
            pass
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
        self._run_self_impl()
        self._generate_symbols()
        self._link_default_module()
        self._link_modules()

    def _link_default_module(self):
        if not has_default_linked_module(self.defn_or_decl):
            return
        target = get_default_linked_module(self.defn_or_decl)
        target = self.backend.get_module(target)
        self.coreir_module.link_default_module(target)

    def _link_modules(self):
        targets = get_linked_modules(self.defn_or_decl)
        for key, target in targets.items():
            target = self.backend.get_module(target)
            self.coreir_module.link_module(key, target)

    def _generate_symbols(self):
        if not self.get_opt("generate_symbols", False):
            return
        out_module_name = _coreir_longname(
            self.defn_or_decl, self.coreir_module)
        self.opts.get("symbol_table").set_module_name(
            self.defn_or_decl.name, out_module_name)

    def _run_self_impl(self):
        if self.coreir_module:
            return
        self.coreir_module = self._children[0].coreir_module
        self.backend.add_module(self.defn_or_decl, self.coreir_module)
        if isdefinition(self.defn_or_decl):
            self.defn_or_decl.wrappedModule = self.coreir_module
            libs = self.backend.included_libs()
            self.defn_or_decl.coreir_wrapped_modules_libs_used = libs


class GeneratorTransformer(TransformerBase):
    def __init__(self, backend, opts, defn_or_decl):
        super().__init__(backend, opts)
        self.defn_or_decl = defn_or_decl
        self.coreir_module = None

    def children(self):
        try:
            coreir_module = self.backend.get_module(self.defn_or_decl)
            _logger.debug(f"{self.defn_or_decl} already compiled, skipping")
            self.coreir_module = coreir_module
            return []
        except KeyError:
            pass
        assert not isdefinition(self.defn_or_decl)
        return [DeclarationTransformer(self.backend,
                                       self.opts,
                                       self.defn_or_decl)]

    def run_self(self):
        self._generate_symbols()
        if self.coreir_module is not None:
            return
        self.coreir_module = self._children[0].coreir_module

    def _generate_symbols(self):
        if not self.get_opt("generate_symbols", False):
            return
        global _generator_callbacks

        def _callback(coreir_inst):
            magma_names = list(self.defn_or_decl.interface.ports.keys())
            coreir_names = list(k for k, _ in coreir_inst.module.type.items())
            assert len(magma_names) == len(coreir_names)
            for magma_name, coreir_name in zip(magma_names, coreir_names):
                self.opts.get("symbol_table").set_port_name(
                    self.defn_or_decl.name, magma_name, coreir_name)

        assert self.defn_or_decl not in _generator_callbacks
        _generator_callbacks[self.defn_or_decl] = _callback


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
            lib = self.backend.get_lib(self.inst.namespace)
        else:
            lib = self.backend.get_lib(self.inst.coreir_lib)
            if self.inst.coreir_lib == "global":
                lib = self.get_opt("user_namespace", lib)
        if not _is_generator(self.inst):
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
        self.backend.include_lib_or_libs(
            self.defn.coreir_wrapped_modules_libs_used)


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
        self.clocks = get_all_output_clocks_in_defn(defn)
        self._constant_cache = {}

    def children(self):
        children = []
        if not self.get_opt("skip_instance_graph", False):
            deps = dependencies(self.defn, include_self=False)
            opts = self.opts.copy()
            opts.update({"skip_instance_graph": True})
            children += [DefnOrDeclTransformer(self.backend, opts, dep)
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
            self.backend.bind_module(name, module)

        self.coreir_module.definition = self.get_coreir_defn()

    def _generate_symbols(self, coreir_insts):
        if not self.get_opt("generate_symbols", False):
            return
        for inst, coreir_inst in coreir_insts.items():
            self.get_opt("symbol_table").set_instance_name(
                self.defn.name, inst.name,
                (SYMBOL_TABLE_EMPTY, coreir_inst.name))
            self.get_opt("symbol_table").set_instance_type(
                self.defn.name, inst.name, type(inst).name)

    def get_coreir_defn(self):
        coreir_defn = self.coreir_module.new_definition()
        coreir_insts = {inst: self.inst_txs[inst].coreir_inst_gen(coreir_defn)
                        for inst in self.defn.instances}
        # Call generator callback if necessary.
        global _generator_callbacks
        for inst, coreir_inst in coreir_insts.items():
            try:
                callback = _generator_callbacks.pop(type(inst))
            except KeyError:
                continue
            callback(coreir_inst)
        self._generate_symbols(coreir_insts)
        # If this module was imported from verilog, do not go through the
        # general module construction flow. Instead just attach the verilog
        # source as metadata and return the module.
        if hasattr(self.defn, "verilogFile") and self.defn.verilogFile:
            metadata = json.dumps({"verilog_string": self.defn.verilogFile})
            self.coreir_module.add_metadata("verilog", metadata)
            return coreir_defn
        if hasattr(self.defn, "verilog") and self.defn.verilog:
            metadata = json.dumps({"verilog_body": self.defn.verilog})
            self.coreir_module.add_metadata("verilog", metadata)
            return coreir_defn
        if self.defn.coreir_lib is not None:
            self.backend.include_lib_or_libs(self.defn.coreir_lib)
        for name, port in self.defn.interface.ports.items():
            _logger.debug(f"{name}, {port}, {port.is_output()}")
        for inst, coreir_inst in coreir_insts.items():
            if get_codegen_debug_info() and getattr(inst, "debug_info", False):
                attach_debug_info(coreir_inst, inst.debug_info)
            if getattr(inst, "coreir_metadata"):
                for k, v in inst.coreir_metadata.items():
                    coreir_inst.add_metadata(k, json.dumps(v))
        for inst in coreir_insts:
            for name, port in inst.interface.ports.items():
                self.connect_non_outputs(coreir_defn, port)
        for port in self.defn.interface.ports.values():
            self.connect_non_outputs(coreir_defn, port)
        return coreir_defn

    def connect_non_outputs(self, module_defn, port):
        # Recurse into non input types that may contain inout children.
        if isinstance(port, Tuple) and not port.is_input() or \
           (isinstance(port, Array) and not port.T.is_input() and
                not port.T.is_output()):
            for elem in port:
                self.connect_non_outputs(module_defn, elem)
        elif not port.is_output():
            self.connect(module_defn, port, port.trace())

    def get_source(self, port, value, module_defn):
        port = _unwrap(port)
        value = _unwrap(value)
        if isinstance(value, pycoreir.Wireable):
            return value
        if isinstance(value, Slice):
            return module_defn.select(value.get_coreir_select())
        if isinstance(value, (Tuple, Array)) and value.anon():
            # anon values are not bulk connected, so we recurse
            for sink, source in port.connection_iter(only_slice_bits=True):
                self.connect(module_defn, sink, source)
            return None
        if value.const():
            if isinstance(value, Digital):
                n = None
            else:
                assert isinstance(value, Array)
                n = len(value)
            return self._const_instance(value, n, module_defn)
        if isinstance(value.name, PortViewRef):
            return module_defn.select(
                magma_name_to_coreir_select(value.name))
        if (isinstance(value, Array) and isinstance(value.name, ArrayRef) and
                isinstance(value.name.index, slice) and
                not issubclass(value.T, Digital)):
            for p, v in zip(port, value):
                self.connect(module_defn, p, v)
            return None
        return module_defn.select(magma_port_to_coreir_port(value))

    def connect(self, module_defn, port, value):
        if value is None and is_clock_or_nested_clock(type(port)):
            with self.defn.open():
                if not drive_all_undriven_clocks_in_value(port, self.clocks):
                    # No default clock
                    raise UnconnectedPortException(port)
            value = port.trace()
        if value is None:
            if port.is_inout():
                return  # skip inouts because they might be conn. as an input.
            if getattr(self.defn, "_ignore_undriven_", False):
                return
            raise UnconnectedPortException(port)
        check_wiring_context(port, value)
        source = self.get_source(port, value, module_defn)
        if not source:
            return
        sink = module_defn.select(magma_port_to_coreir_port(port))
        module_defn.connect(source, sink)
        if get_codegen_debug_info() and getattr(port, "debug_info", False):
            attach_debug_info(module_defn, port.debug_info, source, sink)

    def _const_instance(self, constant, num_bits, module_defn):
        value = constant_to_value(constant)
        key = (value, num_bits)
        try:
            return self._constant_cache[key]
        except KeyError:
            pass
        if num_bits is None:
            config = self.backend.context.new_values({"value": bool(value)})
            name = f"bit_const_{value}_{num_bits}"
            mod = self.backend.get_lib("corebit").modules["const"]
            module_defn.add_module_instance(name, mod, config)
        else:
            config = self.backend.context.new_values({"value": value})
            name = f"const_{value}_{num_bits}"
            gen = self.backend.get_lib("coreir").generators["const"]
            gen_args = self.backend.context.new_values({"width": num_bits})
            module_defn.add_generator_instance(name, gen, gen_args, config)
        out = module_defn.select(f"{name}.out")
        return self._constant_cache.setdefault(key, out)


class DeclarationTransformer(LeafTransformer):
    def __init__(self, backend, opts, decl):
        super().__init__(backend, opts)
        self.decl = decl
        self.coreir_module = None

    def run_self(self):
        self.coreir_module = self._run_self_impl()
        self._generate_symbols()

    def _generate_symbols(self):
        if not self.get_opt("generate_symbols", False):
            return
        if _is_generator(self.decl):
            return
        magma_names = list(self.decl.interface.ports.keys())
        coreir_names = list(k for k, _ in self.coreir_module.type.items())
        assert len(magma_names) == len(coreir_names)
        for magma_name, coreir_name in zip(magma_names, coreir_names):
            self.opts.get("symbol_table").set_port_name(
                self.decl.name, magma_name, coreir_name)

    def _run_self_impl(self):
        _logger.debug(f"Compiling declaration {self.decl}")
        if isinstance(self.decl, InlineVerilogExpression):
            raise NotImplementedError(
                "Can not compile InlineVerilogExpression generator to CoreIR"
            )
        if self.decl.coreir_lib is not None:
            self.backend.include_lib_or_libs(self.decl.coreir_lib)
        # These libraries are already available by default in coreir, so we
        # don't need declarations.
        if self.decl.coreir_lib in ["coreir", "corebit", "commonlib",
                                    "memory"]:
            lib = self.backend.get_lib(self.decl.coreir_lib)
            if not _is_generator(self.decl):
                return lib.modules[self.decl.coreir_name]
            return lib.generators[self.decl.coreir_name]
        try:
            coreir_module = self.backend.get_module(self.decl)
            _logger.debug(f"{self.decl} already compiled, skipping")
            return coreir_module
        except KeyError:
            pass
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
            namespace = self.backend.get_lib(self.decl.namespace)
        else:
            namespace = self.get_opt("user_namespace",
                                     self.backend.context.global_namespace)
        coreir_module = namespace.new_module(
            self.decl.coreir_name, module_type, **kwargs)
        if get_codegen_debug_info() and self.decl.debug_info:
            attach_debug_info(coreir_module, self.decl.debug_info)
        for key, value in self.decl.coreir_metadata.items():
            coreir_module.add_metadata(key, json.dumps(value))
        return coreir_module
