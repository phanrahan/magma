from comb import comb
from graph_base import write_to_dot, topological_sort
from magma_graph import build_magma_graph
#from mlir_graph import lower_graph
from debug_utils import flatten_magma_graph
from passes import *
from mlir_passes import *


def main():
    g = build_magma_graph(comb)

    write_to_dot(flatten_magma_graph(g), "graph.txt")

    SplitPortEdgesTranformer(g).run()
    RemoveDuplicateEdgesTransformer(g).run()
    NetMerger(g).run()

    ctx = MlirContext()
    ModuleInputSplitter(g, ctx).run()
    NetToValueTransformer(g, ctx).run(topological_sort)
    EdgePortToIndexTransformer(g, ctx).run()
    ModuleToOpTransformer(g, ctx).run()

    emitter = Emitter()
    emitter.push()
    EmitMlirVisitor(g, emitter).run(topological_sort)
    emitter.pop()
    
    write_to_dot(flatten_magma_graph(g), "graph-lowered.txt")


if __name__ == "__main__":
    main()
