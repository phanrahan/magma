import os
import magma.ast_utils as ast_utils
import ast
import astor
from .verilog_utils import CollectInitialWidthsAndTypes, PromoteWidths, \
    RemoveBits
import magma as m
import kratos
from magma.config import get_debug_mode


class SpecializeConstantInts(ast.NodeTransformer):
    def __init__(self, defn_env):
        self.defn_env = defn_env

    def visit_Name(self, node):
        if node.id in self.defn_env:
            value = self.defn_env[node.id]
            if isinstance(value, int):
                return ast.Num(value)
        return node


class RewriteSelfAttributes(ast.NodeTransformer):
    def __init__(self, initial_value_map):
        self.initial_value_map = initial_value_map
        self.calls_seen = []

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == "self":
            return ast.Name(f"self_{node.attr}_I", node.ctx)
        return self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and \
                isinstance(node.func.value, ast.Name) and \
                node.func.value.id == "self":
            attr = node.func.attr
            assert attr in self.initial_value_map, \
                "Reference to self that was not initialized"
            ret = []
            ports = self.initial_value_map[attr][3].interface.inputs()
            for name, value in zip(ports, node.args):
                name = magma_value(name)
                ret.append(ast.parse(
                    f"self_{attr}_{name} = {astor.to_source(value).rstrip()}"
                ).body[0])
            self.calls_seen.extend(ret)
            func = astor.to_source(node.func).rstrip()
            outputs = self.initial_value_map[attr][3].interface.outputs()
            if len(outputs) == 1:
                name = outputs[0]
                name = magma_value(name)
                return ast.Name(f"self_{attr}_{name}", ast.Load())
            else:
                assert outputs, "Expected module with at least one output"
                return ast.Tuple([ast.Name(f"self_{attr}_{magma_value(output)}",
                                           ast.Load()) for output in outputs],
                                 ast.Load())
        elif (isinstance(node.func, ast.Attribute) and
                isinstance(node.func.value, ast.Attribute) and
                isinstance(node.func.value.value, ast.Name) and
                node.func.value.value.id == "self" and
                node.func.attr == "prev"):
            return ast.Name(f"self_{node.func.value.attr}_O", ast.Load())
        else:
            self.generic_visit(node)
        return node

    def visit_If(self, node):
        node.test = self.visit(node.test)
        for attr in ["body", "orelse"]:
            new_body = []
            for item in getattr(node, attr):
                new_body.append(self.visit(item))
            if self.calls_seen:
                new_body = self.calls_seen + new_body
                self.calls_seen = []
            setattr(node, attr, new_body)
        return node


def get_initial_value_map(init_func, defn_env):
    """
    Parses __init__ funciton of the form
        def __init__(self):
            self.x = m.bits(0, 2)
            self.y = m.bits(0, 4)
    Returns a map from instance attributes to their initial values
    For the above example,
        {'x': <_ast.Call object at 0x109c17fd0>,
         'y': <_ast.Call object at 0x109c17470>}
    TODO: Should we allow arbitrary code in the definition? For now, the user
    can write any meta code outside the class definition, which makes the
    design of this simpler
    """
    initial_value_map = {}
    if init_func is object.__init__:
        # Handle case when no __init__
        return initial_value_map
    init_def = ast_utils.get_ast(init_func).body[0]
    # init_def = ExecuteEscapedPythonExpressions(defn_env).visit(init_def)
    init_def = SpecializeConstantInts(defn_env).visit(init_def)
    for stmt in init_def.body:
        # We only support basic assignments of the form
        #     self.x: m.Bits(2) = m.bits(0, 2)
        assert isinstance(stmt, ast.AnnAssign)
        assert isinstance(stmt.target, ast.Attribute)
        assert isinstance(stmt.target.value, ast.Name)
        assert stmt.target.value.id == "self"

        # TODO: Should we deal with multiple assignments? For now we take the
        # last one
        class Tmp(m.Circuit):
            eval_type = eval(astor.to_source(stmt.annotation).rstrip(),
                             defn_env)
            eval_value = eval(astor.to_source(stmt.value).rstrip(), defn_env)
        initial_value_map[stmt.target.attr] = (stmt.value, stmt.annotation,
                                               Tmp.eval_type,
                                               Tmp.eval_value)
    return initial_value_map


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
                    node.value.elts[0],
                    lineno=node.lineno
                )
                for i in range(self.len_outputs)
            ]
        else:
            return ast.Assign(
                [ast.parse(f"self.O").body[0].value],
                node.value,
                lineno=node.lineno
            )


def to_type_str(type_):
    if issubclass(type_, m.Digital):
        return "bit"
    elif issubclass(type_, m.UInt):
        return "uint"
    elif issubclass(type_, m.Bits):
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
    elif isinstance(type_, m.ArrayMeta):
        if isinstance(type_.T, m.ArrayMeta):
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


