import magma.ast_utils as ast_utils
import ast
import typing
from collections import defaultdict
import astor
import functools


def flatten(l: list):
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
    def __init__(self, phi_name):
        super().__init__()
        self.last_name = defaultdict(lambda: "")
        self.var_counter = defaultdict(lambda: -1)
        self.args = []
        self.cond_stack = []
        self.return_values = []
        self.phi_name = phi_name

    def write_name(self, var):
        self.var_counter[var] += 1
        self.last_name[var] = f"{var}_{self.var_counter[var]}"

    def visit_Assign(self, node):
        node.value = self.visit(node.value)
        node.targets = flatten([self.visit(t) for t in node.targets])
        return node

    def visit_FunctionDef(self, node):
        for a in node.args.args:
            self.args.append(a.arg)
            self.write_name(a.arg)
            a.arg = f"{a.arg}_0"
        node.body = flatten([self.visit(s) for s in node.body])
        return node

    def visit_Name(self, node):
        if node.id not in self.last_name:
            if node.id not in self.args and isinstance(node.ctx, ast.Store):
                self.last_name[node.id] = f"{node.id}_0"
            else:
                return node
        if isinstance(node.ctx, ast.Store):
            self.write_name(node.id)
        node.id = f"{self.last_name[node.id]}"
        return node

    def visit_If(self, node):
        false_name = dict(self.last_name)

        test = self.visit(node.test)
        self.cond_stack.append(test)
        result = flatten([self.visit(s) for s in node.body])
        true_name = dict(self.last_name)

        if node.orelse:
            self.last_name = false_name
            self.cond_stack[-1] = ast.UnaryOp(ast.Invert(),
                                              self.cond_stack[-1])
            result += flatten([self.visit(s) for s in node.orelse])
            false_name = dict(self.last_name)

        self.cond_stack.pop()

        self.last_name = {**true_name, **false_name}
        for var in self.last_name.keys():
            if var in true_name and var in false_name and \
                    true_name[var] != false_name[var]:
                phi_args = [
                    ast.Name(false_name[var], ast.Load()),
                    ast.Name(true_name[var], ast.Load())
                ]

                self.write_name(var)
                result.append(ast.Assign(
                    [ast.Name(self.last_name[var], ast.Store())],
                    ast.Call(ast.Name(self.phi_name, ast.Load()), [
                        ast.List(phi_args, ast.Load()),
                        test
                    ], [])))
        return result

    def visit_Return(self, node):
        self.return_values.append(self.cond_stack[:])
        node.value = self.visit(node.value)
        return node


class TransformReturn(ast.NodeTransformer):
    def __init__(self):
        self.counter = -1

    def visit_Return(self, node):
        self.counter += 1
        name = f"__magma_ssa_return_value_{self.counter}"
        return ast.Assign([ast.Name(name, ast.Store())], node.value)


class MoveReturn(ast.NodeTransformer):
    def visit_Return(self, node):
        return ast.Assign(
            [ast.Name(f"__magma_ssa_return_value", ast.Store())],
            node.value
        )


def convert_tree_to_ssa(tree: ast.AST, defn_env: dict, phi_name: str = "phi"):
    # tree = MoveReturn().visit(tree)
    # tree.body.append(
    #     ast.Return(ast.Name("__magma_ssa_return_value", ast.Load())))
    ssa_visitor = SSAVisitor(phi_name)
    tree = ssa_visitor.visit(tree)
    return_transformer = TransformReturn()
    tree = return_transformer.visit(tree)
    num_return_values = len(ssa_visitor.return_values)
    for i in reversed(range(num_return_values)):
        conds = ssa_visitor.return_values[i]
        name = f"__magma_ssa_return_value_{i}"
        if i == num_return_values - 1 or not conds:
            if isinstance(tree.returns, ast.Tuple):
                tree.body.append(ast.Assign(
                    [ast.Tuple([ast.Name(f"O{i}", ast.Store())
                     for i in range(len(tree.returns.elts))], ast.Store())],
                    ast.Name(name, ast.Load())
                ))
            else:
                tree.body.append(ast.Assign([ast.Name("O", ast.Load)],
                                            ast.Name(name, ast.Load())))
        else:
            cond = conds[-1]
            for c in conds[:-1]:
                cond = ast.BinOp(cond, ast.BitAnd(), c)
            if isinstance(tree.returns, ast.Tuple):
                for i in range(len(tree.returns.elts)):
                    tree.body.append(ast.Assign(
                        [ast.Name(f"O{i}", ast.Store())],
                        ast.Call(ast.Name(phi_name, ast.Load()), [
                            ast.List([
                                ast.Name(f"O{i}", ast.Load()),
                                ast.Subscript(ast.Name(name, ast.Load()),
                                              ast.Index(ast.Num(i)),
                                              ast.Load())
                            ], ast.Load()),
                            cond], []))
                    )
            else:
                tree.body.append(ast.Assign(
                    [ast.Name("O", ast.Store())],
                    ast.Call(ast.Name(phi_name, ast.Load()), [
                        ast.List([ast.Name("O", ast.Load()), ast.Name(name, ast.Load())],
                                 ast.Load()), cond], []))
                )
    return tree, ssa_visitor.args


def _ssa(defn_env: dict, phi: typing.Union[str, typing.Callable],
         fn: typing.Callable):
    tree = ast_utils.get_func_ast(fn)
    tree.decorator_list = ast_utils.filter_decorator(ssa,
                                                     tree.decorator_list,
                                                     defn_env)

    if isinstance(phi, str):
        phi_name = phi
    else:
        phi_name = ast_utils.gen_free_name(tree, defn_env)

    tree, _ = convert_tree_to_ssa(tree, defn_env, phi_name=phi_name)

    if not isinstance(phi, str):
        defn_env[phi_name] = phi

    tree.body.append(ast.Return(ast.Name("O", ast.Load())))
    return ast_utils.compile_function_to_file(tree, defn_env=defn_env)

@ast_utils.inspect_enclosing_env
def ssa(defn_env: dict, phi: typing.Union[str, typing.Callable] = "phi"):
    return functools.partial(_ssa, defn_env, phi)
