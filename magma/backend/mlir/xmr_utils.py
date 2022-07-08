from typing import List, Tuple

from magma.backend.mlir.magma_common import (
    value_or_value_wrapper_to_tree as magma_value_or_value_wrapper_to_tree
)
from magma.ref import TupleRef, ArrayRef
from magma.view import PortView


def _get_path(tree, node):
    predecessors = tree.predecessors(node)
    try:
        parent = next(predecessors)
    except StopIteration:
        return [node]
    try:
        next(predecessors)
        raise RuntimeError()
    except StopIteration:
        pass
    return _get_path(tree, parent) + [node]


def _path_to_string(path, seperator):
    path = [str(path[0])] + [str(v.name.index) for v in path[1:]]
    return seperator.join(path)


def _get_path_string(tree, node, seperator):
    path = _get_path(tree, node)
    return _path_to_string(path, seperator)


def _get_leaf_descendants(tree, node, include_self=False):
    succ = None
    for succ in tree.successors(node):
        yield from _get_leaf_descendants(tree, succ, include_self=True)
    is_leaf = succ is None
    if is_leaf and include_self:
        yield node


def _find(lst, elt):
    for lst_elt in lst:
        if lst_elt is elt:
            return elt
    return None


def _ascend_to_leaf(value, leaves):
    leaf = _find(leaves, value)
    if leaf is not None:
        return [leaf]
    ref = value.name
    if isinstance(ref, TupleRef):
        path = _ascend_to_leaf(ref.tuple, leaves)
        return path + [f".{ref.index}"]
    if isinstance(ref, ArrayRef):
        path = _ascend_to_leaf(ref.array, leaves)
        return path + [f"[{ref.index}]"]
    raise TypeError(ref, value)


def get_xmr_paths(ctx: 'HardwareModule', xmr: PortView) -> List[Tuple[str]]:
    # We obtain the path to @xmr as follows. (Note that this function only
    # computes the path for the value itself, i.e. the path to the instance in
    # the hierarchy should be computed by the caller.)
    #
    # First, we consider the nested type of the value of which the referred port
    # is a part, as a tree, where array and tuple types result in branches. For
    # example, if the value referred to is `x.y[0].z`, then we build the tree
    # for `x`. The tree construction depends on whether or not we flatten
    # tuples. For example, if we don't flatten tuples, then Tuples are leaves;
    # otherwise, their children are expanded as branches.
    #
    # Next we consider 2 cases:
    # (1) The value referred to is explicitly a node in the constructed tree.
    #     From here, we consider 2 subcases:
    #     (1a) The value referred to is a leaf. In this case, the path is simply
    #          the path to this leaf joined by "_" (since the branches represent
    #          flattening of tuples and arrays).
    #     (1b) Otherwise, we need to consider all leaves which are descendants
    #          of the value referred to. For each such leaf, we compute the path
    #          as in (1a), and return a list of these paths.
    # (2) The value referred to is *not* a node in the constructed tree. This
    #     may happen if the value referred to is a child of a tuple or array
    #     that is not flattened. In this case we need to find the leaf for which
    #     the value referred to is an ancestor. There should be exactly one such
    #     leaf. Then we compute the path as the path to the leaf as computed in
    #     (1a) (i.e. joined with "_"). Then we concatenate the path from this
    #     leaf to the value referred to, joined with ".", since these are not
    #     flattened.
    root = xmr.port.name.root().value()
    tree = magma_value_or_value_wrapper_to_tree(
        root, flatten_all_tuples=ctx.opts.flatten_all_tuples)
    assert tree.has_node(root)

    # (1)
    if tree.has_node(xmr.port):  # visited
        path = _get_path_string(tree, xmr.port, "_")
        # (1a)
        if tree.out_degree(xmr.port) == 0:  # is leaf
            return [(path,)]
        # (1b)
        leaves = _get_leaf_descendants(tree, xmr.port)
        leaves = sorted(leaves, key=lambda n: tree.nodes[n]["index"])
        return [
            (_get_path_string(tree, leaf, "_"),)
            for leaf in leaves
        ]
    # (2)
    leaves = list(_get_leaf_descendants(tree, root, include_self=True))
    leaf, *path = _ascend_to_leaf(xmr.port, leaves)
    path = _get_path_string(tree, leaf, "_") + "".join(path)
    return [(path,)]
