import astor
from staticfg import CFGBuilder
import ast
from ..ast_utils import get_ast


def is_yield(statement):
    return (isinstance(statement, ast.Expr) and \
            isinstance(statement.value, ast.Yield))


def collect_paths_to_yield(start_idx, block):
    path = []
    for statement in block.statements[start_idx:]:
        if is_yield(statement):
            return path
        else:
            path.append(statement)
    return sum(path + p for p in  collect_paths_to_yield(0, exit.target) for
               exit in block.exits)


def coroutine(fn):
    tree = get_ast(fn).body[0]
    call_method = tree.body[1]
    cfg = CFGBuilder().build(call_method.name, call_method)
    # cfg.build_visual(tree.name, 'pdf')
    paths = {}
    for block in cfg:
        for i, statement in enumerate(block.statements):
            if is_yield(statement):
                paths = collect_paths_to_yield(i + 1, block)
                print(paths)
    raise Exception()

