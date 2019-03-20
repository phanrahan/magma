import inspect
import textwrap
import ast
import os
import types
import typing
import astor
import traceback
import functools


def get_ast(obj):
    indented_program_txt = inspect.getsource(obj)
    program_txt = textwrap.dedent(indented_program_txt)
    return ast.parse(program_txt)

def get_func_ast(obj : types.FunctionType):
    """ Implicitly strip ast.Module() surrounding the function """
    return get_ast(obj).body[0]


def compile_function_to_file(tree : typing.Union[ast.Module, ast.FunctionDef],
                             func_name : str = None, defn_env : dict = {}):
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
    # exec(compile(tree, filename=file_name, mode="exec"), defn_env)
    try:
        exec(compile(astor.to_source(tree), filename=file_name, mode="exec"), defn_env)
    except:
        import sys
        tb = traceback.format_exc()
        print(tb)
        raise Exception(f"Error occured when compiling and executing m.circuit.combinational function {func_name}, see above") from None
    return defn_env[func_name]


def inspect_enclosing_env(fn):
    """
    Traverses the current call stack to get the current locals and globals in
    the environment.

    Possible Improvements:
        * Return a scope object that preserves the distinction between globals
        and locals. This isn't currently required by the code using it, but
        could be useful for other use cases.
        * Maintain the stack hierarchy. Again, not currently used, but could be
        useful.
    """
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        stack = inspect.stack()
        enclosing_env = {}
        for i in range(0, len(stack)):
            for key, value in stack[i].frame.f_locals.items():
                if key not in enclosing_env:
                    enclosing_env[key] = value
        for i in range(0, len(stack)):
            for key, value in stack[i].frame.f_globals.items():
                if key not in enclosing_env:
                    enclosing_env[key] = value
        return fn(enclosing_env, *args, **kwargs)
    return wrapped


def filter_decorator(decorator : typing.Callable, decorator_list : typing.List[ast.AST], env : dict):
    def _filter(node):
        code = compile(ast.Expression(node), filename="<string>", mode="eval")
        return eval(code, env) != decorator
    return list(filter(_filter, decorator_list))
