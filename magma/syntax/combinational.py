import functools
import ast
import inspect
import textwrap
from collections import OrderedDict
from magma.logging import debug, warning, error
from magma.backend.util import make_relative
import astor
import os
import traceback
import magma.ast_utils as ast_utils
import types
from magma.debug import debug_info
from magma.config import get_debug_mode
import itertools
import typing
from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT
import ast_tools


class CircuitDefinitionSyntaxError(Exception):
    pass


def m_dot(attr):
    return ast.Attribute(ast.Name("m", ast.Load()), attr, ast.Load())


def report_transformer_warning(message, filename, lineno, line):
    warning(f"\033[1m{make_relative(filename)}:{lineno}: {message}")
    warning(line)


class IfExpTransformer(ast.NodeTransformer):
    def visit_IfExp(self, node):
        node.body = self.visit(node.body)
        node.orelse = self.visit(node.orelse)
        return ast.Call(
            ast.Name("phi", ast.Load()),
            [ast.List([node.orelse, node.body],
                      ast.Load()), node.test],
            [])


class FunctionToCircuitDefTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.IO = set()

    def visit(self, node):
        new_node = super().visit(node)
        if new_node is not node:
            return ast.copy_location(new_node, node)
        return node

    def qualify(self, node, direction):
        return ast.Call(m_dot(direction), [node], [])

    def visit_FunctionDef(self, node):
        types = [arg.annotation for arg in node.args.args]
        IO = []
        for arg in node.args.args:
            self.IO.add(arg.arg)
            IO.extend([ast.Str(arg.arg), self.qualify(arg.annotation, "In")])
        if isinstance(node.returns, ast.Tuple):
            for i, elt in enumerate(node.returns.elts):
                IO.extend([ast.Str(f"O{i}"), self.qualify(elt, "Out")])
        else:
            IO.extend([ast.Str("O"), self.qualify(node.returns, "Out")])
        IO = ast.List(IO, ast.Load())
        node.body = [self.visit(s) for s in node.body]
        assert isinstance(node.body[-1], ast.Return)
        return_value = node.body.pop().value
        if isinstance(node.returns, ast.Tuple):
            node.body.append(ast.Assign(
                [ast.Tuple([ast.Name(f"O{i}", ast.Store())
                 for i in range(len(node.returns.elts))], ast.Store())],
                ast.Name(return_value, ast.Load())
            ))
            for i, elt in enumerate(node.returns.elts):
                node.body.append(ast.Expr(ast.Call(
                    m_dot("wire"),
                    [ast.Name(f"O{i}", ast.Load()),
                     ast.Attribute(ast.Name("io", ast.Load()), f"O{i}",
                                   ast.Load())],
                    []
                )))
        else:
            node.body.append(ast.Expr(ast.Call(
                m_dot("wire"),
                [return_value,
                 ast.Attribute(ast.Name("io", ast.Load()), "O", ast.Load())],
                []
            )))
        # class {node.name}(m.Circuit):
        #     IO = {IO}
        #     @classmethod
        #     def definition(io):
        #         {body}
        class_def = ast.ClassDef(
            node.name,
            [ast.Attribute(ast.Name("m", ast.Load()), "Circuit", ast.Load())],
            [], [
                ast.Assign([ast.Name("IO", ast.Store())], IO),
                ast.FunctionDef(
                    "definition",
                    ast.arguments([ast.arg("io", None)],
                                  None, [], [],
                                  None, []),
                    node.body,
                    [ast.Name("classmethod", ast.Load())],
                    None
                )],
            [])
        return class_def

    def visit_Name(self, node):
        if node.id in self.IO and isinstance(node.ctx, ast.Load):
            return ast.Attribute(ast.Name("io", ast.Load()), node.id,
                                 ast.Load())
        return node

#     def visit_Return(self, node):
#         node.value = self.visit(node.value)
#         if isinstance(node.value, ast.Tuple):
#             return ast.Assign(
#                 [ast.Tuple([ast.Name(f"O{i}", ast.Store())
#                  for i in range(len(node.value.elts))], ast.Store())],
#                 node.value
#             )
#         return ast.Assign([ast.Name("O", ast.Store())], node.value)


def _combinational(tree, env, metadata):
    tree = FunctionToCircuitDefTransformer().visit(tree)
    tree = ast.fix_missing_locations(tree)
    tree = IfExpTransformer().visit(tree)
    tree = ast.fix_missing_locations(tree)
    tree.decorator_list = ast_utils.filter_decorator(
        combinational, tree.decorator_list, env)
    if "mux" not in env:
        from mantle import mux
        # TODO: Gen free name for mux
        env.globals["mux"] = mux

    def phi(args, cond):
        if all(isinstance(arg, tuple) for arg in args):
            return tuple(phi(list(zipped), cond) for zipped in zip(*args))
        return env["mux"](args, cond)

    # TODO: Gen free name for phi
    assert "phi" not in env, "phi already defined"
    env.globals["phi"] = phi
    source = "\n"
    for i, line in enumerate(astor.to_source(tree).splitlines()):
        source += f"    {i}: {line}\n"

    debug(source)
    return tree, env, metadata


class combinational(ast_tools.passes.Pass):
    def rewrite(self, tree: ast.AST, env: ast_tools.SymbolTable, metadata: dict):
        tree, env, metadata = ast_tools.passes.ssa().rewrite(tree, env, metadata)
        return _combinational(tree, env, metadata)
