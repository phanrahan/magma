import functools
from typing import Any

from magma.array import Array
from magma.bit import Bit
from magma.bits import Bits
from magma.digital import Digital
from magma.backend.mlir.builtin import builtin
from magma.backend.mlir.common import wrap_with_not_implemented_error
from magma.backend.mlir.hw import hw
from magma.backend.mlir.mlir import MlirType, MlirAttribute
from magma.t import Kind
from magma.tuple import Tuple as m_Tuple


@wrap_with_not_implemented_error
@functools.lru_cache()
def magma_type_to_mlir_type(type: Kind) -> MlirType:
    type = type.undirected_t
    if issubclass(type, Digital):
        return builtin.IntegerType(1)
    if issubclass(type, Bits):
        return builtin.IntegerType(type.N)
    if issubclass(type, Array):
        if issubclass(type.T, Bit):
            return magma_type_to_mlir_type(Bits[type.N])
        return hw.ArrayType((type.N,), magma_type_to_mlir_type(type.T))
    if issubclass(type, m_Tuple):
        fields = {str(k): magma_type_to_mlir_type(t)
                  for k, t in type.field_dict.items()}
        return hw.StructType(tuple(fields.items()))


@wrap_with_not_implemented_error
@functools.lru_cache()
def python_type_to_mlir_type(type_: type) -> MlirType:
    # NOTE(rsetaluri): We only support integer attribtue types right now. All
    # integer parameter types are assumed to be int32's.
    if type_ is int:
        return builtin.IntegerType(32)


@wrap_with_not_implemented_error
def python_value_to_mlir_attribtue(value: Any) -> MlirAttribute:
    # NOTE(rsetaluri): We only support integer attribute types right now.
    if isinstance(value, int):
        return builtin.IntegerAttr(value)
