from comb import comb
from graph_base import write_to_dot
from magma_graph import build_magma_graph
from mlir_graph import lower_graph


def main():
    g = build_magma_graph(comb)
    write_to_dot(g, "graph.txt")
    lower_graph(g)
    write_to_dot(g, "graph-lowered.txt")


if __name__ == "__main__":
    main()
