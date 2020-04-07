import ast
import astor

import ast_tools
from ast_tools.passes import ssa, begin_rewrite, end_rewrite, if_to_phi

from ..t import In, Out
from ..circuit import Circuit, IO


class RemoveCombDecorator(ast_tools.passes.Pass):
    def rewrite(self, tree: ast.AST, env: ast_tools.SymbolTable,
                metadata: dict):
        for item in tree.decorator_list:
            # TODO: Need robust way to check it's the decorator, but this
            # should work for now if the user imports as combinational2
            if eval(astor.to_source(item)) == combinational2:
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

    io_args = {}

    if "self" in fn.__annotations__:
        raise Exception("Assumed self did not have annotation")

    for param, annotation in fn.__annotations__.items():
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

    class CombinationalCircuit(Circuit):
        name = fn.__name__
        io = IO(**io_args)

        call_args = []
        for param in fn.__annotations__:
            if param == "return":
                continue
            call_args.append(getattr(io, param))

        call_result = fn(*call_args)
        if isinstance(call_result, Circuit):
            if not len(call_result.interface.outputs()) == 1:
                raise TypeError(
                    "Expected register return instance with one output")
            call_result = call_result.interface.outputs()[0]
        if isinstance(fn.__annotations__["return"], tuple):
            for i in range(len(fn.__annotations__["return"])):
                getattr(io, f"O{i}").wire(call_result)
        else:
            io.O.wire(call_result)
    return CombinationalCircuit
