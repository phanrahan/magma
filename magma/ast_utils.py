import inspect
import textwrap
import ast
import os
import types
import typing
import astor
import traceback


def get_ast(obj):
    indented_program_txt = inspect.getsource(obj)
    program_txt = textwrap.dedent(indented_program_txt)
    return ast.parse(program_txt)

def get_func_ast(obj : types.FunctionType):
    """ Implicitly strip ast.Module() surrounding the function """
    return get_ast(obj).body[0]


def compile_function_to_file(tree : ast.FunctionDef, defn_env={}):
    os.makedirs(".magma", exist_ok=True)
    file_name = os.path.join(".magma", tree.name + ".py")
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
    return defn_env[tree.name]


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
    def wrapped(*args, **kwargs):
        stack = inspect.stack()
        enclosing_env = {}
        for i in range(1, len(stack)):
            enclosing_env.update(stack[i].frame.f_locals)
            enclosing_env.update(stack[i].frame.f_globals)
        return fn(enclosing_env, *args, **kwargs)
    return wrapped


def filter_decorator(decorator : typing.Callable, decorator_list : typing.List[ast.AST], env : dict):
    def _filter(node):
        code = compile(ast.Expression(node), filename="<string>", mode="eval")
        return eval(code, env) != decorator
    return list(filter(_filter, decorator_list))
