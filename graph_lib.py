import networkx as nx
from typing import Any, Callable, Iterable, Mapping, Tuple, Union


Graph = nx.MultiDiGraph
Node = Any
Edge = Union[Tuple[Node, Node], Tuple[Node, Node, Mapping]]
NodeOrderer = Callable[[Graph], Iterable[Any]]


def topological_sort(g: Graph) -> Iterable[Node]:
    return nx.algorithms.dag.topological_sort(g)


def reverse_topological_sort(g: Graph) -> Iterable[Node]:
    return reversed(list(topological_sort(g)))


def write_to_dot(g: Graph, filename: str):
    nx.drawing.nx_pydot.write_dot(g, filename)
