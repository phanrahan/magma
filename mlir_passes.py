from typing import Iterable

import magma as m

from graph_base import Graph, Node
from graph_utils import NodeVisitor, NodeTransformer
from mlir_wrapper import MlirContext
from passes import Net


def _mlir_base_pass_factory(base):

    class MlirPass(base):
        def __init__(self, g: Graph, ctx: MlirContext):
            super().__init__(g)
            self._ctx = ctx

        @property
        def ctx(self) -> MlirContext:
            return self._ctx

    return MlirPass


MlirNodeVisitor = _mlir_base_pass_factory(NodeVisitor)
MlirNodeTransformer = _mlir_base_pass_factory(NodeTransformer)


class ModuleInputSplitter(MlirNodeTransformer):
    def generic_visit(self, node: Node):
        if not isinstance(node, m.DefineCircuitKind):
            return node
        nodes = [node]
        edges = list(self.graph.in_edges(node, data=True))
        nodes_to_remove = []
        for edge in self.graph.out_edges(node, data=True):
            _, dst, data = edge
            assert isinstance(dst, Net)
            port = data["info"]
            assert dst.ports[0] is port
            value = self.ctx.new_value(port.name, force=True)
            nodes.append(value)
            assert len(list(self.graph.predecessors(dst))) == 1
            for edge in self.graph.out_edges(dst, data=True):
                _, descendant, data = edge
                edges.append((value, descendant, data))
            nodes_to_remove.append(dst)
        for node in nodes_to_remove:
            self.graph.remove_node(node)
        return nodes, edges
