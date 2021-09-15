from graph_base import Graph, topological_sort
from graph_utils import NodeTransformer


class InsertPortNodeTransformer(NodeTransformer):
    def visit_generic(self, node):
        
