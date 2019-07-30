import ast
import astor
import magma.ast_utils as ast_utils
import types
import collections
from staticfg import CFGBuilder


class Channel:
    def __init__(self, type_):
        self.type_ = type_
        self.direction = None

    def qualify(self, direction):
        self.direction = direction
        self.type_ = self.type_.qualify(direction)
        return self


class Counter:
    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return f"Counter({self.start}, {self.end}, {self.step})"


class FlattenTransformer(ast.NodeTransformer):
    """
    Handles the case when nodes are replaced with a list of nodes
    """
    def visit(self, node):
        node = super().visit(node)
        if hasattr(node, 'body') and not isinstance(node, ast.IfExp):
            new_body = []
            for statement in node.body:
                if isinstance(statement, list):
                    new_body.extend(statement)
                else:
                    new_body.append(statement)
            node.body = new_body
        return node


def collect_IO(tree, defn_env):
    IO = {}
    for arg in tree.args.args:
        IO[arg.arg] = eval(astor.to_source(arg.annotation).rstrip(), defn_env)
    return IO


def rewrite_channel_interface(tree, IO):
    new_args = []
    for key, value in IO.items():
        type_ = repr(value.type_)
        if value.type_.isinput():
            type_ = f"In({type_})"
            valid_type = "In(Bit)"
        elif value.type_.isoutput():
            type_ = f"Out({type_})"
            valid_type = "Out(Bit)"
        else:
            assert False, "Found InOut"
        type_ = ast.parse(type_).body[0].value
        new_args.extend((
            ast.arg(key, type_),
            ast.arg(key + "_valid", valid_type),
        ))
    tree.args.args = new_args
    return tree


def rewrite_channel_references(tree, IO):
    channels = set()
    for key, value in IO.items():
        if isinstance(value, Channel):
            channels.add(key)

    class Transformer(FlattenTransformer):
        def visit_Assign(self, node):
            if isinstance(node.value, ast.Call) and \
                    isinstance(node.value.func, ast.Attribute) and \
                    node.value.func.attr == "pop":
                assert isinstance(node.value.func.value, ast.Name) and \
                    node.value.func.value.id in channels, \
                    "Found pop on non-channel"
                assert len(node.targets) == 1 and \
                    isinstance(node.targets[0], ast.Name), \
                    "Found unsupported pop target"
                channels.add(node.targets[0].id)
                valid = ast.Assign(
                    [ast.Name(node.targets[0].id + "_valid", ast.Store())],
                    ast.Name(node.value.func.value.id + "_valid", ast.Load())
                )
                node.value = node.value.func.value
                return [node, valid]
            return node

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and \
                    node.func.attr == "push":
                assert len(node.args) == 1 and \
                    isinstance(node.args[0], ast.Name) and \
                    node.args[0].id in channels, "Found malformed push"
                assert isinstance(node.func.value, ast.Name), \
                    "Found malformed push value"
                return [
                    ast.Assign([ast.Name(node.func.value.id, ast.Store())],
                               node.args[0]),
                    ast.Assign([ast.Name(node.func.value.id + "_valid",
                                         ast.Store())],
                               ast.Name(node.args[0].id + "_valid",
                                        ast.Load()))
                ]
            return node

    return Transformer().visit(tree)


def transform_for_loops_to_counters(tree):
    counters = {}

    class Transformer(FlattenTransformer):
        def visit_For(self, node):
            assert isinstance(node.iter, ast.Call) and \
                isinstance(node.iter.func, ast.Name) and \
                node.iter.func.id == "range" and \
                isinstance(node.target, ast.Name), \
                f"Found unsupported for loop {ast.dump(ndoe)}"
            assert not node.iter.keywords, "kwargs not implemented"
            if len(node.iter.args) == 1:
                counters[node.target.id] = Counter(0, node.iter.args[0].n, 1)
            else:
                assert False, "Case not implemented"
            node.body = [self.visit(s) for s in node.body]
            return node.body

    return Transformer().visit(tree), counters


def add_counters_to_interface(tree, counters):
    for key, value in counters.items():
        tree.args.args.append(
            ast.arg(key, f"In(Bits[{value.end.bit_length()}])")
        )
    return tree


def count_num_yields(cfg):
    return sum(map(lambda block: block.get_source() == "yield\n", cfg))


def strip_while_true_and_yields(tree):
    class Transformer(FlattenTransformer):
        def visit_While(self, node):
            assert isinstance(node.test, ast.NameConstant) and \
                node.test.value is True, "Expected top level while True"
            return [self.visit(s) for s in node.body]

        def visit_Yield(self, node):
            return []  # removed by FlattenTransformer
    return Transformer().visit(tree)


@ast_utils.inspect_enclosing_env
def coroutine(defn_env: dict, fn: types.FunctionType):
    tree = ast_utils.get_func_ast(fn)
    IO = collect_IO(tree, defn_env)
    tree = rewrite_channel_interface(tree, IO)
    tree = rewrite_channel_references(tree, IO)
    tree, counters = transform_for_loops_to_counters(tree)
    tree = add_counters_to_interface(tree, counters)

    cfg = CFGBuilder().build(fn.__name__, ast.Module([tree]))
    cfg = cfg.functioncfgs[fn.__name__]
    num_states = count_num_yields(cfg)
    if num_states == 1:
        tree = strip_while_true_and_yields(tree)
    else:
        raise NotImplementedError(f"num_states={num_states}")

    # cfg.build_visual(fn.__name__, 'pdf')
    print(IO)
    print(counters)
    print(astor.to_source(tree))
    assert False
