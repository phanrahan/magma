import functools
import ast
import inspect

from ast_tools.passes import Pass, ssa, begin_rewrite, end_rewrite
from ast_tools import SymbolTable
import astor

from ..ast_utils import get_ast
from ..generator import Generator2, _Generator2Meta
from ..circuit import Circuit, IO
from ..clock_io import ClockIO
from ..t import In, Out

def sequential2(**clock_io_kwargs):
    """ clock_io_kwargs used for ClockIO params, e.g. async_reset """
    def seq_inner(cls):
        for pass_ in [begin_rewrite(), ssa(strict=False), end_rewrite()]:
            cls.__call__ = pass_(cls.__call__)

        io_args = {}

        if "self" in cls.__call__.__annotations__:
            raise Exception("Assumed self did not have annotation")

        for param, annotation in cls.__call__.__annotations__.items():
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

        class SequentialCircuit(Circuit):
            name = cls.__name__
            io = IO(**io_args) + ClockIO(**clock_io_kwargs)
            call_args = [cls()]
            for param in cls.__call__.__annotations__:
                if param == "return":
                    continue
                call_args.append(getattr(io, param))

            call_result = cls.__call__(*call_args)
            if isinstance(cls.__call__.__annotations__["return"], tuple):
                for i in range(len(cls.__call__.__annotations__["return"])):
                    getattr(io, f"O{i}").wire(call_result)
            else:
                io.O @= call_result
        return SequentialCircuit
    return seq_inner
