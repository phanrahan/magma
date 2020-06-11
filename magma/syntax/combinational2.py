import ast
import astor
import functools

import ast_tools
from ast_tools.passes import ssa, begin_rewrite, end_rewrite, if_to_phi

from ..circuit import Circuit, IO
from ..protocol_type import MagmaProtocol
from ..t import Type

from .util import build_io_args, build_call_args, wire_call_result


class RemoveCombDecorator(ast_tools.passes.Pass):
    def rewrite(self, tree: ast.AST, env: ast_tools.SymbolTable,
                metadata: dict):
        for item in tree.decorator_list:
            # TODO: Need robust way to check it's the decorator, but this
            # should work for now if the user imports as combinational2
            if eval(astor.to_source(item), {}, env) == combinational2:
                tree.decorator_list.remove(item)
        return tree, env, metadata


def run_comb_passes(fn, remove_decorator=True):
    passes = [begin_rewrite(), ssa(strict=False),
              if_to_phi(lambda s, t, f: s.ite(t, f)), end_rewrite()]
    if remove_decorator:
        passes.insert(1, RemoveCombDecorator())
    for pass_ in passes:
        fn = pass_(fn)
    return fn


def combinational2(fn):
    fn = run_comb_passes(fn)

    io_args = build_io_args(fn.__annotations__)

    class CombinationalCircuit(Circuit):
        name = fn.__name__
        io = IO(**io_args)

        call_args = build_call_args(io, fn.__annotations__)

        call_result = fn(*call_args)

        wire_call_result(io, call_result, fn.__annotations__)

    @functools.wraps(fn)
    def func(*args, **kwargs):
        if (len(args) + len(kwargs) and
            not any(isinstance(x, (Type, MagmaProtocol)) for x in args +
                    tuple(kwargs.values()))):
            # If not called with at least one magma value, use the Python
            # implementation
            return fn(*args, **kwargs)
        return CombinationalCircuit()(*args, **kwargs)
    func.__name__ = fn.__name__
    func.__qualname__ = fn.__name__
    # Provide a mechanism for accessing the underlying circuit definition
    setattr(func, "circuit_definition", CombinationalCircuit)
    return func
