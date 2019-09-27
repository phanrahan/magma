import os
import magma.ast_utils as ast_utils
import ast
import astor
from .verilog_utils import CollectInitialWidthsAndTypes, PromoteWidths, \
    RemoveBits
import magma as m
import kratos


class ProcessNames(ast.NodeTransformer):
    def __init__(self, inputs, outputs, names):
        self.names = list(inputs.keys()) + list(outputs.keys()) + list(names)

    def visit_Name(self, node):
        if node.id in self.names:
            return ast.parse(f"self.{node.id}").body[0].value
        return node


class ProcessReturns(ast.NodeTransformer):
    def __init__(self, outputs):
        self.len_outputs = len(outputs)

    def visit_Return(self, node):
        if self.len_outputs > 1:
            assert isinstance(node.value, ast.Tuple)
            return [
                ast.Assign(
                    [ast.parse(f"self.O{i}").body[0].value],
                    node.value.elts[0]
                )
                for i in range(self.len_outputs)
            ]
        else:
            return ast.Assign(
                [ast.parse(f"self.O").body[0].value],
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

    names = [arg.arg for arg in tree.args.args]
    types = [arg.annotation for arg in tree.args.args]
    IO = []
    for name, type_ in zip(names, types):
        IO += [name, m.In(eval(compile(ast.Expression(type_), "", mode="eval")))]
    if isinstance(tree.returns, ast.Tuple):
        for i, elt in enumerate(tree.returns.elts):
            IO += [f"O{i}", m.Out(eval(compile(ast.Expression(elt), "", mode="eval")))]
    else:
        IO += [f"O", m.Out(eval(compile(ast.Expression(tree.returns), "", mode="eval")))]

    names = collect_names(tree, ctx=ast.Store)

    for io_port in inputs.keys() | outputs.keys():
        if io_port in names:
            names.remove(io_port)

    CollectInitialWidthsAndTypes(width_table, type_table, defn_env).visit(tree)
    PromoteWidths(width_table, type_table).visit(tree)
    tree = ProcessNames(inputs, outputs, names).visit(tree)
    tree = ProcessReturns(outputs).visit(tree)
    tree = RemoveBits().visit(tree)
    tree.args.args = [ast.arg("self", None)]
    tree.decorator_list = []
    tree.returns = None

    print(astor.to_source(tree))
    func = ast_utils.compile_function_to_file(tree, fn.__name__, defn_env)


    class Module(kratos.Generator):
        def __init__(self):
            super().__init__(tree.name, False)
            for key, value in inputs.items():
                setattr(self, key, self.input(key, value))
            for key, value in outputs.items():
                setattr(self, key, self.output(key, value))
            for name in names:
                setattr(self, name, self.var(name, width_table[name]))
            self.add_code(func)

    os.makedirs(".magma", exist_ok=True)
    filename = f".magma/{tree.name}-kratos.sv"
    kratos.verilog(Module(), filename=filename)
    defn = m.DefineCircuit(tree.name, *IO)
    with open(filename, 'r') as f:
        defn.verilogFile = f.read()
    # defn =  m.DefineFromVerilogFile(filename, type_map={"CLK": m.In(m.Clock)},
    #                                 target_modules=[tree.name])[0]
    return lambda *args: defn()(*args)
