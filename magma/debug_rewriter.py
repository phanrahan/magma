import inspect
import textwrap

import libcst as cst
from magma.t import Type
from magma.ref import AnonRef, NamedRef


class Transformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def leave_Assign(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:
        assert len(updated_node.targets) == 1
        assert isinstance(updated_node.targets[0], cst.AssignTarget)
        if not isinstance(updated_node.targets[0].target, cst.Name):
            return updated_node

        pos = self.get_metadata(cst.metadata.PositionProvider,
                                original_node).start
        value_str = cst.Module((cst.Expr(updated_node.value), )).code
        name = updated_node.targets[0].target.value
        tree = cst.parse_expression(
            f"m.debug_rewriter.set_debug_info({value_str}, \"{name}\", "
            f"\"{self.filename}\", {pos.line}, {pos.column})"
        )
        return updated_node.with_changes(value=tree)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> bool:
        return True

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:
        return updated_node.with_changes(decorators=[])


def debug(fn):
    filename = inspect.getfile(fn)
    indented_program_txt = inspect.getsource(fn)
    program_txt = textwrap.dedent(indented_program_txt)
    tree = cst.parse_module(program_txt)
    wrapper = cst.metadata.MetadataWrapper(tree)
    tree = wrapper.visit(Transformer(filename))
    code = "import magma as m\n" + tree.code

    namespace = {}
    exec(code, namespace)
    debug_fn = namespace[fn.__name__]

    def wrapper(*args, **kwargs):
        try:
            return debug_fn(*args, **kwargs)
        except Exception:
            return fn(*args, **kwargs)
    return wrapper


def set_debug_info(value, name, filename, lineno, col_offset):
    if not isinstance(value, Type):
        return
    if not isinstance(value.name, AnonRef):
        return
    value.name = NamedRef(name)
    value.filename = filename
    value.lineno = lineno
    value.col_offset = col_offset
    return value
