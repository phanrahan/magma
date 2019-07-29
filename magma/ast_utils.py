import inspect
import textwrap
import ast
import os
import types
import typing
import astor
import traceback
import functools

from ast_tools.stack import inspect_enclosing_env

def get_ast(obj):
    indented_program_txt = inspect.getsource(obj)
    program_txt = textwrap.dedent(indented_program_txt)
    return ast.parse(program_txt)

def get_func_ast(obj : types.FunctionType):
    """ Implicitly strip ast.Module() surrounding the function """
    return get_ast(obj).body[0]


def compile_function_to_file(tree : typing.Union[ast.Module, ast.FunctionDef],
                             func_name : str = None, defn_env : dict = None):
    if defn_env is None:
        defn_env = {}

    if isinstance(tree, ast.FunctionDef):
        if func_name is None:
            func_name = tree.name
        else:
            if func_name != tree.name:
                raise Exception("Passed in func_name that does not match the "
                                "function being compiled. Got"
                                f" func_name={func_name} expected"
                                f" tree.name={tree.name}")
    elif isinstance(tree, ast.Module):
        if func_name is None:
            raise Exception("func_name required when passing in an ast.Module")
    os.makedirs(".magma", exist_ok=True)
    file_name = os.path.join(".magma", func_name + ".py")
    with open(file_name, "w") as fp:
        fp.write(astor.to_source(tree))

    try:
        code = compile(astor.to_source(tree), filename=file_name, mode="exec")
    except:
        import sys
        tb = traceback.format_exc()
        print(tb)
        raise Exception(f"Error occured when compiling m.circuit.combinational function {func_name}, see above")

    try:
        exec(code, defn_env)
    except:
        import sys
        tb = traceback.format_exc()
        print(tb)
        raise Exception(f"Error occured when executing m.circuit.combinational function {func_name}, see above")

    return defn_env[func_name]

class NameCollector(ast.NodeVisitor):
    def __init__(self):
        self.names = set()

    def visit_Name(self, node: ast.Name):
        self.names.add(node.id)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.names.add(node.name)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.names.add(node.name)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.names.add(node.name)

def gen_free_name(tree: ast.AST, defn_env: dict, prefix: str = '__auto_name_'):
    visitor = NameCollector()
    visitor.visit(tree)
    used_names = visitor.names | defn_env.keys()
    f_str = prefix+'{}'
    c = 0
    name = f_str.format(c)
    while name in used_names:
        c += 1
        name = f_str.format(c)

    return name

def filter_decorator(decorator : typing.Callable, decorator_list : typing.List[ast.AST], env : dict):
    def _filter(node):
        if isinstance(node, ast.Call):
            expr = ast.Expression(node.func)
        elif isinstance(node, ast.Name):
            expr = ast.Expression(node)
        else:
            return True
        code = compile(expr, filename="<string>", mode="eval")
        e = eval(code, env)
        return e != decorator
    return list(filter(_filter, decorator_list))
