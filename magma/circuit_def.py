import functools
import ast
import inspect
import textwrap


def get_ast(obj):
    indented_program_txt = inspect.getsource(obj)
    program_txt = textwrap.dedent(indented_program_txt)
    return ast.parse(program_txt)


def circuit_def(fn):
    tree = get_ast(fn)
    print(ast.dump(tree))

    @classmethod
    @functools.wraps(fn)
    def wrapped(io):
        return fn(io)

    raise NotImplementedError()
    return wrapped
