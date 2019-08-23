import magma.ast_utils as ast_utils
import ast
import astor
from .verilog_utils import Context, CollectInitialWidthsAndTypes, PromoteWidths
import ast
import magma as m
from .combinational import m_dot
import veriloggen as vg


class ProcessReturns(ast.NodeTransformer):
    def __init__(self, outputs):
        self.len_outputs = len(outputs)

    def visit_Return(self, node):
        if self.len_outputs > 1:
            assert isinstance(node.value, ast.Tuple)
            return [
                ast.Assign(
                    [ast.Name(f"O{i}", ast.Load())],
                    node.value.elts[0]
                )
                for i in range(len(self.outputs))
            ]
        else:
            return ast.Assign(
                [ast.Name(f"O", ast.Load())],
                node.value
            )


def to_type_str(type_):
    if isinstance(type_, m.BitKind):
        return "bit"
    elif isinstance(type_, m.UIntKind):
        return "uint"
    elif isinstance(type_, m.BitsKind):
        return "bits"
    else:
        raise NotImplementedError(type_)


class NameCollector(ast.NodeVisitor):
    def __init__(self, ctx):
        self.names = set()
        self.ctx = ctx

    def visit_Name(self, node):
        if self.ctx is None or isinstance(node.ctx, self.ctx):
            self.names.add(node.id)


def collect_names(tree, ctx=None):
    visitor = NameCollector(ctx)
    visitor.visit(tree)
    return visitor.names


def get_io_width(type_):
    if type_ is m.Bit:
        return None
    elif isinstance(type_, m.ArrayKind):
        if isinstance(type_.T, m.ArrayKind):
            elem_width = get_io_width(type_.T)
            if isinstance(elem_width, tuple):
                return (type_.N, ) + elem_width
            else:
                return (type_.N, elem_width)
        else:
            return type_.N
    else:
        raise NotImplementedError(type_)


def get_length(t):
    try:
        # assume flattened type, so it must be an array of Bits or a Bit
        return len(t)
    except Exception:
        # Bit is treated as length 1
        return 1


@ast_utils.inspect_enclosing_env
def combinational_to_verilog(defn_env, fn):
    tree = ast_utils.get_ast(fn).body[0]
    # TODO: Flatten types pass
    ctx = Context(tree.name)
    inputs = {}
    outputs = {}
    width_table = {}
    type_table = {}
    for arg in tree.args.args:
        type_ = eval(astor.to_source(arg.annotation), defn_env)
        inputs[arg.arg] = get_length(type_)
        width_table[arg.arg] = get_io_width(type_)
        type_table[arg.arg] = to_type_str(type_)
    if isinstance(tree.returns, ast.Tuple):
        for i, elt in enumerate(tree.returns.elts):
            type_ = eval(astor.to_source(elt), defn_env)
            outputs[f"O{i}"] = get_length(type_)
            width_table[f"O{i}"] = get_io_width(type_)
            type_table[f"O{i}"] = to_type_str(type_)
    else:
        type_ = eval(astor.to_source(tree.returns), defn_env)
        outputs["O"] = get_length(type_)
        width_table["O"] = get_io_width(type_)
        type_table["O"] = to_type_str(type_)
    ctx.declare_ports(inputs, outputs)
    names = collect_names(tree, ctx=ast.Store)

    for io_port in inputs.keys() | outputs.keys():
        if io_port in names:
            names.remove(io_port)

    CollectInitialWidthsAndTypes(width_table, type_table, defn_env).visit(tree)
    PromoteWidths(width_table, type_table).visit(tree)

    for name in names:
        # TODO: We declare reg to avoid procedural assignment to wire, ideally
        # we'd use logic in system verilog for clarity (not a register)
        ctx.declare_reg(name, width_table[name])
    tree = ProcessReturns(outputs).visit(tree)
    body = list(filter(lambda x: x is not None, map(ctx.translate, tree.body)))
    ctx.module.Always(vg.SensitiveAll())(body)
    verilog_str = ctx.to_verilog()
    defn =  m.DefineFromVerilog(verilog_str, type_map={"CLK": m.In(m.Clock)},
                               target_modules=[tree.name])[0]
    return lambda *args: defn()(*args)
