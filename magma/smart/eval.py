import dataclasses
import networkx as nx
from typing import Any, Dict, Iterable, List, Optional, Set

from magma.bits import Bits
from magma.bitutils import clog2
from magma.common import MroVisitor, Stack
from magma.ref import TempNamedRef
from magma.smart.smart_bits import (
    SmartExprMeta,
    SmartExpr,
    SmartBitsExpr,
    SmartBits,
    issigned,
    SmartSignedOp,
    SmartExtendOp,
)


@dataclasses.dataclass(frozen=True)
class _Node:
    expr: SmartExpr
    children: List['_Node']

    def update(self, children: List['_Node']):
        self.children[:] = children

    __hash__ = object.__hash__


def _make_tree(expr: SmartExpr) -> _Node:
    children = list(_make_tree(arg) for arg in expr.args)
    return _Node(expr, children)


make_tree = _make_tree


class _Visitor(MroVisitor):
    def get_class(self, node: _Node) -> SmartExprMeta:
        return node.expr.__class__

    def generic_visit(self, node: _Node, *args, **kwargs):
        return list(
            self.visit(child, *args, **kwargs) for child in node.children
        )


class _Transformer(_Visitor):
    def generic_visit(self, node: _Node, *args, **kwargs):
        children = list(
            self.visit(child, *args, **kwargs) for child in node.children
        )
        node.update(children)
        return node


def _make_label(node: _Node) -> str:
    if isinstance(node.expr, SmartBitsExpr):
        return str(node.expr)
    label = str(node.expr)
    try:
        index = label.index("(")
    except ValueError:
        return label
    return label[:index]


def _write_debug_graph(root: _Node, filename: str):
    graph = nx.MultiDiGraph()
    stack = Stack()
    stack.push(root)
    while stack:
        node = stack.pop()
        graph.add_node(id(node), label=_make_label(node))
        for child in node.children:
            graph.add_edge(id(node), id(child))
            stack.push(child)
    nx.drawing.nx_pydot.write_dot(graph, filename)


write_debug_graph = _write_debug_graph


@dataclasses.dataclass(frozen=True)
class _Context:
    lhs: Optional[SmartBits]
    root: _Node

    def max_width(self, *widths) -> int:
        max_width = max(widths)
        if self.lhs is None:
            return max_width
        return max(max_width, len(self.lhs))


@dataclasses.dataclass
class _Partition:
    context: _Context
    nodes: Set[_Node] = dataclasses.field(default_factory=set, init=False)

    def add(self, node: _Node):
        self.nodes.add(node)


class _PartitionSet:
    def __init__(self):
        self._partitions = {}  # Dict[_Context, _Partition]
        self._context_lookup = {}  # Dict[_Node, _Context]

    def add(self, context: _Context, node: _Node):
        partition = self._partitions.setdefault(context, _Partition(context))
        partition.add(node)
        self._context_lookup[node] = context

    def get_nodes(self, context: _Context) -> Set[_Node]:
        return self._partitions[context].nodes

    def get_partition(self, node: _Node) -> _Partition:
        context = self._context_lookup[node]
        return self._partitions[context]

    def partitions(self) -> Iterable[_Partition]:
        return self._partitions.values()

    def debug_strings(self) -> Iterable[str]:
        for partition in self._partitions.values():
            yield f"Context: {str(partition.context)}"
            for node in partition.nodes:
                yield f"    {str(node)}"


class _PartitionGraph(_Visitor):
    def __init__(self, partitions: _PartitionSet):
        self._partitions = partitions

    def visit(self, node: _Node, context: _Context):
        self._partitions.add(context, node)
        super().visit(node, context)

    def visit_SmartComparisonOp(self, node: _Node, context: _Context):
        super().generic_visit(node, _Context(None, node))

    def visit_SmartShiftOp(self, node: _Node, context: _Context):
        self.visit(node.children[0], context)
        self.visit(node.children[1], _Context(None, node.children[1]))

    def visit_SmartExtendOp(self, node: _Node, context: _Context):
        for child in node.children:
            self.visit(child, _Context(None, child))

    def visit_SmartConcatOp(self, node: _Node, context: _Context):
        for child in node.children:
            self.visit(child, _Context(None, child))

    def visit_SmartMuxOp(self, node: _Node, context: _Context):
        for child in node.children:
            self.visit(child, _Context(None, child))

    def visit_SmartReductionOp(self, node: _Node, context: _Context):
        super().generic_visit(node, _Context(None, node))


