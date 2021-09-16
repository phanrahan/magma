import magma as m

from graph_lib import Graph


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
    for src, dst, data in g.edges(data=True):
        src = make_str(src)
        dst = make_str(dst)
        label = None
        if "info" in data:
            label = make_str(data["info"])
        g_flat.add_edge(src, dst, label=label)
    return g_flat
