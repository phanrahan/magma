import functools
import ast
import inspect
import textwrap
from collections import OrderedDict
from magma.logging import root_logger
from magma.backend.util import make_relative
import astor
import os
import traceback
import magma.ast_utils as ast_utils
import types
from magma.debug import debug_info
from magma.ssa import convert_tree_to_ssa
from magma.config import get_debug_mode
from ..t import Type
from ..protocol_type import MagmaProtocol
import itertools
import typing
from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, SymbolTable
import magma as m


_logger = root_logger()


class CircuitDefinitionSyntaxError(Exception):
    pass


def m_dot(attr):
    return ast.Attribute(ast.Name("m", ast.Load()), attr, ast.Load())


def report_transformer_warning(message, filename, lineno, line):
    warning(f"\033[1m{make_relative(filename)}:{lineno}: {message}")
    warning(line)


class IfTransformer(ast.NodeTransformer):
    def __init__(self, filename, lines):
        super().__init__()
        self.filename = filename
        if lines:
            self.lines, self.starting_line = lines
        else:
            self.lines, self.starting_line = None, None

    def flatten(self, _list):
        """1-deep flatten"""
        flat_list = []
        for item in _list:
            if isinstance(item, list):
                flat_list.extend(item)
            else:
                flat_list.append(item)
        return flat_list

    def visit_If(self, node):
        # Flatten in case there's a nest If statement that returns a list
        node.body = self.flatten(map(self.visit, node.body))
        if not hasattr(node, "orelse"):
            raise NotImplementedError("If without else")
        node.orelse = self.flatten(map(self.visit, node.orelse))
        seen = OrderedDict()
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign):
                # TODO: Print info from original source file/line
                raise CircuitDefinitionSyntaxError(
                    f"Expected only assignment statements in if statement, got"
                    f" {type(stmt)}")
            if len(stmt.targets) > 1:
                raise NotImplementedError("Assigning more than one value")
            key = ast.dump(stmt.targets[0])
            if key in seen:
                if self.filename:
                    # TODO: Print the line number
                    report_transformer_warning(
                        "Assigning to value twice inside `if` block,"
                        " taking the last value (first value is ignored)",
                        self.filename, node.lineno + self.starting_line,
                        self.lines[node.lineno])
                else:
                    warning(
                        "Assigning to value twice inside `if` block,"
                        " taking the last value (first value is ignored)")
            seen[key] = stmt
        orelse_seen = set()
        for stmt in node.orelse:
            key = ast.dump(stmt.targets[0])
            if key in seen:
                if key in orelse_seen:
                    if self.filename:
                        report_transformer_warning(
                            "Assigning to value twice inside `else` block,"
                            " taking the last value (first value is ignored)",
                            self.filename, node.lineno + self.starting_line,
                            self.lines[node.lineno])
                    else:
                        warning(
                            "Assigning to value twice inside `else` block,"
                            " taking the last value (first value is ignored)")
                orelse_seen.add(key)
                seen[key].value = ast.Call(
                    ast.Name("phi", ast.Load()),
                    [ast.List([stmt.value, seen[key].value],
                              ast.Load()), node.test],
                    [])
            else:
                if self.filename:
                    report_transformer_warning(
                        "NOT IMPLEMENTED: Assigning to a variable once in"
                        " `else` block (not in then block)",
                        self.filename, node.lineno + self.starting_line,
                        self.lines[node.lineno])
                else:
                    warning(
                        "NOT IMPLEMENTED: Assigning to a variable once in"
                        " `else` block (not in then block)")
                raise NotImplementedError()
        return [node for node in seen.values()]

    def visit_IfExp(self, node):
        if not hasattr(node, "orelse"):
            raise NotImplementedError("If without else")
        node.body = self.visit(node.body)
        node.orelse = self.visit(node.orelse)
        return ast.Call(
            ast.Name("phi", ast.Load()),
            [ast.List([node.orelse, node.body],
                      ast.Load()), node.test],
            [])