def _max_width(partition: _Partition) -> int:
    leaves = filter(lambda n: len(n.children) == 0, partition.nodes)
    widths = (len(leaf.expr.bits) for leaf in leaves)
    return partition.context.max_width(*widths)


class _ResultWidthDeterminator(_Visitor):
    def __init__(self, partitions: _PartitionSet, widths: Dict[_Node, int]):
        self._partitions = partitions
        self._widths = widths

    def visit_SmartBitsExpr(self, node: _Node):
        self._widths[node] = len(node.expr.bits)

    def visit_SmartNAryContextualOp(self, node: _Node):
        super().generic_visit(node)
        partition = self._partitions.get_partition(node)
        self._widths[node] = _max_width(partition)

    def visit_SmartComparisonOp(self, node: _Node):
        super().generic_visit(node)
        self._widths[node] = 1

    def visit_SmartShiftOp(self, node: _Node):
        super().generic_visit(node)
        self._widths[node] = self._widths[node.children[0]]

    def visit_SmartConcatOp(self, node: _Node):
        super().generic_visit(node)
        self._widths[node] = sum(self._widths[child] for child in node.children)

    def visit_SmartMuxOp(self, node: _Node):
        super().generic_visit(node)
        self._widths[node] = max(self._widths[child] for child in node.children)

    def visit_SmartReductionOp(self, node: _Node):
        super().generic_visit(node)
        self._widths[node] = 1

    def visit_SmartSignedOp(self, node: _Node):
        super().generic_visit(node)
        self._widths[node] = self._widths[node.children[0]]

    def visit_SmartExtendOp(self, node: _Node):
        super().generic_visit(node)
        self._widths[node] = self._widths[node.children[0]]


class _ResultSignednessDeterminator(_Visitor):
    def __init__(self, signednesses: Dict[_Node, bool]):
        self._signednesses = signednesses

    def visit_SmartNAryContextualOp(self, node: _Node):
        super().generic_visit(node)
        signedness = all(self._signednesses[child] for child in node.children)
        self._signednesses[node] = signedness

    def visit_SmartComparisonOp(self, node: _Node):
        super().generic_visit(node)
        self._signednesses[node] = False

    def visit_SmartBitsExpr(self, node: _Node):
        self._signednesses[node] = issigned(node.expr.bits)

    def visit_SmartReductionOp(self, node: _Node):
        super().generic_visit(node)
        self._signednesses[node] = False

    def visit_SmartSignedOp(self, node: _Node):
        super().generic_visit(node)
        self._signednesses[node] = node.expr.op.signed

    def visit_SmartExtendOp(self, node: _Node):
        super().generic_visit(node)
        self._signednesses[node] = self._signednesses[node.children[0]]

    def visit_SmartConcatOp(self, node: _Node):
        super().generic_visit(node)
        self._signednesses[node] = False


class _SignednessInserter(_Transformer):
    def __init__(
            self,
            widths: Dict[_Node, int],
            signednesses: Dict[_Node, bool],
    ):
        self._widths = widths
        self._signednesses = signednesses

    def _insert_signed_op(self, node: _Node, signedness: bool) -> _Node:
        expr = SmartSignedOp(signedness, None)
        new_node = _Node(expr, [node])
        self._widths[new_node] = self._widths[node]
        self._signednesses[new_node] = signedness
        return new_node

    def visit_SmartNAryContextualOp(self, node: _Node) -> _Node:
        signedness = self._signednesses[node]
        children = [
            self._insert_signed_op(self.visit(child), signedness)
            for child in node.children
        ]
        node.update(children)
        return node

    def generic_visit(self, node: _Node) -> _Node:
        children = [
            self._insert_signed_op(self.visit(child), self._signednesses[child])
            for child in node.children
        ]
        node.update(children)
        return node


