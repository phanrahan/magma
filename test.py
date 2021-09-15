from comb import comb
from graph_base import write_to_dot
from magma_graph import build_magma_graph


def main():
    g = build_magma_graph(comb)
    print (g.nodes())
    print (g.edges())
    write_to_dot(g, "graph.txt")


if __name__ == "__main__":
    main()
