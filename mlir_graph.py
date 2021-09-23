import dataclasses
from typing import Any, Tuple

from common import missing
from graph_lib import Graph, Node
from mlir_value import MlirValue


HashableMapping = Tuple[Tuple[Any, Any]]


def op_kind_set_attr(key: str, value: Any):

    def wrapped(op_kind: type) -> type:
        try:
            attrs = op_kind._mlir_op_kind_attrs_
        except AttributeError:
            attrs = op_kind._mlir_op_kind_attrs_ = {}
        attrs[key] = value
        return op_kind

    return wrapped


def op_kind_get_attr(op_kind: type, key: str, default: Any = missing()):
    attrs = getattr(op_kind, "_mlir_op_kind_attrs_", {})
    if default is missing():
        return attrs[key]
    return attrs.get(key, default)


@dataclasses.dataclass(frozen=True)
class MlirOp:
    name: str


@dataclasses.dataclass(frozen=True)
class MlirMultiOp(MlirOp):
    name: str
    graph: Graph
    primary_inputs: Tuple[Tuple[Node, int, int]]
    primary_outputs: Tuple[Tuple[Node, int]]


@dataclasses.dataclass(frozen=True)
class CombOp(MlirOp):
    name: str
    op: str

    def emit(self):
        return (f"{{outputs.names}} = comb.{self.op} {{inputs.names}} : "
                f"{{outputs.types}}")


@dataclasses.dataclass(frozen=True)
class CombExtractOp(MlirOp):
    name: str
    lo: int
    hi: int

    def emit(self):
        return (f"{{outputs.names}} = comb.extract {{inputs.names}} "
                f"from {self.lo} : ({{inputs.types}}) -> {{outputs.types}}")


@op_kind_set_attr("inputs_reversed", True)
@dataclasses.dataclass(frozen=True)
class CombConcatOp(MlirOp):
    name: str

    def emit(self):
        return (f"{{outputs.names}} = comb.concat {{inputs.names}} : "
                f"({{inputs.types}}) -> {{outputs.types}}")


@dataclasses.dataclass(frozen=True)
class HwConstantOp(MlirOp):
    name: str
    value: int

    def emit(self):
        return (f"{{outputs.names}} = hw.constant {self.value} : "
                f"{{outputs.types}}")


@dataclasses.dataclass(frozen=True)
class HwArrayGetOp(MlirOp):
    name: str

    def emit(self):
        return (f"{{outputs.names}} = hw.array_get "
                f"{{inputs[0].name}}[{{inputs[1].name}}] : {{inputs[0].type}}")


@op_kind_set_attr("inputs_reversed", True)
@dataclasses.dataclass(frozen=True)
class HwArrayCreateOp(MlirOp):
    name: str

    def emit(self):
        return (f"{{outputs.names}} = hw.array_create {{inputs.names}} : "
                f"{{inputs[0].type}}")


@dataclasses.dataclass(frozen=True)
class HwStructExtractOp(MlirOp):
    name: str
    field: str

    def emit(self):
        return (f"{{outputs.names}} = hw.struct_extract "
                f"{{inputs.names}}[\"{self.field}\"] : {{inputs.types}}")


@dataclasses.dataclass(frozen=True)
class HwStructCreateOp(MlirOp):
    name: str

    def emit(self):
        return (f"{{outputs.names}} = hw.struct_create ({{inputs.names}}) : "
                f"{{outputs.types}}")


@dataclasses.dataclass(frozen=True)
class HwInstanceOp(MlirOp):
    name: str
    defn: str

    def emit(self):
        return (f"{{outputs.names}} = hw.instance \"{self.name}\" "
                f"@{self.defn}({{inputs.names}}) : ({{inputs.types}}) -> "
                f"({{outputs.types}})")


@dataclasses.dataclass(frozen=True)
class HwOutputOp(MlirOp):
    name: str

    def emit(self):
        return (f"hw.output {{inputs.names}} : {{inputs.types}}")
