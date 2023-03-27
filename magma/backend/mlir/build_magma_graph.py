import dataclasses
from typing import Any, Callable, Tuple

from magma.array import Array
from magma.backend.mlir.errors import MlirWhenCycleError
from magma.backend.mlir.graph_lib import Graph
from magma.backend.mlir.magma_common import (
    ModuleLike, visit_value_or_value_wrapper_by_direction, safe_root,
    InstanceWrapper,
)
from magma.backend.mlir.magma_ops import (
    MagmaArrayGetOp, MagmaArraySliceOp, MagmaArrayCreateOp,
    MagmaTupleGetOp, MagmaTupleCreateOp,
    MagmaBitConstantOp, MagmaBitsConstantOp)
from magma.bits import Bits
from magma.circuit import DefineCircuitKind
from magma.compile_exception import UnconnectedPortException
from magma.digital import Digital
from magma.primitives.register import Register
from magma.primitives.when import iswhen
from magma.protocol_type import magma_value as get_magma_value
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


@dataclasses.dataclass(frozen=True)
class BuildMagmaGrahOpts:
    flatten_all_tuples: bool = False


class ModuleContext:
    def __init__(self, graph: Graph, opts: BuildMagmaGrahOpts):
        self._graph = graph
        self._opts = opts
        self._getter_cache = {}

    @property
    def graph(self) -> Graph:
        return self._graph

    @property
    def opts(self) -> BuildMagmaGrahOpts:
        return self._opts

    def get_or_make_getter(
            self,
            value: Type,
            index: Any,
            op_maker: Callable,
            args: Tuple[Any]) -> InstanceWrapper:
        key = (value, index)
        try:
            return self._getter_cache[key]
        except KeyError:
            pass
        getter = op_maker(type(value), *args)
        _visit_driver(self, getter.I, value, getter)
        self._getter_cache[key] = getter
        return getter


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
            creator = MagmaArrayCreateOp(driver)
            for i, element in driver._enumerate_children():
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
        index = ref.index
        if isinstance(index, slice):
            assert index.step is None
            assert index.start <= index.stop
            index = index.start, index.stop
            getter_cls, getter_args = MagmaArraySliceOp, index
        else:
            getter_cls, getter_args = MagmaArrayGetOp, (index,)
        getter = ctx.get_or_make_getter(
            ref.array, index, getter_cls, getter_args)
        info = dict(src=getter.O, dst=value)
        ctx.graph.add_edge(getter, module, info=info)
        return
    if isinstance(ref, TupleRef):
        if ref.tuple.is_mixed() or ctx.opts.flatten_all_tuples:
            info = dict(src=driver, dst=value)
            src_module = _get_inst_or_defn_or_die(safe_root(ref.tuple.name))
            ctx.graph.add_edge(src_module, module, info=info)
            return
        getter = ctx.get_or_make_getter(
            ref.tuple, ref.index, MagmaTupleGetOp, (ref.index,))
        info = dict(src=getter.O, dst=value)
        ctx.graph.add_edge(getter, module, info=info)
        return
    raise NotImplementedError(driver, type(driver), ref, type(ref))


def _visit_input(ctx: ModuleContext, value: Type, module: ModuleLike):
    driver = value.trace()
    if driver is None:
        raise UnconnectedPortException(value)
    _visit_driver(ctx, value, driver, module)


def _visit_inputs(
        ctx: ModuleContext, module: ModuleLike, flatten_all_tuples: bool):
    for port in module.interface.ports.values():
        port = get_magma_value(port)
        visit_value_or_value_wrapper_by_direction(
            port,
            lambda p: _visit_input(ctx, p, module),
            lambda _: None,
            flatten_all_tuples=flatten_all_tuples,
        )


def _check_for_when_cycles(graph: Graph):
    """Temporary guard against https://github.com/phanrahan/magma/issues/1248"""
    for node in graph.nodes():
        if not iswhen(node):
            continue
        for predecessor in graph.predecessors(node):
            if isinstance(type(node), Register):  # registers break cycles
                break
            if predecessor is node:
                raise MlirWhenCycleError()


def build_magma_graph(
        ckt: DefineCircuitKind,
        opts: BuildMagmaGrahOpts = BuildMagmaGrahOpts()) -> Graph:
    ctx = ModuleContext(Graph(), opts)
    _visit_inputs(ctx, ckt, opts.flatten_all_tuples)
    for inst in ckt.instances:
        _visit_inputs(ctx, inst, opts.flatten_all_tuples)
    _check_for_when_cycles(ctx.graph)
    return ctx.graph
