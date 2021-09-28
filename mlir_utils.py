from typing import Iterable

import magma as m

from common import wrap_with_not_implemented_error
from graph_lib import Graph
from magma_graph import ModuleLike
from magma_graph_utils import (
    MagmaArrayGetOp, MagmaArrayCreateOp,
    MagmaProductGetOp, MagmaProductCreateOp,
    MagmaBitConstantOp, MagmaBitsConstantOp)
from mlir_context import MlirContext
from mlir_graph import (
    MlirOp, MlirMultiOp,
    HwConstantOp, HwInstanceOp, HwOutputOp,
    HwArrayGetOp, HwArrayCreateOp, HwStructExtractOp, HwStructCreateOp,
    CombOp, CombICmpOp, CombExtractOp, CombConcatOp, CombMuxOp,
    SvRegOp, SvReadInOutOp, SvRegAssignOp, SvRegInitOp)
from mlir_type import (
    MlirType, MlirIntegerType, HwArrayType, HwStructType, HwInOutType)
from mlir_value import MlirValue


def _make_hw_array_get_op(ctx: MlirContext, inst: m.Circuit) -> MlirMultiOp:
    defn = type(inst)
    assert isinstance(defn, MagmaArrayGetOp)
    g = Graph()
    const = HwConstantOp(inst.name, defn.index)
    width = m.bitutils.clog2(len(defn.I))
    value = ctx.anonymous_value(MlirIntegerType(width))
    getter = HwArrayGetOp(inst.name)
    g.add_nodes_from((const, value, getter))
    g.add_edge(const, value, info=0)
    g.add_edge(value, getter, info=1)
    inputs = ((getter, 0, 0),)
    outputs = ((getter, 0),)
    return MlirMultiOp(inst.name, g, inputs, outputs)


def _make_not_op(ctx: MlirContext, inst: m.Circuit) -> MlirMultiOp:
    defn = type(inst)
    assert ((defn.coreir_lib == "coreir" or defn.coreir_lib == "corebit")
            and defn.coreir_name == "not")
    g = Graph()
    const = HwConstantOp(inst.name, -1)
    width = 1 if defn.coreir_lib == "corebit" else len(defn.O)
    value = ctx.anonymous_value(MlirIntegerType(width))
    xor = CombOp(inst.name, "xor")
    g.add_nodes_from((const, value, xor))
    g.add_edge(const, value, info=0)
    g.add_edge(value, xor, info=1)
    inputs = ((xor, 0, 0),)
    outputs = ((xor, 0),)
    return MlirMultiOp(inst.name, g, inputs, outputs)


def _make_mux_op(ctx: MlirContext, inst: m.Circuit) -> MlirMultiOp:
    defn = type(inst)
    assert defn.coreir_lib == "commonlib" and defn.coreir_name == "muxn"
    g = Graph()
    data_extractor = HwStructExtractOp(inst.name, "data")
    sel_extractor = HwStructExtractOp(inst.name, "sel")
    data_value = ctx.anonymous_value(magma_type_to_mlir_type(type(defn.I.data)))
    sel_value = ctx.anonymous_value(magma_type_to_mlir_type(type(defn.I.sel)))
    getter = HwArrayGetOp(inst.name)
    g.add_nodes_from(
        (data_extractor, sel_extractor, data_value, sel_value, getter))
    g.add_edge(data_extractor, data_value, info=0)
    g.add_edge(sel_extractor, sel_value, info=0)
    g.add_edge(data_value, getter, info=0)
    g.add_edge(sel_value, getter, info=1)
    inputs = ((data_extractor, 0, 0), (sel_extractor, 0, 0))
    outputs = ((getter, 0),)
    return MlirMultiOp(inst.name, g, inputs, outputs)


def _make_reg_op(ctx: MlirContext, inst: m.Circuit) -> MlirMultiOp:
    defn = type(inst)
    assert defn.coreir_lib == "coreir" and defn.coreir_name == "reg"
    g = Graph()
    value_type = magma_type_to_mlir_type(type(defn.O))
    reg_type = HwInOutType(value_type)
    reg_op = SvRegOp(inst.name)
    reg = ctx.anonymous_value(reg_type)
    reg_reader = SvReadInOutOp(inst.name)
    reg_assigner = SvRegAssignOp(inst.name, True)
    reg_initer = SvRegInitOp(inst.name)
    reg_init_op = HwConstantOp(inst.name, defn.coreir_configargs["init"].value)
    reg_init_value = ctx.anonymous_value(value_type)
    g.add_nodes_from((
        reg_op, reg, reg_reader, reg_assigner, reg_initer, reg_init_op,
        reg_init_value))
    g.add_edge(reg_op, reg, info=0)
    g.add_edge(reg, reg_reader, info=0)
    g.add_edge(reg, reg_assigner, info=1)
    g.add_edge(reg, reg_initer, info=0)
    g.add_edge(reg_init_op, reg_init_value, info=0)
    g.add_edge(reg_init_value, reg_initer, info=1)
    inputs = ((reg_assigner, 0, 0), (reg_assigner, 1, 2))
    outputs = ((reg_reader, 0),)
    return MlirMultiOp(inst.name, g, inputs, outputs)


