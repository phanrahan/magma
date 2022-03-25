from magma.backend.mlir.magma_common import (
    value_or_value_wrapper_to_tree as magma_value_or_value_wrapper_to_tree
)


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


def _get_leaf_descendants(tree, node, include_self=False):
    is_leaf = True
    for succ in tree.successors(node):
        is_leaf = False
        yield from _get_leaf_descendants(tree, succ, include_self=True)
    if is_leaf and include_self:
        yield node


def _advance(it):
    next(it)
    return it


def get_xmr_paths(ctx, xmr):
    root = xmr.port.name.root().value()
    tree = magma_value_or_value_wrapper_to_tree(
        root, flatten_all_tuples=ctx.opts.flatten_all_tuples)
    assert tree.has_node(root)

    # (1)
    if tree.has_node(xmr.port):  # visited
        path = _path_to_string(_get_path(tree, xmr.port), "_")
        # (1a)
        if tree.out_degree(xmr.port) == 0:  # is leaf
            return [(path,)]
        # (1b)
        leaves = _get_leaf_descendants(tree, xmr.port)
        leaves = sorted(leaves, key=lambda n: tree.nodes[n]["index"])
        return [
            (_path_to_string(_get_path(tree, leaf), "_"),)
            for leaf in leaves
        ]
    # (2)
    for leaf in _get_leaf_descendants(tree, root, include_self=True):
        subtree = magma_value_or_value_wrapper_to_tree(
            leaf, flatten_all_tuples=True)
        if not subtree.has_node(xmr.port):
            continue
        path = (_path_to_string(_get_path(tree, leaf), "_"),)
        path = path + tuple(
            v.name.index for v in _advance(iter(_get_path(subtree, xmr.port)))
        )
        return [path]
