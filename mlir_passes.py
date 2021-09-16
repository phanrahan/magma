from typing import Any, Iterable, List

import magma as m

from graph_base import Graph, Node
from graph_utils import NodeVisitor, NodeTransformer
from mlir_wrapper import MlirContext, MlirValue
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


def replace_node(g: Graph, orig: Node, new: Node) -> Iterable[Any]:
    for edge in g.in_edges(orig, data=True):
        src, _, data = edge
        yield (src, new, data)
    for edge in g.out_edges(orig, data=True):
        _, dst, data = edge
        yield (new, dst, data)


class NetToValueTransformer(MlirNodeTransformer):
    def visit_Net(self, node: Net):
        assert len(list(self.graph.predecessors(node))) == 1
        value = self.ctx.new_value()
        edges = list(replace_node(self.graph, node, value))
        return [value], edges


class EdgePortToIndexTransformer(MlirNodeTransformer):
    def visit_MlirValue(self, node: MlirValue):
        return node

    def _get_index(value: m.Type, values: List[m.Type]) -> int:
        for i, v in enumerate(values):
            if v is value:
                return i
        raise KeyError()

    def generic_visit(self, node: Node):
        assert isinstance(node, (m.DefineCircuitKind, m.Circuit))
        edges = []
        finder = type(self)._get_index
        for edge in self.graph.in_edges(node, data=True):
            src, dst, data = edge
            port = data["info"]
            data["info"] = finder(port, node.interface.inputs())
            edges.append((src, dst, data))
        for edge in self.graph.out_edges(node, data=True):
            src, dst, data = edge
            port = data["info"]
            data["info"] = finder(port, node.interface.outputs())
            edges.append((src, dst, data))
        return [node], edges


import dataclasses


@dataclasses.dataclass(frozen=True)
class MlirOp:
    name: str


@dataclasses.dataclass(frozen=True)
class CombOp(MlirOp):
    name: str
    op: str


@dataclasses.dataclass(frozen=True)
class HwOutputOp(MlirOp):
    name: str


def lower_module_to_op(module): #: ModuleLike):
    if isinstance(module, m.Circuit):
        return CombOp(module.name, type(module).coreir_name)
    if isinstance(module, m.DefineCircuitKind):
        return HwOutputOp(module.name)
    raise NotImplementedError()


class ModuleToOpTransformer(MlirNodeTransformer):
    def visit_MlirValue(self, node: MlirValue):
        return node

    def generic_visit(self, node: Node):
        assert isinstance(node, (m.DefineCircuitKind, m.Circuit))
        new_node = lower_module_to_op(node)
        edges = list(replace_node(self.graph, node, new_node))
        return [new_node], edges
