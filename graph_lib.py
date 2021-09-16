import networkx as nx
from typing import Any, Iterable


Graph = nx.MultiDiGraph
Node = Any


def topological_sort(g: Graph) -> Iterable[Any]:
    return nx.algorithms.dag.topological_sort(g)


def reverse_topological_sort(g: Graph) -> Iterable[Any]:
    return reversed(list(topological_sort(g)))


def write_to_dot(g: Graph, filename: str):
    nx.drawing.nx_pydot.write_dot(g, filename)
