from typing import List

from emitter import Emitter
from mlir_graph import MlirOp
from mlir_value import MlirValue


MlirValueList = List[MlirValue]


class _WrappedValueList:
    def __init__(self, values: MlirValueList):
        self._values = values

    @property
    def names(self) -> str:
        return mlir_values_to_string(self._values, mode=0)

    @property
    def types(self) -> str:
        return mlir_values_to_string(self._values, mode=1)

    @property
    def signature(self) -> str:
        return mlir_values_to_string(self._values, mode=2)

    def __getitem__(self, key: int) -> '_WrappedValue':
        return _WrappedValue(self._values[key])


class _WrappedValue:
    def __init__(self, value: MlirValue):
        self._wrapped_value_list = _WrappedValueList([value])

    @property
    def name(self) -> str:
        return self._wrapped_value_list.names

    @property
    def type(self) -> str:
        return self._wrapped_value_list.types


def mlir_values_to_string(values: MlirValueList, mode: int = 0) -> str:
    if mode == 0:
        mapper = lambda v: v.name
    elif mode == 1:
        mapper = lambda v: v.type.emit()
    else:
        mapper = lambda v: f"{v.name}: {v.type.emit()}"
    return ', '.join(map(mapper, values))


class MlirEmitter(Emitter):
    def emit_op(
            self, op: MlirOp, inputs: MlirValueList, outputs: MlirValueList):
        emission = op.emit()
        emission = emission.format(
            inputs=_WrappedValueList(inputs),
            outputs=_WrappedValueList(outputs))
        self.emit(emission)