def build_kratos_debug_info(circuit, is_top):
    inst_to_defn_map = {}
    for instance in circuit.instances:
        instance_inst_to_defn_map = \
            build_kratos_debug_info(type(instance), is_top=False)
        for k, v in instance_inst_to_defn_map.values():
            key = instance.name + "." + k
            if is_top:
                key = circuit.name + "." + key
            inst_to_defn_map[key] = v
        inst_name = instance.name
        if is_top:
            inst_name = circuit.name + "." + instance.name
        if instance.kratos is not None:
            inst_to_defn_map[inst_name] = instance.kratos
    return inst_to_defn_map


def process_func(defn_env, fn, circ_name, registers=None, debug=False):
    tree = ast_utils.get_ast(fn).body[0]
    # TODO: Flatten types pass
    inputs = {}
    outputs = {}
    width_table = {}
    type_table = {}
    # determine if it's sequential or combinational
    combinational = registers is None
    if not combinational:
        tree = RewriteSelfAttributes(registers).visit(tree)
        for name, info in registers.items():
            width = 1 if isinstance(info[3], m.DigitalMeta) else len(info[3])
            width_table["self_" + name + "_I"] = width
            type_table["self_" + name + "_I"] = to_type_str(info[2])
            width_table["self_" + name + "_O"] = width
            type_table["self_" + name + "_O"] = to_type_str(info[2])
        for name in reversed(tuple(registers.keys())):
            tree.body.insert(
                0, ast.parse(f"self_{name}_I = self_{name}_O")
            )
    else:
        registers = {}
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
    fn_ln = kratos.pyast.get_fn(fn), kratos.pyast.get_ln(fn)

    print(astor.to_source(tree))

    class Module(kratos.Generator):
        def __init__(self):
            super().__init__(circ_name, get_debug_mode() or debug)
            for key, value in inputs.items():
                setattr(self, key, self.input(key, value))
            for key, value in outputs.items():
                setattr(self, key, self.output(key, value))
            for name in names:
                setattr(self, name, self.var(name, width_table[name]))

            block = self.add_code(tree, fn_ln=fn_ln)
            if not combinational:
                # TODO: add option to do reset low
                reset_high = True
                self.CLK = self.clock("CLK")
                self.ASYNCRESET = self.reset("ASYNCRESET")
                sensitivity = [(kratos.posedge, self.CLK),
                               (kratos.posedge
                                if reset_high else kratos.negedge,
                                self.ASYNCRESET)]
                seq = self.sequential(*sensitivity)
                # add an if statement
                if reset_high:
                    if_ = seq.if_(self.ASYNCRESET)
                else:
                    if_ = seq.if_(self.ASYNCRESET.r_not())
                for reg, values in registers.items():
                    try:
                        init = int(values[3])
                    except Exception:
                        raise NotImplementedError(values[3])
                    if_.then_(self.vars[f"self_{reg}_O"].assign(init))
                for n in registers:
                    if_.else_(self.vars[f"self_{n}_O"].assign(
                        self.vars[f"self_{n}_I"]))

            # set locals, which is the inputs and outputs
            for key in inputs:
                block.stmt().add_scope_variable(key, key, True)
            for key in names:
                if "self_" in key:
                    continue
                block.stmt().add_scope_variable(key, key, True)
            if registers:
                for key in registers:
                    block.stmt().add_scope_variable(key, f"self_{key}_I", True)

    os.makedirs(".magma", exist_ok=True)
    filename = f".magma/{circ_name}-kratos.sv"
    mod = Module()

    kratos.verilog(mod, filename=filename,
                   insert_debug_info=get_debug_mode() or debug)
    io_dict = {key: value for key, value in zip(IO[::2], IO[1::2])}

    class _Defn(m.Circuit):
        name = circ_name
        io = m.IO(**io_dict)
        kratos = mod
    with open(filename, 'r') as f:
        _Defn.verilogFile = f.read()
    return _Defn


def combinational_to_verilog(debug=False):
    @ast_utils.inspect_enclosing_env
    def wrapped(defn_env, fn):
        return lambda *args: process_func(defn_env, fn, fn.__name__,
                                          debug=debug)()(*args)
    return wrapped


def sequential_to_verilog(async_reset, debug=False):
    if not async_reset:
        raise NotImplementedError()

    @ast_utils.inspect_enclosing_env
    def wrapped(defn_env, cls):
        initial_value_map = get_initial_value_map(cls.__init__, defn_env)
        return process_func(defn_env, cls.__call__, cls.__name__,
                            initial_value_map, debug=debug)
    return wrapped
