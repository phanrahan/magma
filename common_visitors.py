from graph_lib import Node
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
