from typing import Iterable

import magma as m

from magma_graph import ModuleLike
from mlir_type import MlirType, MlirIntegerType
from mlir_value import MlirValue
from mlir_graph import MlirOp, HwOutputOp, CombOp


def magma_type_to_mlir_type(type: m.Kind) -> MlirType:
    type = type.undirected_t
    if issubclass(type, m.Digital):
        return MlirIntegerType(1)
    if issubclass(type, m.Bits):
        return MlirIntegerType(type.N)
    raise NotImplementedError(type)


def magma_module_to_mlir_op(module: ModuleLike) -> MlirOp:
    if isinstance(module, m.Circuit):
        return CombOp(module.name, type(module).coreir_name)
    if isinstance(module, m.DefineCircuitKind):
        return HwOutputOp(module.name)
    raise NotImplementedError()
