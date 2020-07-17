import ast
from typing import MutableMapping, Optional

import astor

import ast_tools
from ast_tools.stack import SymbolTable
from ast_tools.passes import (apply_ast_passes, Pass, PASS_ARGS_T, ssa,
                              if_to_phi, bool_to_bit)
from ast_tools.common import gen_free_prefix
from ast_tools.immutable_ast import immutable, mutable

from magma.syntax.combinational2 import combinational2
from magma.bit import Bit
from magma.wire import wire


class _ToCombinationalRewriter(ast.NodeTransformer):
    def __init__(self, free_prefix, target_map):
        self.prefix = free_prefix
        self.target_map = target_map
        self.name_count = 0

    def _gen_new_name(self):
        new_name = f"{self.prefix}{self.name_count}"
        self.name_count += 1
        return new_name

    def visit_AugAssign(self, node):
        if not isinstance(node.op, ast.MatMult):
            return node
        key = immutable(node.target)
        if key not in self.target_map:
            retval_name = self._gen_new_name()
            self.target_map[key] = retval_name
        target = ast.Name(self.target_map[key], ast.Store())
        return ast.Assign([target], node.value)


class _RewriteToCombinational(Pass):
    """
    Replace wiring targets with a temporary value (so it is handled properly by
    SSA), store the mapping from temporary values so they can be wired up
    later, "inputs" will just read from the enclosing scope
    """
    def __init__(self, target_map):
        super().__init__()
        self.target_map = target_map

    def rewrite(
        self, tree: ast.AST, env: SymbolTable, metadata: MutableMapping
    ) -> PASS_ARGS_T:
        # prefix used for temporaries
        prefix = gen_free_prefix(tree, env)

        tree = _ToCombinationalRewriter(prefix, self.target_map).visit(tree)

        # Return augassign targets for wiring
        elts = [ast.Name(value, ast.Load())
                for value in self.target_map.values()]
        retval = ast.Tuple(elts, ast.Load()) if len(elts) > 1 else elts[0]
        tree.body.append(ast.Return(retval))

        return tree, env, metadata


class inline_combinational(apply_ast_passes):
    def __init__(self, pre_passes=[], post_passes=[],
                 debug: bool = False,
                 env: Optional[SymbolTable] = None,
                 path: Optional[str] = None,
                 file_name: Optional[str] = None
                 ):
        self.target_map = {}
        passes = (pre_passes + [_RewriteToCombinational(self.target_map),
                                ast_tools.passes.debug(dump_src=True),
                                ssa(strict=False), bool_to_bit(),
                                if_to_phi(lambda s, t, f: s.ite(t, f)),
                                ast_tools.passes.debug(dump_src=True),
                                ] +
                  post_passes)
        super().__init__(passes=passes, env=env, debug=debug, path=path,
                         file_name=file_name)

    def exec(self, etree, stree, env):
        fn = super().exec(etree, stree, env)
        result = fn()
        if not isinstance(result, tuple):
            result = (result,)
        for key, value in zip(self.target_map.keys(), result):
            # Eval original target in env to do wiring, not sure if there's a
            # way we can avoid having to do eval here (other option is to
            # codegen the original augassign in a new tree, but that's
            # effectively the same as evaling)
            wire(eval(astor.to_source(mutable(key)).rstrip(), {}, env), value)
