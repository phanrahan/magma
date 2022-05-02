import dataclasses
from typing import Any, Callable, Tuple

from magma.array import Array
from magma.backend.mlir.graph_lib import Graph, write_to_dot
from magma.backend.mlir.magma_common import (
    ModuleLike, visit_value_or_value_wrapper_by_direction, safe_root,
    InstanceWrapper, get_compile_guard2s_of_module,
)
from magma.backend.mlir.magma_ops import (
    MagmaArrayGetOp, MagmaArraySliceOp, MagmaArrayCreateOp,
    MagmaTupleGetOp, MagmaTupleCreateOp,
    MagmaBitConstantOp, MagmaBitsConstantOp)
from magma.bits import Bits
from magma.circuit import DefineCircuitKind
from magma.common import Stack
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
        # try:
        #     return self._getter_cache[key]
        # except KeyError:
        #     pass
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
    assert driver is not None
    _visit_driver(ctx, value, driver, module)


def _visit_inputs(
        ctx: ModuleContext, module: ModuleLike, flatten_all_tuples: bool):
    for port in module.interface.ports.values():
        visit_value_or_value_wrapper_by_direction(
            port,
            lambda p: _visit_input(ctx, p, module),
            lambda _: None,
            flatten_all_tuples=flatten_all_tuples,
        )


def _postprocess_compile_guard2s(graph: Graph):
    for node in graph.nodes:
        guards = get_compile_guard2s_of_module(node)
        if not guards:
            continue
        ancestors_to_guard = []
        for succ in graph.successors(node):
            if not isinstance(succ, InstanceWrapper):
                continue
            ancestors_to_guard.append(succ)
            working_set = Stack()
            working_set.push(succ)
            while working_set:
                curr = working_set.pop()
                for ancestor in graph.successors(curr):
                    if not isinstance(ancestor, InstanceWrapper):
                        continue
                    working_set.push(ancestor)
                    ancestors_to_guard.append(ancestor)
        for ancestor in ancestors_to_guard:
            new_guards = ancestor.metadata.setdefault("compile_guard2s", guards)
            #assert new_guards == guards


def write_debug_magma_graph(graph: Graph, filename: str):
    from magma.circuit import DefineCircuitKind, Circuit
    from magma.t import Type
    from magma.backend.mlir.magma_common import InstanceWrapper, ValueWrapper

    debug_graph = Graph()

    def make_str(node):
        if isinstance(node, DefineCircuitKind):
            return node.name
        if isinstance(node, Circuit):
            return node.name
        if isinstance(node, Type):
            return repr(node)
        if isinstance(node, InstanceWrapper):
            return node.name + str(id(node))
        if isinstance(node, ValueWrapper):
            return node.name + str(node.id)
        return str(node)

    debug_graph.add_nodes_from(map(make_str, graph.nodes()))
    for src, dst, data in graph.edges(data=True):
        src, dst = map(make_str, (src, dst))
        label = str(data)
        if "info" in data:
            info = data["info"]
            label = f"{make_str(info['src'])} -> {make_str(info['dst'])}"
            #label = str({k: make_str(v) for k, v in info.items()})
            if "CLK" in label:
                continue
        debug_graph.add_edge(src, dst, label=label, key=label)

    write_to_dot(debug_graph, filename)


def build_magma_graph(
        ckt: DefineCircuitKind,
        opts: BuildMagmaGrahOpts = BuildMagmaGrahOpts()) -> Graph:
    ctx = ModuleContext(Graph(), opts)
    _visit_inputs(ctx, ckt, opts.flatten_all_tuples)
    for inst in ckt.instances:
        _visit_inputs(ctx, inst, opts.flatten_all_tuples)
    _postprocess_compile_guard2s(ctx.graph)
    return ctx.graph
