import dataclasses
import functools
import io
import sys
from typing import Any, List, Optional, Tuple, Union

import magma as m

from build_magma_graph import build_magma_graph
from builtin import builtin
from comb import comb
from common import wrap_with_not_implemented_error
from graph_lib import Graph
from hw import hw
from magma_common import (
    ModuleLike as MagmaModuleLike,
    value_or_type_to_string as magma_value_or_type_to_string,
    visit_value_by_direction as visit_magma_value_by_direction)
from magma_ops import (
    MagmaArrayGetOp, MagmaArrayCreateOp,
    MagmaProductGetOp, MagmaProductCreateOp,
    MagmaBitConstantOp, MagmaBitsConstantOp)
from mlir_name_generator import MlirNameGenerator
from mlir import push_block
from mlir import MlirValue
from mlir import MlirType
from printer_base import PrinterBase
from sv import sv


class ModuleContext:
    def __init__(self):
        self._name_gen = MlirNameGenerator()
        self._value_map = {}

    def get_mapped_value(self, port: m.Type) -> MlirValue:
        return self._value_map[port]

    def get_or_make_mapped_value(self, port: m.Type, **kwargs) -> MlirValue:
        try:
            return self._value_map[port]
        except KeyError:
            pass
        self._value_map[port] = value = self.new_value(port, **kwargs)
        return value

    def set_mapped_value(self, port: m.Type, value: MlirValue):
        if port in self._value_map:
            raise ValueError(f"Port {port} already mapped")
        self._value_map[port] = value

    def new_value(
            self, value_or_type: Union[m.Type, m.Kind, MlirType],
            **kwargs) -> MlirValue:
        if isinstance(value_or_type, m.Type):
            mlir_type = magma_type_to_mlir_type(type(value_or_type))
        elif isinstance(value_or_type, m.Kind):
            mlir_type = magma_type_to_mlir_type(value_or_type)
        elif isinstance(value_or_type, MlirType):
            mlir_type = value_or_type
        else:
            raise TypeError(value_or_type)
        name = self._name_gen(**kwargs)
        return MlirValue(mlir_type, name)


@wrap_with_not_implemented_error
def parse_reset_type(T: m.Kind) -> Tuple[str, str]:
     if T is m.Reset:
         return "syncreset", "posedge"
     if T is m.ResetN:
         return "syncreset", "negedge"
     if T is m.AsyncReset:
         return "asyncreset", "posedge"
     if T is m.AsyncResetN:
         return "asyncreset", "negedge"


@wrap_with_not_implemented_error
@functools.lru_cache()
def magma_type_to_mlir_type(type: m.Kind) -> MlirType:
    type = type.undirected_t
    if issubclass(type, m.Digital):
        return builtin.IntegerType(1)
    if issubclass(type, m.Bits):
        return builtin.IntegerType(type.N)
    if issubclass(type, m.Array):
        if issubclass(type.T, m.Bit):
            return magma_type_to_mlir_type(m.Bits[type.N])
        return hw.ArrayType((type.N,), magma_type_to_mlir_type(type.T))
    if issubclass(type, m.Product):
        fields = {k: magma_type_to_mlir_type(t)
                  for k, t in type.field_dict.items()}
        return hw.StructType(tuple(fields.items()))


def get_module_interface(
        module, ctx: ModuleContext) -> Tuple[List[MlirValue], List[MlirValue]]:
    operands = []
    results = []
    for port in module.interface.ports.values():
        visit_magma_value_by_direction(
            port,
            lambda p: operands.append(ctx.get_or_make_mapped_value(p)),
            lambda p: results.append(ctx.get_or_make_mapped_value(p))
        )
    return operands, results


@dataclasses.dataclass(frozen=True)
class ModuleWrapper:
    module: MagmaModuleLike
    operands: List[MlirValue]
    results: List[MlirValue]

    @staticmethod
    def make(module: MagmaModuleLike, ctx: ModuleContext) -> 'ModuleWrapper':
        operands, results = get_module_interface(module, ctx)
        return ModuleWrapper(module, operands, results)


