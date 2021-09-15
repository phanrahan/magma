import magma as m

from graph_base import Graph


def flatten_magma_graph(g: Graph):
    g_flat = Graph()

    def make_str(node):
        if isinstance(node, m.DefineCircuitKind):
            return node.name
        if isinstance(node, m.Circuit):
            return node.name
        if isinstance(node, m.Type):
            return repr(node)
        return str(node)

    g_flat.add_nodes_from(map(make_str, g.nodes()))
    g_flat.add_edges_from((make_str(u), make_str(v)) for u, v in g.edges())
    return g_flat
