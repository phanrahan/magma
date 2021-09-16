from typing import List

from emitter import Emitter
from mlir_graph import MlirOp
from mlir_value import MlirValue


MlirValueList = List[MlirValue]


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
            input_names=mlir_values_to_string(inputs, 0),
            output_names=mlir_values_to_string(outputs, 0),
            input_types=mlir_values_to_string(inputs, 1),
            output_types=mlir_values_to_string(outputs, 1),
            input_names_and_types=mlir_values_to_string(inputs, 2),
            output_names_and_types=mlir_values_to_string(outputs, 2))
        self.emit(emission)