class _PushDownExtensions(_Transformer):
    def __init__(self, widths, signednesses):
        self._widths = widths
        self._signednesses = signednesses

    def _maybe_extend(self, child: _Node, width: int) -> _Node:
        diff = width - self._widths[child]
        if diff <= 0:
            return child
        signedness = self._signednesses[child]
        node = _Node(SmartExtendOp(diff, signedness, None), [child])
        self._widths[node] = width
        return node

    def visit_SmartNAryContextualOp(self, node: _Node) -> _Node:
        width = self._widths[node]
        children = [
            self._maybe_extend(self.visit(child), width)
            for child in node.children
        ]
        node.update(children)
        return node

    def visit_SmartComparisonOp(self, node: _Node) -> _Node:
        width = max(self._widths[child] for child in node.children)
        children = [
            self._maybe_extend(self.visit(child), width)
            for child in node.children
        ]
        node.update(children)
        return node

    def visit_SmartMuxOp(self, node: _Node) -> _Node:
        width = self._widths[node]
        children = [
            self._maybe_extend(self.visit(child), width)
            for child in node.children[:-1]
        ]
        sel_width = clog2(len(node.children) - 1)
        children.append(self._maybe_extend(node.children[-1], sel_width))
        node.update(children)
        return node


class _ShiftOperandWidthMatcher(_PushDownExtensions):
    def visit_SmartShiftOp(self, node: _Node) -> _Node:
        lchild, rchild = node.children
        lwidth, rwidth = map(self._widths.get, node.children)
        if lwidth == rwidth:
            return node
        if lwidth > rwidth:
            rchild = self._maybe_extend(rchild, lwidth)
            node.update([lchild, rchild])
            return node
        # TODO(rsetaluri): Figure out why this actually works...
        return node


class _Evaluator(_Visitor):
    def visit_SmartBitsExpr(self, node: _Node) -> Bits:
        return node.expr.bits.typed_value()

    def visit_SmartOp(self, node: _Node) -> Bits:
        operands = self.generic_visit(node)
        return node.expr.op(*operands)

    def visit_SmartMuxOp(self, node: _Node) -> Bits:
        operands = self.generic_visit(node)
        sel = operands.pop()
        sel_width = clog2(len(node.children) - 1)
        assert len(sel) >= sel_width
        if len(sel) > sel_width:
            sel = sel[:sel_width]
        return node.expr.op(*operands, sel)


def _determine_result_widths(lhs: SmartBits, root: _Node) -> Dict[_Node, int]:
    context = _Context(lhs, root)
    partitions = _PartitionSet()
    _PartitionGraph(partitions).visit(root, context)
    widths = {}
    _ResultWidthDeterminator(partitions, widths).visit(root)
    return widths


def _determine_result_signednesses(root: _Node) -> Dict[_Node, bool]:
    signednesses = {}
    _ResultSignednessDeterminator(signednesses).visit(root)
    return signednesses


def _insert_signednesses(
        root: _Node,
        widths: Dict[_Node, int],
        signednesses: Dict[_Node, bool],
) -> _Node:
    root = _SignednessInserter(widths, signednesses).visit(root)
    return root


def _push_down_extensions(
        root: _Node,
        widths: Dict[_Node, int],
        signednesses: Dict[_Node, int],
) -> _Node:
    root = _PushDownExtensions(widths, signednesses).visit(root)
    root = _ShiftOperandWidthMatcher(widths, signednesses).visit(root)
    return root


def _evaluate(root: _Node) -> Bits:
    return _Evaluator().visit(root)


def _force_width(value: SmartBits, width: int) -> SmartBits:
    diff = len(value) - width
    if diff == 0:
        return value
    value = value.typed_value()
    if diff > 0:
        value = value[:-diff]
    else:
        value = value.ext(-diff)
    return SmartBits.from_bits(value)


def evaluate_assignment(lhs: SmartBits, rhs: SmartExpr) -> SmartBits:
    root = make_tree(rhs)
    widths = _determine_result_widths(lhs, root)
    signednesses = _determine_result_signednesses(root)
    root = _insert_signednesses(root, widths, signednesses)
    root = _push_down_extensions(root, widths, signednesses)
    evaluated = SmartBits.from_bits(_evaluate(root))
    result = _force_width(evaluated, len(lhs))
    if not rhs.name or isinstance(rhs, SmartBits):
        return result
    # SmartExpr was given a lazy name, apply it now.
    temp = type(result).undirected_t(name=rhs.name)
    temp @= result
    return temp
