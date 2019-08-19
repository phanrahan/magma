import ast
import astor
import magma.ast_utils as ast_utils
import types
import collections
from staticfg import CFGBuilder
import typing
from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT
import magma as m


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
    channel_returns = []
    returns = ""
    for key, value in IO.items():
        type_ = repr(value.type_)
        if value.type_.isinput():
            new_args.extend((
                ast.arg(key, type_),
                ast.arg(key + "_valid", "Bit"),
            ))
        elif value.type_.isoutput():
            type_ = f"{type_}"
            valid_type = "Out(Bit)"
            returns += f"{type_}, Bit"
            channel_returns.extend((ast.Name(key, ast.Load()),
                                    ast.Name(key + "_valid", ast.Load())))
        else:
            assert False, "Found InOut"
    tree.args.args = new_args
    tree.returns = "(" + returns + ")"
    return tree, channel_returns


def rewrite_channel_references(tree, channels):
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
                channels[node.targets[0].id] = \
                    channels[node.value.func.value.id]
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


def add_channel_defaults(tree, channels):
    for key, value in channels.items():
        if value.direction == "output":
            tree.body.insert(0, ast.Assign(
                [ast.Name(key + "_valid", ast.Store())],
                ast.parse(f"m.bit(0)").body[0].value
            ))
            # For now we default channel output values to 0, ideally this is
            # "X" and the compiler can choose something smarter (e.g. wire it
            # to an input port of the same type, so we don't need a constant
            # value, or one of the possible values, since there will already be
            # a wire connecting them up)
            tree.body.insert(0, ast.Assign(
                [ast.Name(key, ast.Store())],
                ast.parse(f"m.bits(0, {len(value.type_)})").body[0].value
            ))
    return tree


def transform_for_loops_to_counters(tree):
    counters = {}

    class Transformer(FlattenTransformer):
        def __init__(self):
            super().__init__()
            self.active_counters = []

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
            self.active_counters.append(node.target.id)
            node.body = [self.visit(s) for s in node.body]
            self.active_counters.pop()
            return node.body

        def visit_Name(self, node):
            if node.id in self.active_counters:
                return ast.Attribute(ast.Name("self", node.ctx), node.id)
            return node

    return Transformer().visit(tree), counters


def gen_counters(counters):
    counter_decls = []
    counter_types = set()
    for key, value in counters.items():
        if value.start != 0:
            raise NotImplementedError()
        counter_type = f"Counter_{value.start}_{value.end}_{value.step}"
        counter_types.add(
            f"{counter_type} ="
            f" gen_counter({value.start}, {value.end}, {value.step})"
        )
        counter_decls.append(
            f"self.{key}: {counter_type} = {counter_type}()"
        )

    counter_types = "\n".join(counter_types)
    counter_decls = "\n            ".join(counter_decls)
    return counter_types, counter_decls


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


def _coroutine(
        defn_env: dict,
        fn: types.FunctionType,
        combinational_decorator: typing.Callable):
    tree = ast_utils.get_func_ast(fn)
    IO = collect_IO(tree, defn_env)
    tree, channel_returns = rewrite_channel_interface(tree, IO)

    channels = {}
    for key, value in IO.items():
        if isinstance(value, Channel):
            channels[key] = value

    tree = rewrite_channel_references(tree, channels)
    tree = add_channel_defaults(tree, channels)
    tree, counters = transform_for_loops_to_counters(tree)
    counter_types, counter_decls = gen_counters(counters)


    # tree = add_counters_to_interface(tree, counters)

    cfg = CFGBuilder().build(fn.__name__, ast.Module([tree]))
    cfg = cfg.functioncfgs[fn.__name__]
    num_states = count_num_yields(cfg)
    if num_states == 1:
        tree = strip_while_true_and_yields(tree)
    else:
        raise NotImplementedError(f"num_states={num_states}")

    tree.decorator_list = []
    tree.name = "__call__"
    tree.args.args.insert(0, ast.Name("self", ast.Load()))
    tree.body.append(ast.Return(ast.Tuple(channel_returns, ast.Load())))
    call_str = "\n        ".join(astor.to_source(tree).splitlines())
    circuit_def = f"""\
def gen_counter(start, end, step):
    N = (end - 1).bit_length()
    T = m.UInt[N]
    @m.circuit.sequential(async_reset=False)
    class Counter:
        def __init__(self):
            self.value: T = m.bits(start, N)

        def __call__(self) -> T:
            value = self.value
            if value == m.bits(end, N):
                self.value = m.bits(start, N)
            else:
                self.value = self.value + m.bits(step, N)
            return value
    return Counter

{counter_types}

def make_{fn.__name__}(sequential):
    @sequential
    class {fn.__name__}:
        def __init__(self):
            {counter_decls}

        {call_str}
    return {fn.__name__}
"""
    print(circuit_def)
    tree = ast.parse(circuit_def)
    tree.body.insert(0, ast.parse("import magma as m").body[0])
    tree.body.insert(0, ast.parse("from magma import Bit, Bits").body[0])
    circuit_def_constructor = ast_utils.compile_function_to_file(
        tree, 'make_' + fn.__name__, defn_env)
    circuit_def = circuit_def_constructor(combinational_decorator)

    return circuit_def


def coroutine(
        fn=None,
        *,
        decorators: typing.Optional[typing.Sequence[typing.Callable]] = None,
        ):

    exec(_SKIP_FRAME_DEBUG_STMT)
    if decorators is not None:
        assert fn is None
        def wrapped(fn):
            exec(_SKIP_FRAME_DEBUG_STMT)
            nonlocal decorators
            decorators = list(itertools.chain(decorators, [wrapped]))
            wrapped_coroutine = ast_utils.inspect_enclosing_env(
                    _coroutine,
                    decorators=decorators)
            sequential = m.circuit.sequential(decorators=decorators)
            return wrapped_coroutine(fn, sequential)
        return wrapped
    else:
        assert fn is not None
        wrapped_coroutine = ast_utils.inspect_enclosing_env(
                _coroutine,
                decorators=[coroutine]
        )
        sequential = m.circuit.sequential(decorators=[coroutine])
        return wrapped_coroutine(fn, sequential)
