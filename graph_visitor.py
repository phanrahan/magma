from typing import Any, Callable, Iterable, Optional

from graph_lib import Graph, Node, NodeOrderer


def order_nodes(
        g: Graph, node_orderer: Optional[NodeOrderer]) -> Iterable[Node]:
    if node_orderer is None:
        return g.nodes()
    return node_orderer(g)


def _process_transform_info(transform_info, g: Graph, node: Node):
    if transform_info is node:
        return
    orig = node
    nodes, edges = transform_info
    g.remove_node(orig)
    for node in nodes:
        g.add_node(node)
    for edge in edges:
        src, dst, attrs = edge
        g.add_edge(src, dst, **attrs)


class NodeVisitor:
    def __init__(self, g: Graph):
        self._g = g

    def run(self, node_orderer: Optional[NodeOrderer] = None):
        nodes = order_nodes(self._g, node_orderer)
        self._run_on_nodes(nodes)

    def _run_on_nodes(self, nodes: Iterable[Any]):
        for node in nodes:
            self.visit(node)

    def generic_visit(self, node: Any):
        pass

    def visit(self, node: Any):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        visitor(node)

    @property
    def graph(self):
        return self._g


class NodeTransformer(NodeVisitor):
    def run(self, node_orderer: Optional[NodeOrderer] = None):
        nodes = list(order_nodes(self._g, node_orderer))
        self._run_on_nodes(nodes)

    def generic_visit(self, node: Any):
        return node

    def visit(self, node: Any):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        transform_info = visitor(node)
        _process_transform_info(transform_info, self._g, node)
