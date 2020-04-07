import inspect
import textwrap
import ast

from ..t import In, Out

def get_ast(obj):
    indented_program_txt = inspect.getsource(obj)
    program_txt = textwrap.dedent(indented_program_txt)
    return ast.parse(program_txt)


def build_io_args(annotations):
    io_args = {}

    for param, annotation in annotations.items():
        if param == "return":
            annotation = Out(annotation)
            if isinstance(annotation, tuple):
                for i, elem in enumerate(annotation):
                    io_args[f"O{i}"] = elem
            else:
                io_args["O"] = annotation
            continue
        annotation = In(annotation)
        io_args[param] = annotation
    return io_args
