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
        return ", ".join(v.name for v in self._values)

    @property
    def types(self) -> str:
        return ", ".join(v.type.emit() for v in self._values)

    @property
    def signature(self) -> str:
        return ", ".join(f"{v.name}: {v.type.emit()}" for v in self._values)

    def __getitem__(self, key: int) -> '_WrappedValue':
        return _WrappedValue(self._values[key])


class _WrappedValue:
    def __init__(self, value: MlirValue):
        self._value = value

    @property
    def name(self) -> str:
        return self._value.name

    @property
    def type(self) -> str:
        return self._value.type.emit()


class MlirEmitter(Emitter):
    def emit_op(
            self, op: MlirOp, inputs: MlirValueList, outputs: MlirValueList):
        emission = op.emit()
        emission = emission.format(
            inputs=_WrappedValueList(inputs),
            outputs=_WrappedValueList(outputs))
        self.emit(emission)
