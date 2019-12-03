import os
import magma.ast_utils as ast_utils
import ast
import astor
from .verilog_utils import CollectInitialWidthsAndTypes, PromoteWidths, \
    RemoveBits
from .sequential import get_initial_value_map, RewriteSelfAttributes
import magma as m
import kratos
from magma.config import get_debug_mode


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


def process_comb_func(defn_env, fn, circ_name, registers={}, init_fn=None):
    tree = ast_utils.get_ast(fn).body[0]
    # TODO: Flatten types pass
    inputs = {}
    outputs = {}
    width_table = {}
    type_table = {}
    if registers:
        tree = RewriteSelfAttributes(registers).visit(tree)
        for name, info in registers.items():
            width = 1 if isinstance(info[3], m._BitKind) else len(info[3])
            width_table["self_" + name + "_I"] = width
            type_table["self_" + name + "_I"] = to_type_str(info[2])
            width_table["self_" + name + "_O"] = width
            type_table["self_" + name + "_O"] = to_type_str(info[2])
    for arg in tree.args.args:
        if arg.arg == "self":
            continue
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

    names = [arg.arg for arg in tree.args.args if arg.arg != "self"]
    types = [arg.annotation for arg in tree.args.args if arg.arg != "self"]
    IO = []
    for name, type_ in zip(names, types):
        IO += [name, m.In(eval(compile(ast.Expression(type_), "",
                                       mode="eval")))]
    if isinstance(tree.returns, ast.Tuple):
        for i, elt in enumerate(tree.returns.elts):
            IO += [f"O{i}", m.Out(eval(compile(ast.Expression(elt), "",
                                               mode="eval")))]
    else:
        IO += [f"O", m.Out(eval(compile(ast.Expression(tree.returns), "",
                                        mode="eval")))]
    if registers:
        IO += m.ClockInterface(has_async_reset=True)

    names = collect_names(tree, ctx=ast.Store) | \
        set(f"self_{name}_I" for name in registers) | \
        set(f"self_{name}_O" for name in registers)

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

    # obtain the filename and line number information
    # due to the multi-line info, the offset calculation is a little bit
    # complicated
    lineno_offset = tree.body[0].lineno
    fn_ln = kratos.pyast.get_fn(fn), kratos.pyast.get_ln(fn) + lineno_offset - 2

    print(astor.to_source(tree))
    func = ast_utils.compile_function_to_file(tree, fn.__name__, defn_env)

    class Module(kratos.Generator):
        def __init__(self):
            super().__init__(circ_name, get_debug_mode())
            for key, value in inputs.items():
                setattr(self, key, self.input(key, value))
            for key, value in outputs.items():
                setattr(self, key, self.output(key, value))
            for name in names:
                setattr(self, name, self.var(name, width_table[name]))
            if registers:
                self.CLK = self.clock("CLK")
                self.ASYNCRESET = self.reset("ASYNCRESET")

                reg_updates = "\n        ".join(
                    f"self.self_{name}_O = self.self_{name}_I"
                    for name in registers
                )
                reg_inits = []
                for reg, info in registers.items():
                    eval_value = info[3]
                    try:
                        init = int(eval_value)
                    except Exception as e:
                        raise NotImplementedError(eval_value)
                    reg_inits.append(
                        f"self.self_{reg}_O = {init}"
                    )
                reg_inits = "\n        ".join(reg_inits)
                code = f"""
from kratos import always, posedge

@always((posedge, "CLK"), (posedge, "ASYNCRESET"))
def seq_code_block(self):
    if self.ASYNCRESET:
        {reg_inits}
    else:
        {reg_updates}
"""
                lineno_offset = ast_utils.get_ast(init_fn).body[0].lineno
                init_fn_ln = kratos.pyast.get_fn(init_fn), \
                    kratos.pyast.get_ln(init_fn) + lineno_offset - 2
                seq_code_block = ast_utils.compile_function_to_file(
                    ast.parse(code), "seq_code_block", defn_env)
                # TODO: What lines should this block map to?  This is implict
                # in sequential, for now we can just map it to __init__
                seq_block = self.add_code(seq_code_block, fn_ln=init_fn_ln)

            block = self.add_code(func, fn_ln=fn_ln)
            # set locals, which is the inputs and outputs
            for key in inputs:
                block.stmt().add_scope_variable(key, key, True)
            for key in names:
                block.stmt().add_scope_variable(key, key, True)

    os.makedirs(".magma", exist_ok=True)
    filename = f".magma/{circ_name}-kratos.sv"
    mod = Module()

    kratos.verilog(mod, filename=filename, insert_debug_info=get_debug_mode())
    defn = m.DefineCircuit(circ_name, *IO, kratos=mod)
    with open(filename, 'r') as f:
        defn.verilogFile = f.read()
    m.EndCircuit()
    return defn


@ast_utils.inspect_enclosing_env
def combinational_to_verilog(defn_env, fn):
    return lambda *args: process_comb_func(defn_env, fn, fn.__name__)()(*args)


def sequential_to_verilog(async_reset):
    if not async_reset:
        raise NotImplementedError()

    @ast_utils.inspect_enclosing_env
    def wrapped(defn_env, cls):
        initial_value_map = get_initial_value_map(cls.__init__, defn_env)
        return process_comb_func(defn_env, cls.__call__, cls.__name__,
                                 initial_value_map, cls.__init__)
    return wrapped
