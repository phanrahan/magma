import dataclasses
from typing import Any, Iterable, List

import magma as m

from common_visitors import replace_node
from emitter import Emitter
from graph_lib import Graph, Node
from graph_visitor import NodeVisitor, NodeTransformer
from magma_graph import Net
from mlir_context import MlirContext, Contextual
from mlir_graph import MlirOp
from mlir_type import MlirType
from mlir_utils import (
    magma_type_to_mlir_type, magma_module_to_mlir_op, mlir_values_to_string)
from mlir_value import MlirValue


class ModuleInputSplitter(NodeTransformer, Contextual):
    def __init__(self, g: Graph, ctx: MlirContext):
        super().__init__(g)
        self._ctx = ctx

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
            t = magma_type_to_mlir_type(type(port))
            value = self.ctx.new_value(t, port.name, force=True)
            nodes.append(value)
            assert len(list(self.graph.predecessors(dst))) == 1
            for edge in self.graph.out_edges(dst, data=True):
                _, descendant, data = edge
                edges.append((value, descendant, data))
            nodes_to_remove.append(dst)
        for node in nodes_to_remove:
            self.graph.remove_node(node)
        return nodes, edges


class NetToValueTransformer(NodeTransformer, Contextual):
    def __init__(self, g: Graph, ctx: MlirContext):
        super().__init__(g)
        self._ctx = ctx

    def visit_Net(self, node: Net):
        assert len(list(self.graph.predecessors(node))) == 1
        t = magma_type_to_mlir_type(type(node.ports[0]))
        value = self.ctx.new_value(t)
        edges = list(replace_node(self.graph, node, value))
        return [value], edges


class EdgePortToIndexTransformer(NodeTransformer):
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


class ModuleToOpTransformer(NodeTransformer):
    def visit_MlirValue(self, node: MlirValue):
        return node

    def generic_visit(self, node: Node):
        assert isinstance(node, (m.DefineCircuitKind, m.Circuit))
        new_node = magma_module_to_mlir_op(node)
        edges = list(replace_node(self.graph, node, new_node))
        return [new_node], edges


def sort_values(g: Graph, node: MlirOp):
    inputs = {}
    outputs = {}
    for edge in g.in_edges(node, data=True):
        src, _, data = edge
        assert isinstance(src, MlirValue)
        idx = data["info"]
        assert idx not in inputs
        inputs[idx] = src
    for edge in g.out_edges(node, data=True):
        _, dst, data = edge
        assert isinstance(dst, MlirValue)
        idx = data["info"]
        assert idx not in outputs
        outputs[idx] = dst
    inputs = [inputs[i] for i in range(len(inputs))]
    outputs = [outputs[i] for i in range(len(outputs))]
    return inputs, outputs


class EmitMlirVisitor(NodeVisitor):
    def __init__(self, g: Graph, emitter: Emitter):
        super().__init__(g)
        self._emitter = emitter

    def visit_MlirValue(self, node: MlirValue):
        pass

    def generic_visit(self, node: MlirOp):
        assert isinstance(node, MlirOp)
        inputs, outputs = sort_values(self.graph, node)
        emission = node.emit()
        emission = emission.format(
            input_names=mlir_values_to_string(inputs, 0),
            output_names=mlir_values_to_string(outputs, 0),
            input_types=mlir_values_to_string(inputs, 1),
            output_types=mlir_values_to_string(outputs, 1))
        self._emitter.emit(emission)
