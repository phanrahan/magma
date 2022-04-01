import ast
import astor
import functools

from magma.ast_utils import get_ast


class ClsReferenceCollector(ast.NodeVisitor):
    def __init__(self):
        self.references = set()

    def _get_leaf(self, node):
        if isinstance(node, ast.Attribute):
            return self._get_leaf(node.value)
        return node

    def _get_attrs(self, node):
        if isinstance(node, ast.Attribute):
            return self._get_attrs(node.value) + (node.attr, )
        assert isinstance(node, ast.Name) and node.id == "cls"
        return tuple()

    def visit_Attribute(self, node):
        leaf = self._get_leaf(node.value)
        if not (isinstance(leaf, ast.Name) and leaf.id == "cls"):
            return
        self.references.add(self._get_attrs(node))


def inline_combinational2(fn):
    fn._magma_inline_combinational_ = True
    return fn


def process_inline_comb_fn(defn, fn):
    tree = get_ast(fn)
    collector = ClsReferenceCollector()
    collector.visit(tree)
    values = []
    for ref in collector.references:
        values.append(functools.reduce(lambda x, y: getattr(x, y), ref, defn))

    import magma as m  # TODO(leonardt): Can we avoid this circular ref?

    class InlineCombWrapper(m.Circuit):
        io = m.IO()
        for i, value in enumerate(values):
            io += m.IO(**{f"v{i}": type(value).flip()})
        for i, value in enumerate(values):
            if value.is_input():
                getattr(io, f"v{i}").undriven()
        _magma_inline_combinational_ast_ = tree
        m.inline_verilog("// " +
                         "\n// ".join(astor.to_source(tree).splitlines()))

    inst = InlineCombWrapper()
    for i, value in enumerate(values):
        m.wire(getattr(inst, f"v{i}"), value)
