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
        self.last_name = defaultdict(lambda : "")
        self.var_counter = defaultdict(lambda : -1)

    def write_name(self, var):
        self.var_counter[var] += 1
        self.last_name[var] = f"{var}_{self.var_counter[var]}"

    def visit_Assign(self, node):
        node.value = self.visit(node.value)
        node.targets = flatten([self.visit(t) for t in node.targets])
        return node

    def visit_FunctionDef(self, node):
        node.body = flatten([self.visit(s) for s in node.body])
        return node

    def visit_Name(self, node):
        if node.id not in self.last_name:
            self.last_name[node.id] = node.id
        if isinstance(node.ctx, ast.Store):
            self.write_name(node.id)
        node.id = f"{self.last_name[node.id]}"
        return node

    def visit_If(self, node):
        true_name = {}
        false_name = dict(self.last_name)

        test = self.visit(node.test)
        result = flatten([self.visit(s) for s in node.body])
        true_name = dict(self.last_name)

        if node.orelse:
            self.last_name = false_name
            result += flatten([self.visit(s) for s in node.orelse])
            false_name = dict(self.last_name)

        self.last_name = {**true_name, **false_name}
        for var in self.last_name.keys():
            if var in true_name and var in false_name and true_name[var] != false_name[var]:
                phi_args = [
                    ast.Name(false_name[var], ast.Load()),
                    ast.Name(true_name[var], ast.Load())
                ]

                self.write_name(var)
                result.append(ast.Assign(
                    [ast.Name(self.last_name[var], ast.Store())],
                    ast.Call(ast.Name("phi", ast.Load()), [
                        ast.List(phi_args, ast.Load()),
                        test
                    ], [])))
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
