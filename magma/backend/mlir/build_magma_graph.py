import dataclasses

from magma.array import Array
from magma.backend.mlir.graph_lib import Graph
from magma.backend.mlir.magma_common import (
    ModuleLike, visit_value_or_value_wrapper_by_direction, safe_root)
from magma.backend.mlir.magma_ops import (
    MagmaArrayGetOp, MagmaArraySliceOp, MagmaArrayCreateOp,
    MagmaTupleGetOp, MagmaTupleCreateOp,
    MagmaBitConstantOp, MagmaBitsConstantOp)
from magma.bits import Bits
from magma.circuit import DefineCircuitKind
from magma.digital import Digital
from magma.ref import InstRef, DefnRef, AnonRef, ArrayRef, TupleRef
from magma.t import Type
from magma.tuple import Tuple as m_Tuple


def _const_digital_to_bool(digital: Digital) -> bool:
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


class ModuleContext:
    def __init__(self, graph: Graph):
        self._graph = graph
        self._getter_cache = {}

    @property
    def graph(self) -> Graph:
        return self._graph

    @property
    def getter_cache(self):
        return self._getter_cache


def _visit_driver(
        ctx: ModuleContext, value: Type, driver: Type, module: ModuleLike):
    if driver.const():
        if isinstance(driver, Digital):
            as_bool = _const_digital_to_bool(driver)
            const = MagmaBitConstantOp(type(driver), as_bool)
            info = dict(src=const.O, dst=value)
            ctx.graph.add_edge(const, module, info=info)
            return
        if isinstance(driver, Bits):
            const = MagmaBitsConstantOp(type(driver), int(driver))
            info = dict(src=const.O, dst=value)
            ctx.graph.add_edge(const, module, info=info)
            return
    ref = driver.name
    if isinstance(ref, InstRef):
        info = dict(src=driver, dst=value)
        ctx.graph.add_edge(ref.inst, module, info=info)
        return
    if isinstance(ref, DefnRef):
        info = dict(src=driver, dst=value)
        ctx.graph.add_edge(ref.defn, module, info=info)
        return
    if isinstance(ref, AnonRef):
        if isinstance(driver, Array):
            T = type(driver)
            creator = MagmaArrayCreateOp(T)
            for i, element in enumerate(driver):
                creator_input = getattr(creator, f"I{i}")
                _visit_driver(ctx, creator_input, element, creator)
            info = dict(src=creator.O, dst=value)
            ctx.graph.add_edge(creator, module, info=info)
            return
        if isinstance(driver, m_Tuple):
            T = type(driver)
            creator = MagmaTupleCreateOp(T)
            for k, element in driver.items():
                creator_input = getattr(creator, f"I{k}")
                _visit_driver(ctx, creator_input, element, creator)
            info = dict(src=creator.O, dst=value)
            ctx.graph.add_edge(creator, module, info=info)
            return
        raise NotImplementedError(driver, ref)
    if isinstance(ref, ArrayRef):
        if ref.array.is_mixed():
            info = dict(src=driver, dst=value)
            src_module = _get_inst_or_defn_or_die(safe_root(ref.array.name))
            ctx.graph.add_edge(src_module, module, info=info)
            return
        cache_key = (ref.array, ref.index)
        try:
            getter = ctx.getter_cache[cache_key]
        except KeyError:
            T = type(ref.array)
            getter = MagmaArrayGetOp(T, ref.index)
            _visit_driver(ctx, getter.I, ref.array, getter)
            ctx.getter_cache[cache_key] = getter
        info = dict(src=getter.O, dst=value)
        ctx.graph.add_edge(getter, module, info=info)
        return
    if isinstance(ref, TupleRef):
        if ref.tuple.is_mixed():
            info = dict(src=driver, dst=value)
            src_module = _get_inst_or_defn_or_die(safe_root(ref.tuple.name))
            ctx.graph.add_edge(src_module, module, info=info)
            return
        cache_key = (ref.tuple, ref.index)
        try:
            getter = ctx.getter_cache[cache_key]
        except KeyError:
            T = type(ref.tuple)
            getter = MagmaTupleGetOp(T, ref.index)
            _visit_driver(ctx, getter.I, ref.tuple, getter)
            ctx.getter_cache[cache_key] = getter
        info = dict(src=getter.O, dst=value)
        ctx.graph.add_edge(getter, module, info=info)
        return
    raise NotImplementedError(driver, type(driver), ref, type(ref))


def _visit_input(ctx: ModuleContext, value: Type, module: ModuleLike):
    driver = value.trace()
    assert driver is not None
    _visit_driver(ctx, value, driver, module)


def _visit_inputs(ctx: ModuleContext, module: ModuleLike):
    for port in module.interface.ports.values():
        visit_value_or_value_wrapper_by_direction(
            port,
            lambda p: _visit_input(ctx, p, module),
            lambda _: None
        )


def build_magma_graph(ckt: DefineCircuitKind) -> Graph:
    ctx = ModuleContext(Graph())
    _visit_inputs(ctx, ckt)
    for inst in ckt.instances:
        _visit_inputs(ctx, inst)
    return ctx.graph
