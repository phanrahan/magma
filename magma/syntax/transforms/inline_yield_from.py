import copy
import ast
from .replace_symbols import replace_symbols
import astor
from ...ast_utils import get_ast


class YieldFromFunctionInliner(ast.NodeTransformer):
    def __init__(self, method_name_map):
        self.method_name_map = method_name_map

    def visit(self, node):
        """
        For nodes with a `body` attribute, we explicitly traverse them and
        flatten any lists that are returned. This allows visitors to return
        more than one node.
        """
        if hasattr(node, 'body') and not isinstance(node, ast.IfExp):
            new_body = []
            for statement in node.body:
                result = self.visit(statement)
                if isinstance(result, list):
                    new_body.extend(result)
                else:
                    new_body.append(result)
            node.body = new_body
            if isinstance(node, ast.If):
                new_orelse = []
                for statement in node.orelse:
                    result = self.visit(statement)
                    if isinstance(result, list):
                        new_orelse.extend(result)
                    else:
                        new_orelse.append(result)
                node.orelse = new_orelse
            return node
        return super().visit(node)

    def visit_Assign(self, node):
        """
        If node.value is a YieldFrom that is inlined, it will return a list, so
        here we pass the list on so it can be flattened into the body of the
        parent node
        """
        node.value = self.visit(node.value)
        if isinstance(node.value, list):
            return node.value
        return node

    def visit_Expr(self, node):
        node = self.generic_visit(node)
        if isinstance(node.value, list):
            return node.value
        return node

    def visit_YieldFrom(self, node):
        if isinstance(node.value, ast.Call):
            func = node.value
            if (not isinstance(func.func, ast.Attribute)
                    and isinstance(func.func.value, ast.Name)
                    and func.func.value.id == "self"):
                raise NotImplementedError(ast.dump(func))
            tree = copy.deepcopy(self.method_name_map[func.func.attr])
            if (isinstance(tree, ast.FunctionDef) and
                    tree.name[0:5] == "make_"):
                symbol_table = {}
                # Skip self arg
                for arg, param in zip(func.args, tree.args.args[1:]):
                    symbol_table[param.arg] = arg
                tree = replace_symbols(tree, symbol_table)
                # TODO: Assumes make function is well formed
                # TODO: Should use an ast_tools macro symbol replacer
                # instead
                tree = tree.body[0]
            # TODO: Assumes function signature and return is well formed
            return tree.body[:-1]
        else:
            return node


def inline_yield_from_functions(tree, method_name_map):
    return YieldFromFunctionInliner(method_name_map).visit(tree)