@wrap_with_not_implemented_error
def magma_type_to_mlir_type(type: m.Kind) -> MlirType:
    type = type.undirected_t
    if issubclass(type, m.Digital):
        return MlirIntegerType(1)
    if issubclass(type, m.Bits):
        return MlirIntegerType(type.N)
    if issubclass(type, m.Array):
        if issubclass(type.T, m.Bit):
            return magma_type_to_mlir_type(m.Bits[type.N])
        return HwArrayType((type.N,), magma_type_to_mlir_type(type.T))
    if issubclass(type, m.Product):
        fields = {k: magma_type_to_mlir_type(t)
                  for k, t in type.field_dict.items()}
        return HwStructType(tuple(fields.items()))


@wrap_with_not_implemented_error
def commonlib_primitive_to_mlir_op(ctx: MlirContext, inst: m.Circuit) -> MlirOp:
    defn = type(inst)
    assert defn.coreir_lib == "commonlib"
    if defn.coreir_name == "muxn":
        return _make_mux_op(ctx, inst)


@wrap_with_not_implemented_error
def coreir_primitive_to_mlir_op(ctx: MlirContext, inst: m.Circuit) -> MlirOp:
    defn = type(inst)
    assert (defn.coreir_lib == "coreir" or defn.coreir_lib == "corebit")
    if defn.coreir_name == "not":
        return _make_not_op(ctx, inst)
    if defn.coreir_name in ("eq",):
        return CombICmpOp(inst.name, defn.coreir_name)
    if defn.coreir_name == "reg":
        return _make_reg_op(ctx, inst)
    return CombOp(inst.name, defn.coreir_name)


@wrap_with_not_implemented_error
def magma_primitive_to_mlir_op(ctx: MlirContext, inst: m.Circuit) -> MlirOp:
    defn = type(inst)
    assert m.isprimitive(defn)
    if defn.coreir_lib == "coreir" or defn.coreir_lib == "corebit":
        return coreir_primitive_to_mlir_op(ctx, inst)
    if defn.coreir_lib == "commonlib":
        return commonlib_primitive_to_mlir_op(ctx, inst)
    if isinstance(defn, MagmaArrayGetOp):
        if isinstance(defn.T, m.BitsMeta) or issubclass(defn.T.T, m.Bit):
            return CombExtractOp(inst.name, defn.index, defn.index + 1)
        return _make_hw_array_get_op(ctx, inst)
    if isinstance(defn, MagmaArrayCreateOp):
        if isinstance(defn.T, m.BitsMeta) or issubclass(defn.T.T, m.Bit):
            return CombConcatOp(inst.name)
        return HwArrayCreateOp(inst.name)
    if isinstance(defn, MagmaProductGetOp):
        return HwStructExtractOp(inst.name, defn.index)
    if isinstance(defn, MagmaProductCreateOp):
        return HwStructCreateOp(inst.name)
    if isinstance(defn, MagmaBitConstantOp):
        return HwConstantOp(inst.name, int(defn.value))
    if isinstance(defn, MagmaBitsConstantOp):
        return HwConstantOp(inst.name, defn.value)


@wrap_with_not_implemented_error
def magma_instance_to_mlir_op(ctx: MlirContext, inst: m.Circuit) -> MlirOp:
    defn = type(inst)
    if m.isprimitive(defn):
        return magma_primitive_to_mlir_op(ctx, inst)
    return HwInstanceOp(inst.name, defn.name)


@wrap_with_not_implemented_error
def magma_module_to_mlir_op(ctx: MlirContext, module: ModuleLike) -> MlirOp:
    if isinstance(module, m.Circuit):
        return magma_instance_to_mlir_op(ctx, module)
    if isinstance(module, m.DefineCircuitKind):
        return HwOutputOp(module.name)
