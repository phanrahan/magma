from typing import Iterable

import magma as m

from common import wrap_with_not_implemented_error
from magma_graph import ModuleLike
from mlir_type import MlirType, MlirIntegerType
from mlir_value import MlirValue
from mlir_graph import MlirOp, HwInstanceOp, HwOutputOp, CombOp


@wrap_with_not_implemented_error
def magma_type_to_mlir_type(type: m.Kind) -> MlirType:
    type = type.undirected_t
    if issubclass(type, m.Digital):
        return MlirIntegerType(1)
    if issubclass(type, m.Bits):
        return MlirIntegerType(type.N)


@wrap_with_not_implemented_error
def magma_instance_to_mlir_op(inst: m.Circuit) -> MlirOp:
    defn = type(inst)
    if m.isprimitive(defn):
        return CombOp(inst.name, defn.coreir_name)
    return HwInstanceOp(inst.name, defn.name)


@wrap_with_not_implemented_error
def magma_module_to_mlir_op(module: ModuleLike) -> MlirOp:
    if isinstance(module, m.Circuit):
        return magma_instance_to_mlir_op(module)
    if isinstance(module, m.DefineCircuitKind):
        return HwOutputOp(module.name)