class ModuleVisitor:
    def __init__(self, graph: Graph, ctx: ModuleContext):
        self._graph = graph
        self._ctx = ctx
        self._visited = set()

    def make_constant(self, T: m.Kind, value: Any) -> MlirValue:
        result = self._ctx.new_value(T)
        if isinstance(T, (m.DigitalMeta, m.BitsMeta)):
            hw.ConstantOp(value=int(value), results=[result])
            return result
        if isinstance(T, m.ArrayMeta):
            operands = [self.make_constant(T.T, v) for v in value]
            hw.ArrayCreateOp(operands=operands, results=[result])
            return result
        if isinstance(T, m.ProductMeta):
            fields = T.field_dict.items()
            operands = [self.make_constant(t, value[k]) for k, t in fields]
            hw.StructCreateOp(operands=operands, results=[result])
            return result
        raise TypeError(T)

    @wrap_with_not_implemented_error
    def visit_coreir_not(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_name == "not"
        neg_one = self.make_constant(type(inst.I), -1)
        comb.BaseOp(
            op_name="xor",
            operands=[neg_one, module.operands[0]],
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_coreir_reg(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_name == "reg" or defn.coreir_name == "reg_arst"
        reg = self._ctx.new_value(
            hw.InOutType(magma_type_to_mlir_type(type(defn.O))))
        sv.RegOp(name=inst.name, results=[reg])
        clock_edge = "posedge"
        has_reset = (defn.coreir_name == "reg_arst")
        operands = [module.operands[1]]
        attrs = dict(clock_edge=clock_edge)
        if has_reset:
            reset_type = "asyncreset"
            arst_posedge = defn.coreir_configargs["arst_posedge"]
            reset_edge = "posedge" if arst_posedge else "negedge"
            operands.append(module.operands[2])
            attrs.update(dict(reset_type=reset_type, reset_edge=reset_edge))
        always = sv.AlwaysFFOp(operands=operands, **attrs)
        init = defn.coreir_configargs["init"].value
        const = self.make_constant(type(defn.I), init)
        with push_block(always.body_block):
            sv.PAssignOp(operands=[reg, module.operands[0]])
        if has_reset:
            always.operands.append(module.operands[1])
            with push_block(always.reset_block):
                sv.PAssignOp(operands=[reg, const])
        with push_block(sv.InitialOp()):
            sv.BPAssignOp(operands=[reg, const])
        sv.ReadInOutOp(operands=[reg], results=module.results.copy())
        return True

    @wrap_with_not_implemented_error
    def visit_coreir_primitive(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert (defn.coreir_lib == "coreir" or defn.coreir_lib == "corebit")
        if defn.coreir_name == "not":
            return self.visit_coreir_not(module)
        if defn.coreir_name in ("eq", "ult"):
            comb.ICmpOp(
                predicate=defn.coreir_name,
                operands=module.operands,
                results=module.results)
            return True
        if defn.coreir_name in ("reg", "reg_arst"):
            return self.visit_coreir_reg(module)
        comb.BaseOp(
            op_name=defn.coreir_name,
            operands=module.operands,
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_muxn(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_name == "muxn"
        data = self._ctx.new_value(defn.I.data)
        sel = self._ctx.new_value(defn.I.sel)
        hw.StructExtractOp(
            field="data",
            operands=module.operands.copy(),
            results=[data])
        hw.StructExtractOp(
            field="sel",
            operands=module.operands.copy(),
            results=[sel])
        hw.ArrayGetOp(
            operands=[data, sel],
            results=module.results.copy())
        return True

    @wrap_with_not_implemented_error
    def visit_commonlib_primitive(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_lib == "commonlib"
        if defn.coreir_name == "muxn":
            return self.visit_muxn(module)

    @wrap_with_not_implemented_error
    def visit_array_get(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert isinstance(defn, MagmaArrayGetOp)
        sel_size = m.bitutils.clog2(len(defn.I))
        index = self.make_constant(m.Bits[sel_size], inst.kwargs["index"])
        hw.ArrayGetOp(
            operands=(module.operands + [index]),
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_primitive(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert m.isprimitive(defn)
        if defn.coreir_lib == "coreir" or defn.coreir_lib == "corebit":
            return self.visit_coreir_primitive(module)
        if defn.coreir_lib == "commonlib":
            return self.visit_commonlib_primitive(module)
        if isinstance(defn, MagmaArrayGetOp):
            if isinstance(defn.T, m.BitsMeta) or issubclass(defn.T.T, m.Bit):
                comb.ExtractOp(
                    operands=module.operands,
                    results=module.results,
                    lo=inst.kwargs["index"])
                return True
            return self.visit_array_get(module)
        if isinstance(defn, MagmaArrayCreateOp):
            if isinstance(defn.T, m.BitsMeta) or issubclass(defn.T.T, m.Bit):
                if len(module.operands) == 1:
                    comb.BaseOp(
                        op_name="merge",
                        operands=module.operands,
                        results=module.results)
                    return True
                comb.ConcatOp(
                    operands=list(reversed(module.operands)),
                    results=module.results)
                return True
            hw.ArrayCreateOp(
                operands=list(reversed(module.operands)),
                results=module.results)
            return True
        if isinstance(defn, (MagmaBitConstantOp, MagmaBitsConstantOp)):
            hw.ConstantOp(value=int(defn.value), results=module.results)
            return True
        if isinstance(defn, MagmaProductGetOp):
            hw.StructExtractOp(
                field=defn.index,
                operands=module.operands,
                results=module.results)
            return True
        if isinstance(defn, MagmaProductCreateOp):
            hw.StructCreateOp(
                operands=module.operands,
                results=module.results)
            return True

    @wrap_with_not_implemented_error
    def visit_magma_mux(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert isinstance(defn, m.Mux)
        # NOTE(rsetaluri): This is a round-about way to get the height while
        # magma.Mux does not store those parameters. That should be fixed in
        # magma/primitives/mux.py.
        height = len(list(filter(
            lambda p: "I" in p.name.name, defn.interface.outputs())))
        T = type(defn.I0)
        mlir_type = hw.ArrayType((height,), magma_type_to_mlir_type(T))
        array = self._ctx.new_value(mlir_type)
        hw.ArrayCreateOp(
            operands=module.operands[:-1],
            results=[array])
        hw.ArrayGetOp(
            operands=[array, module.operands[-1]],
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_magma_register(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        reg = self._ctx.new_value(
            hw.InOutType(magma_type_to_mlir_type(type(defn.O))))
        sv.RegOp(name=inst.name, results=[reg])
        clock_edge = "posedge"
        has_reset = defn.reset_type is not None
        operands = [module.operands[1]]
        attrs = dict(clock_edge=clock_edge)
        if has_reset:
            operands.append(module.operands[2])
            reset_type, reset_edge = parse_reset_type(defn.reset_type)
            attrs.update(dict(reset_type=reset_type, reset_edge=reset_edge))
        always = sv.AlwaysFFOp(operands=operands, **attrs)
        const = self.make_constant(type(defn.I), defn.init)
        with push_block(always.body_block):
            sv.PAssignOp(operands=[reg, module.operands[0]])
        if has_reset:
            always.operands.append(module.operands[1])
            with push_block(always.reset_block):
                sv.PAssignOp(operands=[reg, const])
        with push_block(sv.InitialOp()):
            sv.BPAssignOp(operands=[reg, const])
        sv.ReadInOutOp(operands=[reg], results=module.results.copy())
        return True

    @wrap_with_not_implemented_error
    def visit_instance(self, module: ModuleWrapper) -> bool:
        inst = module.module
        assert isinstance(inst, m.circuit.AnonymousCircuitType)
        defn = type(inst)
        if isinstance(defn, m.Mux):
            return self.visit_magma_mux(module)
        if isinstance(defn, m.Register):
            return self.visit_magma_register(module)
        if m.isprimitive(defn):
            return self.visit_primitive(module)
        hw.InstanceOp(
            name=inst.name,
            module=defn.name,
            operands=module.operands,
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_module(self, module: ModuleWrapper) -> bool:
        if isinstance(module.module, m.DefineCircuitKind):
            return True
        if isinstance(module.module, m.circuit.AnonymousCircuitType):
            return self.visit_instance(module)

    def visit(self, module: MagmaModuleLike):
        if module in self._visited:
            raise RuntimeError(f"Can not re-visit module")
        self._visited.add(module)
        for predecessor in self._graph.predecessors(module):
            if predecessor in self._visited:
                continue
            self.visit(predecessor)
        for src, _, data in self._graph.in_edges(module, data=True):
            info = data["info"]
            src_port, dst_port = info["src"], info["dst"]
            src_value = self._ctx.get_or_make_mapped_value(src_port)
            self._ctx.set_mapped_value(dst_port, src_value)
        assert self.visit_module(ModuleWrapper.make(module, self._ctx))


def lower_magma_defn_to_hw_module_op(defn: m.DefineCircuitKind):
    graph = build_magma_graph(defn)
    ctx = ModuleContext()

    def new_values(fn, ports):
        namer = magma_value_or_type_to_string
        return [fn(port, name=namer(port), force=True) for port in ports]

    i, o = [], []
    for port in defn.interface.ports.values():
        visit_magma_value_by_direction(port, i.append, o.append)
    inputs = new_values(ctx.get_or_make_mapped_value, o)
    named_outputs = new_values(ctx.new_value, i)
    op = hw.ModuleOp(
        name=defn.name,
        operands=inputs,
        results=named_outputs)
    visitor = ModuleVisitor(graph, ctx)
    if not named_outputs:
        return
    with push_block(op):
        visitor.visit(defn)
        output_values = new_values(ctx.get_or_make_mapped_value, i)
        hw.OutputOp(operands=output_values)


def lower_magma_defn_to_mlir_module_op(
        defn: m.DefineCircuitKind) -> builtin.ModuleOp:

    # NOTE(rsetaluri): This is a round-about way to mark new types as
    # primitives. These definitions should actually be marked as primitives.
    def isdefinition(defn_or_decl: m.circuit.CircuitKind):
        if isinstance(defn_or_decl, m.Mux):
            return False
        if isinstance(defn_or_decl, m.Register):
            return False
        return m.isdefinition(defn_or_decl)

    deps = m.passes.dependencies(defn, include_self=True)
    module = builtin.ModuleOp()
    with push_block(module):
        for dep in deps:
            if not isdefinition(dep):
                continue
            lower_magma_defn_to_hw_module_op(dep)
    return module


def compile_to_mlir(
        defn: m.DefineCircuitKind, sout: Optional[io.TextIOBase] = None):
    if sout is None:
        sout = sys.stdout
    printer = PrinterBase(sout=sout)
    module = lower_magma_defn_to_mlir_module_op(defn)
    for hw_module in module.regions[0].blocks[0].operations:
        hw_module.print(printer)
