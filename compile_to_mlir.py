import dataclasses
import io
from typing import Optional

import magma as m

from common_visitors import RemoveDuplicateEdgesTransformer
from graph_lib import Graph, topological_sort
from magma_graph import build_magma_graph
from magma_visitors import SplitPortEdgesTranformer, MergeNetsTransformer
from mlir_context import MlirContext
from mlir_emitter import MlirEmitter
from mlir_graph import MlirOp
from mlir_utils import magma_type_to_mlir_type
from mlir_value import MlirValue
from mlir_visitors import (
    ModuleInputSplitter, NetToValueTransformer, EdgePortToIndexTransformer,
    ModuleToOpTransformer, MultiOpFlattener, EmitMlirVisitor)


@dataclasses.dataclass(frozen=True)
class HwModuleOp(MlirOp):
    name: str

    def emit(self) -> str:
        return (f"hw.module @{self.name}({{inputs.signature}}) -> "
                f"({{outputs.signature}}) {{{{")


def emit_module(emitter: MlirEmitter, ckt: m.DefineCircuitKind, g: Graph):
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


def compile_defn_to_mlir(ckt: m.DefineCircuitKind, emitter: MlirEmitter):
    g = build_magma_graph(ckt)
    ctx = MlirContext()

    SplitPortEdgesTranformer(g).run()
    RemoveDuplicateEdgesTransformer(g).run()
    MergeNetsTransformer(g).run()
    ModuleInputSplitter(g, ctx).run()
    NetToValueTransformer(g, ctx).run(topological_sort)
    EdgePortToIndexTransformer(g).run()
    ModuleToOpTransformer(g, ctx).run()
    MultiOpFlattener(g).run()

    emit_module(emitter, ckt, g)


def compile_to_mlir(ckt: m.DefineCircuitKind, sout: Optional[io.TextIOBase] = None):
    deps = m.passes.dependencies(ckt, include_self=True)
    emitter = MlirEmitter(sout)
    for dep in deps:
        if not m.isdefinition(dep):
            continue
        compile_defn_to_mlir(dep, emitter)
