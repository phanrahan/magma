import dataclasses

import magma as m

from graph_lib import Graph
from magma_common import ModuleLike, make_instance
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


def _process_driver(g: Graph, value: m.Type, driver: m.Type, module):
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
                _process_driver(g, creator_input, element, creator)
            info = dict(src=creator.O, dst=value)
            g.add_edge(creator, module, info=info)
            return
        if isinstance(driver, m.Product):
            T = type(driver)
            creator = make_instance(MagmaProductCreateOp(T))
            for k, t in T.field_dict.items():
                element = getattr(driver, k)
                creator_input = getattr(creator, f"I{k}")
                _process_driver(g, creator_input, element, creator)
            info = dict(src=creator.O, dst=value)
            g.add_edge(creator, module, info=info)
            return
        raise NotImplementedError(driver, ref)
    if isinstance(ref, m.ref.ArrayRef):
        T = type(ref.array)
        getter = make_instance(MagmaArrayGetOp(T), index=ref.index)
        _process_driver(g, getter.I, ref.array, getter)
        info = dict(src=getter.O, dst=value)
        g.add_edge(getter, module, info=info)
        return
    if isinstance(ref, m.ref.TupleRef):
        T = type(ref.tuple)
        getter = make_instance(MagmaProductGetOp(T, ref.index))
        _process_driver(g, getter.I, ref.tuple, getter)
        info = dict(src=getter.O, dst=value)
        g.add_edge(getter, module, info=info)
        return
    raise NotImplementedError(driver, type(driver), ref, type(ref))


def _traverse_input(g: Graph, value: m.Type, module):
    driver = value.trace()
    assert driver is not None
    _process_driver(g, value, driver, module)


def _traverse_inputs(g: Graph, module: ModuleLike):
    for port in module.interface.inputs(include_clocks=True):
        _traverse_input(g, port, module)


def build_magma_graph(ckt: m.DefineCircuitKind) -> Graph:
    g = Graph()
    _traverse_inputs(g, ckt)
    for inst in ckt.instances:
        _traverse_inputs(g, inst)
    return g
