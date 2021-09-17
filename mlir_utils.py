from typing import Iterable

import magma as m

from common import wrap_with_not_implemented_error
from magma_graph import ModuleLike
from magma_graph_utils import MagmaArrayGetOp, MagmaArrayCreateOp
from mlir_context import MlirContext
from mlir_graph import (
    MlirOp, MlirMultiOp,
    HwConstantOp, HwArrayGetOp, HwArrayCreateOp, HwInstanceOp, HwOutputOp,
    CombOp, CombExtractOp, CombConcatOp)
from mlir_type import MlirType, MlirIntegerType, HwArrayType
from mlir_value import MlirValue


def _make_hw_array_get_op(ctx: MlirContext, inst: m.Circuit) -> MlirMultiOp:
    defn = type(inst)
    assert isinstance(defn, MagmaArrayGetOp)
    const = HwConstantOp(inst.name, defn.index)
    width = m.bitutils.clog2(len(defn.I))
    value = ctx.new_value(MlirIntegerType(width))
    getter = HwArrayGetOp(inst.name)
    edges = ((const, value, (("info", 0),)),
             (value, getter, (("info", 1),)))
    input_nodes = ((getter, 0),)
    output_nodes = ((getter, 0),)
    return MlirMultiOp(
        inst.name, (getter, const, value), edges, input_nodes, output_nodes)


@wrap_with_not_implemented_error
def magma_type_to_mlir_type(type: m.Kind) -> MlirType:
    type = type.undirected_t
    if issubclass(type, m.Digital):
        return MlirIntegerType(1)
    if issubclass(type, m.Bits):
        return MlirIntegerType(type.N)
    if issubclass(type, m.Array):
        return HwArrayType((type.N,), magma_type_to_mlir_type(type.T))


@wrap_with_not_implemented_error
def magma_primitive_to_mlir_op(ctx: MlirContext, inst: m.Circuit) -> MlirOp:
    defn = type(inst)
    assert m.isprimitive(defn)
    if defn.coreir_lib == "coreir" or defn.coreir_lib == "corebit":
        return CombOp(inst.name, defn.coreir_name)
    if isinstance(defn, MagmaArrayGetOp):
        if isinstance(defn.T, m.BitsMeta):
            return CombExtractOp(inst.name, defn.index, defn.index + 1)
        return _make_hw_array_get_op(ctx, inst)
    if isinstance(defn, MagmaArrayCreateOp):
        if isinstance(defn.T, m.BitsMeta):
            return CombConcatOp(inst.name)
        return HwArrayCreateOp(inst.name)


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
