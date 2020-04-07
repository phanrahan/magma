import functools
import ast
import inspect

from ast_tools.passes import ssa, begin_rewrite, end_rewrite, if_to_phi

from ..circuit import Circuit, IO
from ..clock_io import ClockIO
from ..t import In, Out, Type

from .combinational2 import run_comb_passes


def sequential_setattr(self, key, value):
    # TODO: for now we assume this is a register, ideally we'd type check this,
    # but we need to have a notion of a register primitive (e.g. right now the
    # mantle reg wraps the coreir reg primitive, so technically the register is
    # an arbitrary user-defined circuit)

    # We can at least match the value is a circuit with outputs that match the
    # input of the attribute circuit
    if not isinstance(getattr(self, key), Circuit):
        raise TypeError("Excepted setattr key to be a Circuit")

    if not isinstance(value, (Circuit, int, Type)):
        raise TypeError("Excepted setattr value to be a Circuit, Type, or int",
                        f"not {type(value)}")

    # Simply use function call syntax for now (should automatically retrieve
    # the output of value)
    getattr(self, key)(value)


def sequential2(**clock_io_kwargs):
    """ clock_io_kwargs used for ClockIO params, e.g. async_reset """
    def seq_inner(cls):
        cls.__call__ = run_comb_passes(cls.__call__)

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

            # Monkey patch setattribute for register assign syntax, we could
            # also add this in a Sequential base class, but if we do that we
            # might as well use a metaclass rather than a decorator, but to
            # preserve the old interface we do this for now
            cls.__setattr__ = sequential_setattr

            for param in cls.__call__.__annotations__:
                if param == "return":
                    continue
                call_args.append(getattr(io, param))

            call_result = cls.__call__(*call_args)
            if isinstance(call_result, Circuit):
                if not len(call_result.interface.outputs()) == 1:
                    raise TypeError(
                        "Expected register return instance with one output")
                call_result = call_result.interface.outputs()[0]
            if isinstance(cls.__call__.__annotations__["return"], tuple):
                for i in range(len(cls.__call__.__annotations__["return"])):
                    getattr(io, f"O{i}").wire(call_result)
            else:
                io.O.wire(call_result)
        return SequentialCircuit
    return seq_inner
