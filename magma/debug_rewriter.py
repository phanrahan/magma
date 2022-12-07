import inspect
import textwrap

import libcst as cst
from magma.t import Type
from magma.ref import AnonRef, NamedRef


class Transformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def leave_Assign(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:
        if len(updated_node.targets) != 1:
            # TODO: handle chained assigns
            return updated_node
        if not isinstance(updated_node.targets[0], cst.AssignTarget):
            # TODO: Handle this case
            return updated_node
        if not isinstance(updated_node.targets[0].target, cst.Name):
            return updated_node

        pos = self.get_metadata(cst.metadata.PositionProvider,
                                original_node).start
        value_str = cst.Module((cst.Expr(updated_node.value), )).code
        name = updated_node.targets[0].target.value
        targets = updated_node.targets + (
            cst.AssignTarget(cst.parse_expression(f"self.{name}")),
        )
        return updated_node.with_changes(targets=targets)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> bool:
        return True

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:
        return updated_node.with_changes(decorators=[])


def debug(fn):
    indented_program_txt = inspect.getsource(fn)
    program_txt = textwrap.dedent(indented_program_txt).lstrip()
    tree = cst.parse_module(program_txt)
    wrapper = cst.metadata.MetadataWrapper(tree)
    tree = wrapper.visit(Transformer())

    namespace = dict(**fn.__globals__)
    exec(tree.code, namespace)
    debug_fn = namespace[fn.__name__]

    def wrapper(*args, **kwargs):
        try:
            return debug_fn(*args, **kwargs)
        except Exception:
            # TODO: Namespace issues, need to inherite fn closure
            return fn(*args, **kwargs)
    return wrapper
