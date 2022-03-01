import networkx as nx
from typing import Any, Callable, Iterable, List, Mapping, Tuple, Union


Graph = nx.MultiDiGraph


def write_to_dot(g: Graph, filename: str):
    nx.drawing.nx_pydot.write_dot(g, filename)
