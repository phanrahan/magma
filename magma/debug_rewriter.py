import ast
import astor
import inspect

from magma.ast_utils import get_ast, compile_function_to_file
from magma.t import Type
from magma.ref import AnonRef, NamedRef


class DebugTransformer(ast.NodeTransformer):
    def __init__(self, filename):
        self.filename = filename

    def visit_Assign(self, node):
        if len(node.targets) > 1:
            raise NotImplementedError()

        assert len(node.targets) == 1
        if not isinstance(node.targets[0], ast.Name):
            return node
        node.value = ast.Call(
            ast.Attribute(ast.Attribute(ast.Name("m", ast.Load()),
                                        "debug_rewriter",
                                        ast.Load()),
                          "set_debug_info",
                          ast.Load()),
            [node.value, ast.Str(node.targets[0].id), ast.Str(self.filename),
             ast.Num(node.lineno), ast.Num(node.col_offset)],
            [],
            lineno=node.lineno,
            col_offset=node.col_offset
        )
        return node


def debug(fn):
    filename = inspect.getfile(fn)
    tree = get_ast(fn)
    assert len(tree.body[0].decorator_list) == 1
    tree.body[0].decorator_list = []
    tree = DebugTransformer(filename).visit(tree)
    # TODO(leonardt): gen_free_name for magma ref
    tree.body.insert(0, ast.parse("import magma as m").body[0])
    tree = ast.fix_missing_locations(tree)

    namespace = {}
    exec(compile(tree, filename, 'exec'), namespace)
    return namespace[fn.__name__]


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
