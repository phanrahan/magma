import dataclasses
from typing import Any, Tuple

from graph_base import Graph
from magma_graph import MagmaNodeBase, MagmaDefnNode, MagmaInstNode


class MlirNodeBase:
    pass


@dataclasses.dataclass(frozen=True)
class HwModuleNode(MlirNodeBase):
    name: str
    inputs: Tuple[Any]
    outputs: Tuple[Any]


@dataclasses.dataclass(frozen=True)
class CombOpNode(MlirNodeBase):
    name: str
    op: str


@dataclasses.dataclass(frozen=True)
class HwOutputNode(MlirNodeBase):
    name: str
    outputs: Tuple[Any]


class MlirEdgeInfoBase:
    pass


class MlirValueEdgeInfo(MlirEdgeInfoBase):
    pass


def make_mlir_op_node(node: MagmaInstNode):
    return CombOpNode(node.inst.name, "")


def lower_defn_node(g: Graph, node: MagmaDefnNode):
    defn = node.defn
    inputs = tuple(defn.interface.outputs())
    outputs = tuple(defn.interface.inputs())
    input_node = HwModuleNode(defn.name, inputs, outputs)
    output_node = HwOutputNode(defn.name, outputs)
    g.add_node(input_node)
    g.add_node(output_node)
    for out_edge in g.out_edges(node, data=True):
        _, dst, attrs = out_edge
        g.add_edge(input_node, dst, **attrs)
    for in_edge in g.in_edges(node, data=True):
        src, _, attrs = in_edge
        g.add_edge(src, output_node, **attrs)
    g.remove_node(node)


def lower_inst_node(g: Graph, node: MagmaInstNode):
    new = make_mlir_op_node(node)
    g.add_node(new)
    for incoming in g.in_edges(node, data=True):
        src, _, attrs = incoming
        g.add_edge(src, new, **attrs)
    for outgoing in g.out_edges(node, data=True):
        _, dst, attrs = outgoing
        g.add_edge(new, dst, **attrs)
    g.remove_node(node)


def lower_node(g: Graph, node: MagmaNodeBase):
    if isinstance(node, MagmaDefnNode):
        lower_defn_node(g, node)
        return
    if isinstance(node, MagmaInstNode):
        lower_inst_node(g, node)
        return
    raise NotImplementedError(node)


def lower_graph(g: Graph):
    nodes = list(g.nodes())
    for node in nodes:
        lower_node(g, node)
