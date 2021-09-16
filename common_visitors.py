from typing import Iterable

from graph_lib import Graph, Node, Edge
from graph_visitor import NodeTransformer


class RemoveDuplicateEdgesTransformer(NodeTransformer):
    def generic_visit(self, node: Node):
        dsts = set()
        edges = list(self.graph.in_edges(node, data=True))
        for edge in self.graph.out_edges(node, data=True):
            src, dst, data = edge
            if dst in dsts:
                continue
            dsts.add(dst)
            edges.append((src, dst, data))
        return [node], edges


def replace_node(g: Graph, orig: Node, new: Node) -> Iterable[Edge]:
    for edge in g.in_edges(orig, data=True):
        src, _, data = edge
        yield (src, new, data)
    for edge in g.out_edges(orig, data=True):
        _, dst, data = edge
        yield (new, dst, data)
