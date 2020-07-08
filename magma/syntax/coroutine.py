from typing import Optional, MutableMapping
import ast
import copy

import astor
from staticfg import CFGBuilder
from staticfg.builder import invert
from ast_tools.stack import SymbolTable
from ast_tools.passes import PASS_ARGS_T, Pass, apply_ast_passes

from .transforms import inline_yield_from_functions
from ..ast_utils import get_ast
from ..bitutils import clog2
from ..clock import AbstractReset
from .sequential2 import sequential2


def is_if_not_true(node):
    return (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.Not)
        and isinstance(node.operand, ast.NameConstant)
        and node.operand.value is True
    )


class RemoveIfTrues(ast.NodeTransformer):
    """
    Remove `if True:` nodes by replacing them with their body
    Remove `if not True:` nodes by replacing them with `pass`
    """
    def visit_If(self, node):
        node = self.generic_visit(node)
        if isinstance(node.test, ast.NameConstant) and node.test.value is True:
            return node.body
        elif is_if_not_true(node.test):
            return ast.Pass()
        return node


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
        if is_if_not_true(exit.exitcase):
            # skip 'if not True:'
            continue
        elif exit.exitcase is not None:
            assert (len(_path) == 1
                    and isinstance(_path[0], (ast.If, ast.While))), \
                "Expect branch"
            _path = _path.copy()
            _path[0] = copy.copy(_path[0])
            _path[0].test = exit.exitcase
        paths.extend(_path + p for p in collect_paths_to_yield(0, exit.target))
    return paths


def build_method_name_map(tree):
    name_map = {}
    for stmt in tree.body:
        if isinstance(stmt, ast.FunctionDef):
            name_map[stmt.name] = stmt
    return name_map


class _ReplaceTree(Pass):
    def __init__(self, tree):
        self.tree = tree

    def rewrite(self,
                tree: ast.AST,
                env: SymbolTable,
                metadata: MutableMapping) -> PASS_ARGS_T:
        return self.tree, env, metadata


def coroutine(pre_passes=[], post_passes=[],
              debug: bool = False,
              env: Optional[SymbolTable] = None,
              path: Optional[str] = None,
              file_name: Optional[str] = None,
              annotations: Optional[dict] = None,
              manual_encoding: bool = False,
              reset_type: AbstractReset = None,
              has_enable: bool = False,
              reset_priority: bool = True):

    def inner(cls):
        tree = get_ast(cls).body[0]
        method_name_map = build_method_name_map(tree)

        call_method = method_name_map["__call__"]
        call_method = inline_yield_from_functions(call_method, method_name_map)

        # build cfg
        cfg = CFGBuilder().build(call_method.name, call_method)
        # debug cfg visualizer
        # cfg.build_visual(tree.name, 'pdf')

        # map from yield ast node (by id) to paths to other yields
        yield_paths = {}
        # map from yield ast node (by id) to numeric id (for state encoding)
        yield_encoding_map = {}

        # populate maps
        for block in cfg:
            for i, statement in enumerate(block.statements):
                if is_yield(statement):
                    paths = collect_paths_to_yield(i + 1, block)
                    yield_paths[statement] = paths
                    if not manual_encoding:
                        # Encode by index
                        encoding = len(yield_encoding_map)
                    else:
                        # TODO: Assumes previous stmt sets encoding
                        encoding = astor.to_source(
                            block.statements[i - 1].value
                        ).rstrip()
                    yield_encoding_map[statement] = encoding

        return_type = cls.__call__.__annotations__["return"]
        if isinstance(return_type, tuple):
            return_target = [f"__magma_coroutine_return_value_{i}"
                             for i in range(len(return_type))]
        else:
            return_target = "__magma_coroutine_return_value"

        # add yield state register declaration
        yield_state_width = clog2(len(yield_encoding_map))
        if not manual_encoding:
            method_name_map["__init__"].body.append(ast.parse(
                f"self.yield_state = m.Register("
                f"T=m.Bits[{yield_state_width}], init=0)()"
            ).body[0])

            # replace __init__
            cls.__init__ = apply_ast_passes(
                passes=[_ReplaceTree(method_name_map["__init__"])],
                debug=debug,
                env=env,
                path=path,
                file_name=file_name
            )(cls.__init__)

        # create new call body
        call_method.body = []
        for i, (yield_, paths) in enumerate(yield_paths.items()):
            # condition based on yield state encoding for current start yield
            test = ast.parse(
                f"self.yield_state == {yield_encoding_map[yield_]}"
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
            for path_ in paths:
                body = curr_body
                end_yield = None
                for statement in path_:
                    if is_yield(statement):
                        end_yield = statement
                        break
                    body.append(copy.deepcopy(statement))
                    # If we encounter a branch, subsequent statements go inside
                    # the branch
                    if isinstance(statement, ast.While):
                        body[-1] = ast.If(body[-1].test, [], [])
                    if isinstance(statement, ast.If):
                        body[-1].body = []
                        body[-1].orelse = []
                    if isinstance(statement, (ast.If, ast.While)):
                        body = body[-1].body
                assert end_yield is not None, "Found path not ending in yield"

                if not manual_encoding:
                    # Finish with updating the yield state register with the end
                    # yield of the path
                    body.append(ast.parse(
                        f"self.yield_state = m.bits("
                        f"{yield_encoding_map[end_yield]}, {yield_state_width})"
                    ).body[0])

                # Return the value of the original end yield
                if isinstance(return_target, list):
                    body.append(
                        ast.Assign([
                            ast.Tuple([ast.Name(x, ast.Store()) for x in
                                       return_target], ast.Load())
                        ], end_yield.value.value))
                else:
                    body.append(ast.Assign(
                        [ast.Name(return_target, ast.Store())],
                        end_yield.value.value
                    ))

        # Remove if trues for readability
        call_method = RemoveIfTrues().visit(call_method)
        # Merge `if cond:` with `if not cond` for readability
        call_method = MergeInverseIf().visit(call_method)
        if isinstance(return_target, list):
            call_method.body.append(
                ast.Return(ast.Tuple([ast.Name(x, ast.Load())
                                      for x in return_target], ast.Load())))
        else:
            call_method.body.append(
                ast.Return(ast.Name(return_target, ast.Load())))

        # Replace __call__
        cls.__call__ = apply_ast_passes(
            passes=[_ReplaceTree(call_method)],
            debug=debug,
            env=env,
            path=path,
            file_name=file_name,
        )(cls.__init__)

        return sequential2(
            pre_passes=pre_passes,
            post_passes=post_passes,
            debug=debug,
            env=env,
            path=path,
            file_name=file_name,
            annotations=annotations,
            reset_type=reset_type,
            has_enable=has_enable,
            reset_priority=reset_priority,
        )(cls)

    return inner
