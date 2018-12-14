import magma.ast_utils as ast_utils
import ast
import types
from collections import defaultdict
import inspect


def flatten(l : list):
    """
    Non-recursive flatten that ignores non-list children
    """
    flat = []
    for item in l:
        if not isinstance(item, list):
            item = [item]
        flat += item
    return flat


class SSAVisitor(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.var_counter = defaultdict(lambda : -1)

    def visit_FunctionDef(self, node):
        node.body = flatten([self.visit(s) for s in node.body])
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.var_counter[node.id] += 1
        if isinstance(node.ctx, ast.Store) or node.id in self.var_counter:
            node.id += f"_{self.var_counter[node.id]}"
        return node

    def visit_If(self, node):
        false_var_counter = dict(self.var_counter)
        test = self.visit(node.test)
        result = flatten([self.visit(s) for s in node.body])
        if node.orelse:
            false_var_counter = dict(self.var_counter)
            result += flatten([self.visit(s) for s in node.orelse])
        for var, count in self.var_counter.items():
            if var in false_var_counter and count != false_var_counter[var]:
                phi_args = [
                    ast.Name(f"{var}_{count}", ast.Load()),
                    ast.Name(f"{var}_{false_var_counter[var]}", ast.Load())
                ]
                if not node.orelse:
                    phi_args = [phi_args[1], phi_args[0]]
                result.append(ast.Assign(
                    [ast.Name(f"{var}_{count + 1}", ast.Store())],
                    ast.Call(ast.Name("phi", ast.Load()), [
                        ast.List(phi_args, ast.Load()),
                        test
                    ], [])))
                self.var_counter[var] += 1
        return result


@ast_utils.inspect_enclosing_env
def ssa(defn_env : dict, fn : types.FunctionType):
    stack = inspect.stack()
    defn_env = {}
    for i in range(1, len(stack)):
        defn_env.update(stack[i].frame.f_locals)
        defn_env.update(stack[i].frame.f_globals)
    tree = ast_utils.get_func_ast(fn)
    tree.decorator_list = ast_utils.filter_decorator(ssa, tree.decorator_list, defn_env)
    tree = SSAVisitor().visit(tree)
    return ast_utils.compile_function_to_file(tree, defn_env=defn_env)
