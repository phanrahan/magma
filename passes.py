import dataclasses
from typing import Tuple

import magma as m

from graph_lib import Graph, Node, topological_sort
from visitor import NodeTransformer


class SplitPortEdgesTranformer(NodeTransformer):
    def generic_visit(self, node: Node):
        edges = list(self.graph.in_edges(node, data=True))
        nodes = [node]
        for edge in self.graph.out_edges(node, data=True):
            src, dst, data = edge
            info = data["info"]
            src_port, dst_port = info["src"], info["dst"]            
            nodes.append(src_port)
            nodes.append(dst_port)
            edges.append((src, src_port, {}))
            edges.append((src_port, dst_port, {}))
            edges.append((dst_port, dst, {}))
        return nodes, edges


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


@dataclasses.dataclass(frozen=True)
class Net:
    ports: Tuple


class NetMerger(NodeTransformer):
    def _make_new_node(node: Node, predecessor: Node):
        if isinstance(predecessor, m.Type):
            return Net((predecessor, node))
        if isinstance(predecessor, Net):
            ports = tuple(list(predecessor.ports) + [node])
            return Net(ports)
        return None
    
    def generic_visit(self, node: Node):
        if not isinstance(node, m.Type):
            return node
        predecessors = list(self.graph.predecessors(node))
        assert len(predecessors) == 1
        predecessor = predecessors[0]
        new_node = NetMerger._make_new_node(node, predecessor)
        if new_node is None:
            return node
        edges = []
        for edge in self.graph.in_edges(predecessor, data=True):
            src, _, data = edge
            data.setdefault("info", predecessor)
            edges.append((src, new_node, data))
        for edge in self.graph.out_edges(predecessor, data=True):
            _, dst, data = edge
            if dst is node:
                continue
            data.setdefault("info", None)
            edges.append((new_node, dst, data))
        for edge in self.graph.out_edges(node, data=True):
            _, dst, data = edge
            data.setdefault("info", node)
            edges.append((new_node, dst, data))        
        self.graph.remove_node(predecessor)
        return [new_node], edges
