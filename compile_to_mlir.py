from graph_lib import Graph, write_to_dot
from magma_graph import build_magma_graph
from debug_utils import flatten_magma_graph
from mlir_visitors import *
from common_visitors import *
from magma_visitors import *
from mlir_utils import magma_type_to_mlir_type
from mlir_emitter import mlir_values_to_string


@dataclasses.dataclass(frozen=True)
class HwModuleOp(MlirOp):
    name: str

    def emit(self) -> str:
        return (f"hw.module @{self.name}({{output_names_and_types}}) -> "
                f"({{output_names_and_types}}) {{{{")


def emit_module(ckt: m.DefineCircuitKind, g: Graph):
    emitter = MlirEmitter()
    inputs = [MlirValue(f"%{port.name}", magma_type_to_mlir_type(type(port)))
              for port in ckt.interface.outputs()]
    outputs = [MlirValue(f"%{port.name}", magma_type_to_mlir_type(type(port)))
               for port in ckt.interface.inputs()]
    op = HwModuleOp(ckt.name)
    emitter.emit_op(op, inputs, outputs)
    emitter.push()
    EmitMlirVisitor(g, emitter).run(topological_sort)
    emitter.pop()
    emitter.emit("}")


def compile_to_mlir(ckt: m.DefineCircuitKind):
    g = build_magma_graph(ckt)

    write_to_dot(flatten_magma_graph(g), "graph.txt")

    SplitPortEdgesTranformer(g).run()
    RemoveDuplicateEdgesTransformer(g).run()
    MergeNetsTransformer(g).run()

    ctx = MlirContext()
    ModuleInputSplitter(g, ctx).run()
    NetToValueTransformer(g, ctx).run(topological_sort)
    EdgePortToIndexTransformer(g).run()
    ModuleToOpTransformer(g).run()

    emit_module(ckt, g)

    write_to_dot(flatten_magma_graph(g), "graph-lowered.txt")
