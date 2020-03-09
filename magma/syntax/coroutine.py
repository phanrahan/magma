import ast
import copy

import astor
from staticfg import CFGBuilder
from staticfg.builder import invert

from ..ast_utils import get_ast
from ..bitutils import clog2


class RemoveIfTrues(ast.NodeTransformer):
    def visit_If(self, node):
        if isinstance(node.test, ast.NameConstant) and node.test.value is True:
            return node.body
        return self.generic_visit(node)


class MergeInverseIf(ast.NodeTransformer):
    def visit(self, node):
        if hasattr(node, 'body'):
            node.body = self.visit_body(node.body)
        return self.generic_visit(node)

    def visit_body(self, body):
        new_body = []
        skip_next = False
        for i, node in enumerate(body):
            if skip_next:
                continue
            new_body.append(node)
            if i == len(body) - 1:
                break
            if (isinstance(node, ast.If) and isinstance(body[i + 1], ast.If)
                    and ast.dump(invert(node.test)) ==
                        ast.dump(body[i + 1].test)):
                node.orelse = body[i + 1].body
                skip_next = True
            else:
                skip_next = False
        return new_body



def is_yield(statement):
    return (isinstance(statement, ast.Expr) and \
            isinstance(statement.value, ast.Yield))


def collect_paths_to_yield(start_idx, block):
    path = []
    for statement in block.statements[start_idx:]:
        path.append(statement)
        if is_yield(statement):
            return [path]
    paths = []
    for exit in block.exits:
        _path = path
        if exit.exitcase is not None:
            assert len(_path) == 1
            _path = _path.copy()
            _path[0] = copy.copy(_path[0])
            _path[0].exitcase = exit.exitcase
        paths.extend(_path + p for p in collect_paths_to_yield(0, exit.target))
    return paths


def coroutine(fn):
    tree = get_ast(fn).body[0]
    assert (isinstance(tree.body[0], ast.FunctionDef) and
            tree.body[0].name == "__init__")
    assert (isinstance(tree.body[1], ast.FunctionDef) and
            tree.body[1].name == "__call__")
    call_method = tree.body[1]
    # insert while true
    call_method.body = [ast.While(ast.NameConstant(True), call_method.body, [])]
    cfg = CFGBuilder().build(call_method.name, call_method)
    # cfg.build_visual(tree.name, 'pdf')
    yield_paths = {}
    yield_id_map = {}
    for block in cfg:
        for i, statement in enumerate(block.statements):
            if is_yield(statement):
                yield_id_map[statement] = len(yield_id_map)
                paths = collect_paths_to_yield(i + 1, block)
                yield_paths[statement] = paths
    tree.body[0].body.append(ast.parse(
        f"self.yield_state: m.Bits[{clog2(len(yield_id_map))}] = 0"
    ).body[0])
    call_method.body = []
    for i, (yield_, paths) in enumerate(yield_paths.items()):
        test = ast.parse(
            f"self.yield_state == {yield_id_map[yield_]}"
        ).body[0].value
        if i == 0:
            curr_body = []
            call_method.body.append(ast.If(test, curr_body, []))
            prev_if = call_method.body[0]
        elif i == len(yield_paths) - 1:
            curr_body = prev_if.orelse
        else:
            curr_body = []
            prev_if.orelse.append(ast.If(test, curr_body, []))
            prev_if = prev_if.orelse[-1]
        for path in paths:
            body = curr_body
            end_yield = path[-1]
            for statement in path[:-1]:
                body.append(copy.deepcopy(statement))
                if isinstance(statement, ast.While):
                    body[-1] = ast.If(body[-1].test, body[-1].body, [])
                    body[-1].exitcase = statement.exitcase
                if isinstance(statement, (ast.If, ast.While)):
                    body[-1].test = body[-1].exitcase
                    body[-1].body = []
                    body = body[-1].body
            body.append(ast.parse(
                f"self.yield_state = {yield_id_map[end_yield]}"
            ).body[0])
            body.append(ast.Return(end_yield.value.value))
    call_method = RemoveIfTrues().visit(call_method)
    call_method = MergeInverseIf().visit(call_method)
    tree.decorator_list = [ast.parse(f"m.circuit.sequential").body[0].value]
    print(astor.to_source(tree))
    raise Exception()
