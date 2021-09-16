from graph_base import write_to_dot
from magma_graph import build_magma_graph
from debug_utils import flatten_magma_graph
from passes import *
from mlir_passes import *


def compile_to_mlir(ckt: m.DefineCircuitKind):
    g = build_magma_graph(ckt)

    write_to_dot(flatten_magma_graph(g), "graph.txt")

    SplitPortEdgesTranformer(g).run()
    RemoveDuplicateEdgesTransformer(g).run()
    NetMerger(g).run()

    ctx = MlirContext()
    ModuleInputSplitter(g, ctx).run()
    NetToValueTransformer(g, ctx).run(topological_sort)
    EdgePortToIndexTransformer(g, ctx).run()
    ModuleToOpTransformer(g, ctx).run()

    emit_module(ckt, g)

    write_to_dot(flatten_magma_graph(g), "graph-lowered.txt")
