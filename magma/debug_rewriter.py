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
            ast.Attribute(ast.Attribute(ast.Name("m"), "debug_rewriter",
                                        ast.Load()), "set_name", ast.Load()),
            [node.value, ast.Str(node.targets[0].id), ast.Str(self.filename),
             ast.Num(node.lineno)],
            []
        )
        return node


def get_filename(fn):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    return module.__file__


def debug(fn):
    filename = get_filename(fn)
    tree = get_ast(fn)
    assert len(tree.body[0].decorator_list) == 1
    tree.body[0].decorator_list = []
    tree = DebugTransformer(filename).visit(tree)
    # TODO(leonardt): gen_free_name for magma ref
    tree.body.insert(0, ast.parse("import magma as m").body[0])
    return compile_function_to_file(tree, fn.__name__)
    return fn


def set_name(value, name, filename, lineno):
    if not isinstance(value, Type):
        return
    if not isinstance(value.name, AnonRef):
        return
    value.name = NamedRef(name)
    value.filename = filename
    value.lineno = lineno
    return value
