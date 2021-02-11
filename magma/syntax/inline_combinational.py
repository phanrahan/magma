import ast
import libcst as cst
from typing import MutableMapping, Optional

import astor

import ast_tools
from ast_tools.stack import SymbolTable, get_symbol_table
from ast_tools.passes import (apply_passes, Pass, PASS_ARGS_T, ssa,
                              if_to_phi, bool_to_bit)
from ast_tools.common import gen_free_prefix, gen_free_name, to_module
from ast_tools.immutable_ast import immutable, mutable

import magma as magma_module
from magma.syntax.combinational2 import combinational2
from magma.bit import Bit
from magma.wire import wire


class _ToCombinationalRewriter(cst.CSTTransformer):
    def __init__(self, free_prefix, wire_map, env):
        super().__init__()
        self.prefix = free_prefix
        self.wire_map = wire_map
        self.env = env
        self.name_count = 0

    def _gen_new_name(self):
        new_name = f"{self.prefix}_{self.name_count}_"
        self.name_count += 1
        return new_name

    def _gen_assign(self, target, value):
        key = to_module(target).code
        if key not in self.wire_map:
            self.wire_map[key] = self._gen_new_name()
        target = cst.Name(self.wire_map[key])
        return cst.Assign((cst.AssignTarget(target), ), value)

    def leave_AugAssign(self, original_node, updated_node):
        if not isinstance(updated_node.operator, cst.MatrixMultiplyAssign):
            return updated_node
        return self._gen_assign(updated_node.target, updated_node.value)

    def leave_Expr(self, original_node, updated_node):
        final_node = super().leave_Expr(original_node, updated_node)
        if isinstance(final_node.value, cst.Assign):
            return final_node.value
        return final_node

    def leave_Call(self, original_node, updated_node):
        if (
            isinstance(updated_node.func, cst.Attribute) and
            updated_node.func.attr.value == "wire" and
            eval(updated_node.func.value.value, {}, self.env) is magma_module
        ):
            # m.wire(value, target)
            return self._gen_assign(updated_node.args[1].value,
                                    updated_node.args[0].value)
        return updated_node


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
        self, tree: cst.CSTNode, env: SymbolTable, metadata: MutableMapping
    ) -> PASS_ARGS_T:
        # prefix used for temporaries
        prefix = gen_free_prefix(tree, env)

        tree = tree.visit(_ToCombinationalRewriter(
            prefix, self.wire_map, env
        ))
        # Return targets for wiring and assignments
        return_values = list(self.wire_map.values())
        elts = [cst.Name(value) for value in return_values]
        retval = (cst.Tuple([cst.Element(e) for e in elts])
                  if len(elts) > 1 else elts[0])
        tree = tree.with_changes(
            body=tree.body.with_changes(
                body=tree.body.body + (
                    cst.SimpleStatementLine([cst.Return(retval)]),
                )
            )
        )

        return tree, env, metadata


class inline_combinational(apply_passes):
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

    def exec(self, etree, stree, env, metadata):
        fn = super().exec(etree, stree, env, metadata)
        result = fn()
        if not isinstance(result, tuple):
            result = (result,)
        for key, value in zip(self.wire_map.keys(), result):
            # Eval original target in env to do wiring, not sure if there's a
            # way we can avoid having to do eval here (other option is to
            # codegen the original augassign in a new tree, but that's
            # effectively the same as evaling)
            wire(value, eval(key, {}, env))
