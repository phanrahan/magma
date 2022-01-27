import networkx as nx
from typing import Any, Callable, Iterable, List, Mapping, Tuple, Union


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


def _sort_cycle(
        cycle: List[Node], key: Callable[[Node], Any] = str) -> List[Node]:
    """
    Reorders @cycle by putting the lexicographically first (according to @key)
    element at index 0, and the remainder of the cycle in the remainder of the
    list.
    """
    size = len(cycle)
    if size == 0:
        return []
    min_index, min_value = 0, key(cycle[0])
    for index in range(1, size):
        value = key(cycle[index])
        if value == min_value:
            raise RuntimeError("Expected distinct keys")
        if value < min_value:
            min_index, min_value = index, value
    order = ((min_index + j) % size for j in range(size))
    return [cycle[i] for i in order]


def simple_cycles(g: Graph) -> Iterable[List[Node]]:
    cycles = nx.algorithms.cycles.simple_cycles(g)
    return map(_sort_cycle, cycles)
