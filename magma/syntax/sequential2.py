import functools
import ast
import inspect

from ast_tools.passes import Pass, ssa, begin_rewrite, end_rewrite
from ast_tools import SymbolTable
import astor

from ..ast_utils import get_ast
from ..generator import Generator2, _Generator2Meta


class SequentialCircuitMeta(_Generator2Meta):
    def __new__(metacls, name, bases, dct):
        if "__call__" in dct:
            for pass_ in [begin_rewrite(), ssa(strict=False), end_rewrite()]:
                dct["__call__"] = pass_(dct["__call__"])
        return super().__new__(metacls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        circuit = super().__call__(*args, **kwargs)
        call_params = inspect.signature(cls.__call__)
        call_args = []
        for i, param in enumerate(call_params.parameters):
            if i == 0:
                assert param == "self"
                call_args.append(circuit)
            else:
                # TODO: Assumes param is valid io attribute, can raise error here
                # if not
                call_args.append(getattr(circuit, param))
        with circuit.open():
            call_result = cls.__call__(*call_args)
            getattr(circuit, circuit._call_output_name_).wire(call_result)
        return circuit


class SequentialCircuit(Generator2, metaclass=SequentialCircuitMeta):
    _call_output_name_ = "O"
    def __init__(self):
        # Ignore undriven errors because some may be wired up by __call__
        self._ignore_undriven_ = True
