import dataclasses
from typing import Any, Optional, Tuple

from graph_base import Graph, topological_sort
from graph_utils import NodeTransformer
from magma_graph import MagmaNodeBase, MagmaDefnNode, MagmaInstNode, MagmaConnectionEdgeInfo


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


@dataclasses.dataclass(frozen=True)
class MlirValueEdgeInfo(MlirEdgeInfoBase):
    src_key: Any
    dst_key: Any
    value: str


class SplitMagmaDefnNodeTransformer(NodeTransformer):
    def __init__(self, g: Graph):
        super().__init__(g)
        self.nodes = None

    def visit_MagmaDefnNode(self, node: MagmaDefnNode):
        assert isinstance(node, MagmaDefnNode)
        if self.nodes is not None:
            raise TypeError()
        defn = node.defn
        inputs = tuple(defn.interface.outputs())
        outputs = tuple(defn.interface.inputs())
        input_node = HwModuleNode(defn.name, inputs, outputs)
        output_node = HwOutputNode(defn.name, outputs)
        nodes = self.nodes = [input_node, output_node]
        edges = []
        for out_edge in self.graph.out_edges(node, data=True):
            _, dst, attrs = out_edge
            edges.append((input_node, dst, attrs))
        for in_edge in self.graph.in_edges(node, data=True):
            src, _, attrs = in_edge
            edges.append((src, output_node, attrs))
        return nodes, edges


def make_mlir_op_node(node: MagmaInstNode):
    return CombOpNode(node.inst.name, "")


idx = 0
def make_mlir_value_edge_info(info: MagmaConnectionEdgeInfo):

    def root(value):
        ref = value.name
        try:
            return ref.inst, True
        except AttributeError:
            pass
        return ref.defn, False

    def get_index(ports, value):
        for i, port in enumerate(ports):
            if port is value:
                return i
        raise KeyError()

    src_root = root(info.src)[0]
    dst_root = root(info.dst)[0]
    src_key = get_index(root(info.src)[0].interface.outputs(), info.src)
    dst_key = get_index(root(info.dst)[0].interface.inputs(), info.dst)
    global idx
    value = f"%{idx}__{info.src.name}"
    idx += 1
    print (src_key, dst_key, value)
    return MlirValueEdgeInfo(src_key, dst_key, value)


class LowerMagmaInstNodeTransformer(NodeTransformer):
    def _generic_visit(self, node: Any, new_node: Optional[Any]):
        if new_node is None:
            new_node = node
        edges = list(self.graph.in_edges(node, data=True))
        for outgoing in self.graph.out_edges(node, data=True):
            _, dst, attrs = outgoing
            info = make_mlir_value_edge_info(attrs["info"])
            attrs = dict(info=info, label=str(info))
            edges.append((new_node, dst, attrs))
        return [new_node], edges
    
    def generic_visit(self, node: Any):
        return self._generic_visit(node, None)

    def visit_MagmaInstNode(self, node: MagmaInstNode):
        return self.generic_visit(node)
        assert isinstance(node, MagmaInstNode)
        new_node = make_mlir_op_node(node)
        return self._generic_visit(node, new_node)


def lower_node(g: Graph, node: MagmaNodeBase):
    if isinstance(node, MagmaDefnNode):
        lower_defn_node(g, node)
        return
    if isinstance(node, MagmaInstNode):
        lower_inst_node(g, node)
        return
    raise NotImplementedError(node)


def lower_graph(g: Graph):
    return
    SplitMagmaDefnNodeTransformer(g).run()
    LowerMagmaInstNodeTransformer(g).run(topological_sort)
    return
    
    nodes = list(g.nodes())
    for node in nodes:
        lower_node(g, node)