class FunctionToCircuitDefTransformer(ast.NodeTransformer):
    def __init__(self, renamed_args):
        super().__init__()
        self.IO = {}
        self.renamed_args = renamed_args

    def visit(self, node):
        new_node = super().visit(node)
        if new_node is not node:
            return ast.copy_location(new_node, node)
        return node

    def qualify(self, node, direction):
        return ast.Call(m_dot(direction), [node], [])

    def visit_FunctionDef(self, node):
        names = self.renamed_args
        types = [arg.annotation for arg in node.args.args]
        keywords = []
        for name, type_ in zip(names, types):
            self.IO[name + "_0"] = name  # Add ssa rename
            keywords.append(ast.keyword(name, self.qualify(type_, "In")))
        if isinstance(node.returns, ast.Tuple):
            for i, elt in enumerate(node.returns.elts):
                keywords.append(ast.keyword(f"O{i}", self.qualify(elt, "Out")))
        else:
            keywords.append(ast.keyword("O", self.qualify(node.returns, "Out")))
        IO = ast.Call(m_dot("IO"), [], keywords)
        node.body = [self.visit(s) for s in node.body]
        if isinstance(node.returns, ast.Tuple):
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
                [ast.Name("O", ast.Load()),
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
            [], [ast.Assign([ast.Name("io", ast.Store())], IO)] + node.body,
            [])
        return class_def

    def visit_Name(self, node):
        if node.id in self.IO and isinstance(node.ctx, ast.Load):
            return ast.Attribute(ast.Name("io", ast.Load()), self.IO[node.id],
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


def _combinational(defn_env: dict, fn: types.FunctionType):
    tree = ast_utils.get_func_ast(fn)
    tree, renamed_args = convert_tree_to_ssa(tree, defn_env)
    tree = FunctionToCircuitDefTransformer(renamed_args).visit(tree)
    tree = ast.fix_missing_locations(tree)
    filename = None
    lines = None
    if get_debug_mode():
        filename = inspect.getsourcefile(fn)
        lines = inspect.getsourcelines(fn)
    tree = IfTransformer(filename, lines).visit(tree)
    tree = ast.fix_missing_locations(tree)
    tree.decorator_list = ast_utils.filter_decorator(
        combinational, tree.decorator_list, defn_env)
    if "m" not in defn_env:
        defn_env["m"] = m
    if "phi" not in defn_env:
        defn_env["phi"] = m.primitives.mux
    source = "\n"
    for i, line in enumerate(astor.to_source(tree).splitlines()):
        source += f"    {i}: {line}\n"

    _logger.debug(source)
    circuit_def = ast_utils.compile_function_to_file(tree, fn.__name__,
                                                     defn_env)
    if get_debug_mode() and getattr(circuit_def, "debug_info", False):
        circuit_def.debug_info = debug_info(circuit_def.debug_info.filename,
                                            circuit_def.debug_info.lineno,
                                            inspect.getmodule(fn))

    @functools.wraps(fn)
    def func(*args, **kwargs):
        if (len(args) + len(kwargs) and
            not any(isinstance(x, (Type, MagmaProtocol, m.AnonymousCircuitType)) for x in args +
                    tuple(kwargs.values()))):
                # If not called with at least one magma value, use the Python
                # implementation
                return fn(*args, **kwargs)
        return circuit_def()(*args, **kwargs)
    func.__name__ = fn.__name__
    func.__qualname__ = fn.__name__
    # Provide a mechanism for accessing the underlying circuit definition
    setattr(func, "circuit_definition", circuit_def)
    return func

def combinational(
        fn: typing.Callable = None,
        *,
        decorators: typing.Optional[typing.Sequence[typing.Callable]] = None,
        env: SymbolTable = None
        ):
    exec(_SKIP_FRAME_DEBUG_STMT)
    if decorators is not None:
        assert fn is None
        def wrapped(fn):
            exec(_SKIP_FRAME_DEBUG_STMT)
            nonlocal decorators
            decorators = list(itertools.chain(decorators, [wrapped]))
            wrapped_combinational = ast_utils.inspect_enclosing_env(
                    _combinational,
                    decorators=decorators,
                    st=env
            )
            return wrapped_combinational(fn)
        return wrapped

    else:
        wrapped_combinational = ast_utils.inspect_enclosing_env(
                _combinational,
                decorators=[combinational],
                st=env
        )
        return wrapped_combinational(fn)
