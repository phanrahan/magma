import dataclasses

import magma as m

from graph_base import Graph


def _get_inst_or_defn(value: m.Type):
    ref = value.name
    try:
        return ref.inst, True
    except AttributeError:
        pass
    return ref.defn, False


class MagmaNodeBase:
    pass


@dataclasses.dataclass(frozen=True)
class MagmaDefnNode(MagmaNodeBase):
    defn: m.DefineCircuitKind

    def __repr__(self):
        return f"{type(self).__name__}({self.defn.name})"


@dataclasses.dataclass(frozen=True)
class MagmaInstNode(MagmaNodeBase):
    inst: m.Circuit


class MagmaEdgeInfoBase:
    pass


@dataclasses.dataclass(frozen=True)
class MagmaConnectionEdgeInfo:
    src: m.Type
    dst: m.Type


def _traverse_inputs(g: Graph, interface: m.Interface, this: MagmaNodeBase):
    for port in interface.inputs():
        driver = port.trace()
        assert isinstance(driver.name, (m.ref.InstRef, m.ref.DefnRef))
        root, is_inst = _get_inst_or_defn(driver)
        if is_inst:
            neighbor = MagmaInstNode(root)
        else:
            neighbor = MagmaDefnNode(root)
        info = MagmaConnectionEdgeInfo(driver, port)
        g.add_edge(neighbor, this, info=info, label=str(info))


def build_magma_graph(ckt: m.DefineCircuitKind) -> Graph:
    g = Graph()
    g.add_node(MagmaDefnNode(ckt))
    for inst in ckt.instances:
        g.add_node(MagmaInstNode(inst))
    _traverse_inputs(g, ckt.interface, MagmaDefnNode(ckt))
    for inst in ckt.instances:
        _traverse_inputs(g, inst.interface, MagmaInstNode(inst))
    return g
