import functools
import ast
import inspect
import textwrap
from collections import OrderedDict
from magma.logging import debug, warning, error
from .backend.util import make_relative
import astor
import os
import traceback
from .debug import debug_info


class CircuitDefinitionSyntaxError(Exception):
    pass


def m_dot(attr):
    return ast.Attribute(ast.Name("m", ast.Load()), attr, ast.Load())


def get_ast(obj):
    indented_program_txt = inspect.getsource(obj)
    program_txt = textwrap.dedent(indented_program_txt)
    return ast.parse(program_txt)


def report_transformer_warning(message, filename, lineno, line):
    warning(f"\033[1m{make_relative(filename)}:{lineno}: {message}")
    warning(line)


class IfTransformer(ast.NodeTransformer):
    def __init__(self, filename, lines):
        super().__init__()
        self.filename = filename
        self.lines, self.starting_line = lines

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
                # TODO: Print the line number
                report_transformer_warning("Assigning to value twice inside `if` block,"
                        " taking the last value (first value is ignored)", self.filename, node.lineno + self.starting_line, self.lines[node.lineno])
            seen[key] = stmt
        orelse_seen = set()
        for stmt in node.orelse:
            key = ast.dump(stmt.targets[0])
            if key in seen:
                if key in orelse_seen:
                    report_transformer_warning("Assigning to value twice inside `else` block,"
                            " taking the last value (first value is ignored)", self.filename, node.lineno + self.starting_line, self.lines[node.lineno])
                orelse_seen.add(key)
                seen[key].value = ast.Call(
                    ast.Name("mux", ast.Load()),
                    [ast.List([stmt.value, seen[key].value],
                              ast.Load()), node.test],
                    [])
            else:
                report_transformer_warning("NOT IMPLEMENTED: Assigning to a variable once in"
                        " `else` block (not in then block)", self.filename, node.lineno + self.starting_line, self.lines[node.lineno])
                raise NotImplementedError()
        return [node for node in seen.values()]

    def visit_IfExp(self, node):
        if not hasattr(node, "orelse"):
            raise NotImplementedError("If without else")
        node.body = self.visit(node.body)
        node.orelse = self.visit(node.orelse)
        return ast.Call(
            ast.Name("mux", ast.Load()),
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
        names = [arg.arg for arg in node.args.args]
        types = [arg.annotation for arg in node.args.args]
        IO = []
        for name, type_ in zip(names, types):
            self.IO.add(name)
            IO.extend([ast.Str(name),
                       self.qualify(type_, "In")])
        if isinstance(node.returns, ast.Tuple):
            for i, elt in enumerate(node.returns.elts):
                IO.extend([ast.Str(f"O{i}"), self.qualify(elt, "Out")])
        else:
            IO.extend([ast.Str("O"), self.qualify(node.returns, "Out")])
        IO = ast.List(IO, ast.Load())
        node.body = [self.visit(s) for s in node.body]
        if isinstance(node.returns, ast.Tuple):
            for i, elt in enumerate(node.returns.elts):
                node.body.append(ast.Expr(ast.Call(
                    m_dot("wire"),
                    [ast.Name(f"O{i}", ast.Load()),
                     ast.Attribute(ast.Name("io", ast.Load()), f"O{i}", ast.Load())],
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
                )

                ],
            [])
        return class_def

    def visit_Name(self, node):
        if node.id in self.IO:
            return ast.Attribute(ast.Name("io", ast.Load()), node.id,
                                 ast.Load())
        return node

    def visit_Return(self, node):
        node.value = self.visit(node.value)
        if isinstance(node.value, ast.Tuple):
            return ast.Assign(
                [ast.Tuple([ast.Name(f"O{i}", ast.Store())
                 for i in range(len(node.value.elts))], ast.Store())],
                node.value
            )
        return ast.Assign([ast.Name("O", ast.Store())], node.value)




def combinational(fn):
    stack = inspect.stack()
    defn_env = {}
    for i in range(1, len(stack)):
        defn_env.update(stack[i].frame.f_locals)
        defn_env.update(stack[i].frame.f_globals)
    tree = get_ast(fn)
    tree = FunctionToCircuitDefTransformer().visit(tree)
    tree = ast.fix_missing_locations(tree)
    tree = IfTransformer(inspect.getsourcefile(fn), inspect.getsourcelines(fn)).visit(tree)
    tree = ast.fix_missing_locations(tree)
    # TODO: Only remove @m.circuit.combinational, there could be others
    tree.body[0].decorator_list = []
    if "mux" not in defn_env:
        tree.body.insert(0, ast.parse("from mantle import mux").body[0])
    source = "\n"
    for i, line in enumerate(astor.to_source(tree).splitlines()):
        source += f"    {i}: {line}\n"

    debug(source)
    os.makedirs(".magma", exist_ok=True)
    file_name = os.path.join(".magma", fn.__name__ + ".py")
    with open(file_name, "w") as fp:
        fp.write(astor.to_source(tree))
    # exec(compile(tree, filename=file_name, mode="exec"), defn_env)
    try:
        exec(compile(astor.to_source(tree), filename=file_name, mode="exec"), defn_env)
    except:
        import sys
        tb = traceback.format_exc()
        print(tb)
        raise Exception(f"Error occured when compiling and executing m.circuit.combinational function {fn.__name__}, see above") from None
    circuit_def = defn_env[fn.__name__]
    circuit_def.debug_info = debug_info(circuit_def.debug_info.filename,
                                        circuit_def.debug_info.lineno,
                                        inspect.getmodule(fn))

    @functools.wraps(fn)
    def func(*args, **kwargs):
        return circuit_def()(*args, **kwargs)
    func.__name__ = fn.__name__
    func.__qualname__ = fn.__name__
    func.circuit_definition = circuit_def
    return func
