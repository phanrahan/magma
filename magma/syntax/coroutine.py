import ast
import copy

import astor
from staticfg import CFGBuilder
from staticfg.builder import invert
from ast_tools.stack import inspect_enclosing_env

from ..ast_utils import get_ast, compile_function_to_file
from ..bitutils import clog2


class RemoveIfTrues(ast.NodeTransformer):
    """
    Remove `if True:` nodes by replacing them with their body
    """
    def visit_If(self, node):
        if isinstance(node.test, ast.NameConstant) and node.test.value is True:
            return node.body
        return self.generic_visit(node)


class MergeInverseIf(ast.NodeTransformer):
    """
    Merge cases where
    ```
    if cond:
        ...
    if invert(cond):
        ...
    ```
    into
    ```
    if cond:
        ...
    else:
        ...
    ```

    `invert` comes from the `staticfg` library, which is used in marking
    control flow graph paths, so this just tries to reconstruct the if/else
    structure found in the original code based on the control flow graph
    construction
    """
    def visit(self, node):
        if hasattr(node, 'body'):
            node.body = self.visit_body(node.body)
        if hasattr(node, 'orelse'):
            node.orelse = self.visit_body(node.orelse)
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
                    and ast.dump(invert(node.test))
                    == ast.dump(body[i + 1].test)):
                node.orelse = body[i + 1].body
                skip_next = True
            else:
                skip_next = False
        return new_body


def is_yield(statement):
    """
    Is this a statement of the form `yield <expr>`
    """
    return (isinstance(statement, ast.Expr)
            and isinstance(statement.value, ast.Yield))


def collect_paths_to_yield(start_idx, block):
    """
    Given a start idx in a block, collect the paths to the next yield.

    Use a start offset because some yields occur inside a basic block, so the
    start of a path may not be the start of the block.

    Copies branch nodes and stores their `exitcase` into the test for use later
    (so we know the required condition of this path)
    """
    path = []
    for statement in block.statements[start_idx:]:
        path.append(statement)
        if is_yield(statement):
            return [path]
    paths = []
    for exit in block.exits:
        _path = path
        if exit.exitcase is not None:
            assert (len(_path) == 1
                    and isinstance(_path[0], (ast.If, ast.While))), \
                "Expect branch"
            _path = _path.copy()
            _path[0] = copy.copy(_path[0])
            _path[0].test = exit.exitcase
        paths.extend(_path + p for p in collect_paths_to_yield(0, exit.target))
    return paths


def _coroutine(defn_env, fn):
    tree = get_ast(fn).body[0]

    # validate assumptions on program format
    assert (isinstance(tree.body[0], ast.FunctionDef)
            and tree.body[0].name == "__init__")
    assert (isinstance(tree.body[1], ast.FunctionDef)
            and tree.body[1].name == "__call__")
    call_method = tree.body[1]

    # build cfg
    cfg = CFGBuilder().build(call_method.name, call_method)
    # debug cfg visualizer
    # cfg.build_visual(tree.name, 'pdf')

    # map from yield ast node (by id) to paths to other yields
    yield_paths = {}
    # map from yield ast node (by id) to numeric id (for state encoding)
    yield_id_map = {}

    # populate maps
    for block in cfg:
        for i, statement in enumerate(block.statements):
            if is_yield(statement):
                # Encode by index
                yield_id_map[statement] = len(yield_id_map)

                paths = collect_paths_to_yield(i + 1, block)
                yield_paths[statement] = paths

    # add yield state register declaration
    yield_state_width = clog2(len(yield_id_map))
    tree.body[0].body.append(ast.parse(
        f"self.yield_state: m.Bits[{yield_state_width}] = 0"
    ).body[0])

    # create new call body
    call_method.body = []
    for i, (yield_, paths) in enumerate(yield_paths.items()):
        # condition based on yield state encoding for current start yield
        test = ast.parse(
            f"self.yield_state == {yield_id_map[yield_]}"
        ).body[0].value

        if i == 0:
            # for first if, populate new call method body
            curr_body = []
            call_method.body.append(ast.If(test, curr_body, []))
            prev_if = call_method.body[0]
        elif i == len(yield_paths) - 1:
            # Use the previous if's orelse block for final state
            curr_body = prev_if.orelse
        else:
            # use the previous if's orelse block (so we generate an if/elif
            # chain)
            curr_body = []
            prev_if.orelse.append(ast.If(test, curr_body, []))
            prev_if = prev_if.orelse[-1]

        # Emite code for each path
        for path in paths:
            body = curr_body
            end_yield = path[-1]
            for statement in path[:-1]:
                body.append(copy.deepcopy(statement))
                # If we encounter a branch, subsequent statements go inside the
                # branch
                if isinstance(statement, ast.While):
                    body[-1] = ast.If(body[-1].test, body[-1].body, [])
                if isinstance(statement, (ast.If, ast.While)):
                    body[-1].body = []
                    body = body[-1].body

            # Finish with updating the yield state register with the end yield
            # of the path
            body.append(ast.parse(
                f"self.yield_state = m.bits({yield_id_map[end_yield]}, "
                f"{yield_state_width})"
            ).body[0])

            # Return the value of the original end yield
            body.append(ast.Return(end_yield.value.value))

    # Remove if trues for readability
    call_method = RemoveIfTrues().visit(call_method)
    # Merge `if cond:` with `if not cond` for readability
    call_method = MergeInverseIf().visit(call_method)

    # Sequential stage
    tree.decorator_list = [ast.parse(
        f"m.circuit.sequential(async_reset=True)"
    ).body[0].value]

    # print(astor.to_source(tree))
    circuit = compile_function_to_file(tree, tree.name, defn_env)
    return circuit


coroutine = inspect_enclosing_env(_coroutine)
