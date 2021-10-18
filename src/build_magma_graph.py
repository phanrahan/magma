import dataclasses

import magma as m

from graph_lib import Graph
from magma_common import ModuleLike, make_instance, visit_value_by_direction
from magma_ops import (
    MagmaArrayGetOp, MagmaArraySliceOp, MagmaArrayCreateOp,
    MagmaProductGetOp, MagmaProductCreateOp,
    MagmaBitConstantOp, MagmaBitsConstantOp)


def _const_digital_to_bool(digital: m.Digital) -> bool:
    assert isinstance(digital, m.Digital)
    assert digital.const()
    T = type(digital)
    if digital is T.GND:
        return False
    assert digital is T.VCC
    return True


def _get_inst_or_defn_or_die(ref):
    try:
        return ref.inst
    except AttributeError:
        pass
    try:
        return ref.defn
    except AttributeError:
        pass
    assert False


def _visit_driver(g: Graph, value: m.Type, driver: m.Type, module):
    if driver.const():
        if isinstance(driver, m.Digital):
            as_bool = _const_digital_to_bool(driver)
            const = make_instance(MagmaBitConstantOp(type(driver), as_bool))
            info = dict(src=const.O, dst=value)
            g.add_edge(const, module, info=info)
            return
        if isinstance(driver, m.Bits):
            op = MagmaBitsConstantOp(type(driver), int(driver))
            const = make_instance(op)
            info = dict(src=const.O, dst=value)
            g.add_edge(const, module, info=info)
            return
    ref = driver.name
    if isinstance(ref, m.ref.InstRef):
        info = dict(src=driver, dst=value)
        g.add_edge(ref.inst, module, info=info)
        return
    if isinstance(ref, m.ref.DefnRef):
        info = dict(src=driver, dst=value)
        g.add_edge(ref.defn, module, info=info)
        return
    if isinstance(ref, m.ref.AnonRef):
        if isinstance(driver, m.Array):
            T = type(driver)
            creator = make_instance(MagmaArrayCreateOp(T))
            for i, element in enumerate(driver):
                creator_input = getattr(creator, f"I{i}")
                _visit_driver(g, creator_input, element, creator)
            info = dict(src=creator.O, dst=value)
            g.add_edge(creator, module, info=info)
            return
        if isinstance(driver, m.Product):
            T = type(driver)
            creator = make_instance(MagmaProductCreateOp(T))
            for k, t in T.field_dict.items():
                element = getattr(driver, k)
                creator_input = getattr(creator, f"I{k}")
                _visit_driver(g, creator_input, element, creator)
            info = dict(src=creator.O, dst=value)
            g.add_edge(creator, module, info=info)
            return
        raise NotImplementedError(driver, ref)
    if isinstance(ref, m.ref.ArrayRef):
        if ref.array.is_mixed():
            info=dict(src=driver, dst=value)
            src_module = _get_inst_or_defn_or_die(ref.array.name.root())
            g.add_edge(src_module, module, info=info)
            return
        T = type(ref.array)
        getter = make_instance(MagmaArrayGetOp(T), index=ref.index)
        _visit_driver(g, getter.I, ref.array, getter)
        info = dict(src=getter.O, dst=value)
        g.add_edge(getter, module, info=info)
        return
    if isinstance(ref, m.ref.TupleRef):
        if ref.tuple.is_mixed():
            info=dict(src=driver, dst=value)
            src_module = _get_inst_or_defn_or_die(ref.tuple.name.root())
            g.add_edge(src_module, module, info=info)
            return
        T = type(ref.tuple)
        getter = make_instance(MagmaProductGetOp(T, ref.index))
        _visit_driver(g, getter.I, ref.tuple, getter)
        info = dict(src=getter.O, dst=value)
        g.add_edge(getter, module, info=info)
        return
    raise NotImplementedError(driver, type(driver), ref, type(ref))


def _visit_input(g: Graph, value: m.Type, module: ModuleLike):
    driver = value.trace()
    assert driver is not None
    _visit_driver(g, value, driver, module)


def _visit_inputs(g: Graph, module: ModuleLike):
    for port in module.interface.ports.values():
        visit_value_by_direction(
            port,
            lambda p: _visit_input(g, p, module),
            lambda _: None
        )


def build_magma_graph(ckt: m.DefineCircuitKind) -> Graph:
    g = Graph()
    _visit_inputs(g, ckt)
    for inst in ckt.instances:
        _visit_inputs(g, inst)
    return g
