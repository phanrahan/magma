import ast
from typing import MutableMapping, Optional

import astor

import ast_tools
from ast_tools.stack import SymbolTable, get_symbol_table
from ast_tools.passes import (apply_ast_passes, Pass, PASS_ARGS_T, ssa,
                              if_to_phi, bool_to_bit)
from ast_tools.common import gen_free_prefix, gen_free_name
from ast_tools.immutable_ast import immutable, mutable

import magma as magma_module
from magma.syntax.combinational2 import combinational2
from magma.bit import Bit
from magma.wire import wire


class _ToCombinationalRewriter(ast.NodeTransformer):
    def __init__(self, free_prefix, wire_map, env):
        self.prefix = free_prefix
        self.wire_map = wire_map
        self.env = env
        self.name_count = 0

    def _gen_new_name(self):
        new_name = f"{self.prefix}_{self.name_count}_"
        self.name_count += 1
        return new_name

    def _gen_assign(self, target, value):
        key = immutable(target)
        if key not in self.wire_map:
            self.wire_map[key] = self._gen_new_name()
        target = ast.Name(self.wire_map[key], ast.Store())
        return ast.Assign([target], value)

    def visit_AugAssign(self, node):
        if not isinstance(node.op, ast.MatMult):
            return node
        return self._gen_assign(node.target, node.value)

    def visit_Call(self, node):
        if (
            isinstance(node.func, ast.Attribute) and node.func.attr == "wire"
            and eval(node.func.value.id, {}, self.env) is magma_module
        ):
            # m.wire(value, target)
            return self._gen_assign(node.args[1], node.args[0])
        return node


class _RewriteToCombinational(Pass):
    """
    Replace wiring targets with a temporary value (so it is handled properly by
    SSA), store the mapping from temporary values so they can be wired up
    later, "inputs" will just read from the enclosing scope
    """
    def __init__(self, wire_map):
        super().__init__()
        self.wire_map = wire_map

    def rewrite(
        self, tree: ast.AST, env: SymbolTable, metadata: MutableMapping
    ) -> PASS_ARGS_T:
        # prefix used for temporaries
        prefix = gen_free_prefix(tree, env)

        tree = _ToCombinationalRewriter(prefix, self.wire_map, env).visit(tree)

        # Return targets for wiring and assignments
        return_values = list(self.wire_map.values())
        elts = [ast.Name(value, ast.Load()) for value in return_values]
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
        if env is None:
            env = get_symbol_table([self.__init__])
        self.wire_map = {}
        passes = (pre_passes + [_RewriteToCombinational(self.wire_map),
                                ssa(strict=False), bool_to_bit(),
                                if_to_phi(Bit.ite)] +
                  post_passes)
        super().__init__(passes=passes, env=env, debug=debug, path=path,
                         file_name=file_name)

    def exec(self, etree, stree, env):
        fn = super().exec(etree, stree, env)
        result = fn()
        if not isinstance(result, tuple):
            result = (result,)
        for key, value in zip(self.wire_map.keys(), result):
            # Eval original target in env to do wiring, not sure if there's a
            # way we can avoid having to do eval here (other option is to
            # codegen the original augassign in a new tree, but that's
            # effectively the same as evaling)
            wire(value, eval(astor.to_source(mutable(key)).rstrip(), {}, env))
