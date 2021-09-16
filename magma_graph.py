from typing import Union

import magma as m

from graph_lib import Graph


ModuleLike = Union[m.DefineCircuitKind, m.Circuit]


def _get_inst_or_defn_or_die(value: m.Type) -> ModuleLike:
    ref = value.name
    try:
        return ref.inst, True
    except AttributeError:
        pass
    return ref.defn, False


def _traverse_inputs(g: Graph, module: ModuleLike):
    for port in module.interface.inputs():
        driver = port.trace()
        assert isinstance(driver.name, (m.ref.InstRef, m.ref.DefnRef))
        root, _ = _get_inst_or_defn_or_die(driver)
        info = dict(src=driver, dst=port)
        g.add_edge(root, module, info=info)


def build_magma_graph(ckt: m.DefineCircuitKind) -> Graph:
    g = Graph()
    _traverse_inputs(g, ckt)
    for inst in ckt.instances:
        _traverse_inputs(g, inst)
    return g
