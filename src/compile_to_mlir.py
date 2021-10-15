import dataclasses
import io
import sys
from typing import List, Optional, Tuple, Union

import magma as m

from build_magma_graph import build_magma_graph
from builtin import builtin
from comb import comb
from common import wrap_with_not_implemented_error
from graph_lib import Graph
from hw import hw
from magma_common import ModuleLike as MagmaModuleLike
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
        if port.is_input():
            value = ctx.get_or_make_mapped_value(port)
            operands.append(value)
        elif port.is_output():
            value = ctx.get_or_make_mapped_value(port)
            results.append(value)
        else:
            raise NotImplementedError()
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

    def make_constant(self, T: m.Kind, value: int):
        result = self._ctx.new_value(T)
        hw.ConstantOp(value=value, results=[result])
        return result

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
        assert defn.coreir_name == "reg"
        reg = self._ctx.new_value(
            hw.InOutType(magma_type_to_mlir_type(type(defn.O))))
        sv.RegOp(name=inst.name, results=[reg])
        with push_block(sv.AlwaysFFOp(operands=[module.operands[1]])):
            sv.PAssignOp(operands=[reg, module.operands[0]])
        with push_block(sv.InitialOp()):
            init = defn.coreir_configargs["init"].value
            const = self.make_constant(type(defn.I), init)
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
        # if defn.coreir_name in ("eq", "ult"):
        #     return comb.ICmpOp(inst.name, defn.coreir_name)
        if defn.coreir_name == "reg":
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
    def visit_instance(self, module: ModuleWrapper) -> bool:
        inst = module.module
        assert isinstance(inst, m.Circuit)
        defn = type(inst)
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
        if isinstance(module.module, m.Circuit):
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
    inputs = [
        ctx.get_or_make_mapped_value(port, name=port.name, force=True)
        for port in defn.interface.outputs()
    ]
    named_outputs = [
        ctx.new_value(port, name=port.name, force=True)
        for port in defn.interface.inputs()
    ]
    op = hw.ModuleOp(
        name=defn.name,
        operands=inputs,
        results=named_outputs)
    visitor = ModuleVisitor(graph, ctx)
    with push_block(op):
        visitor.visit(defn)
        output_values = [
            ctx.get_or_make_mapped_value(port, name=port.name, force=True)
            for port in defn.interface.inputs()
        ]
        hw.OutputOp(operands=output_values)


def lower_magma_defn_to_mlir_module_op(
        defn: m.DefineCircuitKind) -> builtin.ModuleOp:
    deps = m.passes.dependencies(defn, include_self=True)
    module = builtin.ModuleOp()
    with push_block(module):
        for dep in deps:
            if not m.isdefinition(dep):
                continue
            lower_magma_defn_to_hw_module_op(dep)
    return module


def compile_to_mlir(
        defn: m.DefineCircuitKind, sout: Optional[io.TextIOBase] = None):
    if sout is None:
        sout = sys.stdout
    deps = m.passes.dependencies(defn, include_self=True)
    printer = PrinterBase(sout=sout)
    module = lower_magma_defn_to_mlir_module_op(defn)
    for hw_module in module.regions[0].blocks[0].operations:
        hw_module.print(printer)
