import inspect
import ast
from .util import get_ast
import astor
import magma.ast_utils as ast_utils
from magma.debug import debug_info
import functools


class RewriteSelfAttributes(ast.NodeTransformer):
    def visit_Attribute(self, node):
        assert isinstance(node.value, ast.Name)
        assert node.value.id == "self"
        return ast.Name(f"self_{node.attr}", ast.Load())


class RewriteReturn(ast.NodeTransformer):
    def __init__(self, initial_value_map):
        self.initial_value_map = initial_value_map

    def visit_Return(self, node):
        elts = []
        for name in self.initial_value_map:
            elts.append(ast.Name(f"self_{name}", ast.Load()))
        elts.append(node.value)
        node.value = ast.Tuple(elts, ast.Load())
        return node


def get_initial_value_map(init_func):
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
    init_def = get_ast(init_func).body[0]
    for stmt in init_def.body:
        # We only support basic assignments of the form
        #     self.x: m.Bits(2) = m.bits(0, 2)
        assert isinstance(stmt, ast.AnnAssign)
        assert isinstance(stmt.target, ast.Attribute)
        assert isinstance(stmt.target.value, ast.Name)
        assert stmt.target.value.id == "self"
        # TODO: Should we deal with multiple assignments? For now we take the
        # last one
        initial_value_map[stmt.target.attr] = (stmt.value, stmt.annotation)
    return initial_value_map


def get_io(call_def):
    """
    Parses a __call__ method of the form

        def __call__(self, I):
            O = self.y
            self.y = self.x
            self.x = I
            return O

    Returns a tuple
    [0]: the list of tuples containing the name and type of each input argument
         excluding `self`
    [1]: the output type
    """
    # Only support basic args for now
    assert not call_def.args.vararg
    assert not call_def.args.kwonlyargs
    assert not call_def.args.kwarg
    assert not call_def.args.defaults
    assert not call_def.args.kw_defaults

    # Skips self
    assert call_def.args.args[0].arg == "self"
    inputs = [(arg.arg, arg.annotation) for arg in call_def.args.args[1:]]
    return inputs, call_def.returns


circuit_definition_template = """
class {circuit_name}(m.Circuit):
    IO = {io_list}

    @classmethod
    def definition(io):
{register_instances}
        @m.circuit.combinational
        def {circuit_name}_comb({circuit_combinational_args}) -> ({circuit_combinational_output_type}):
{circuit_combinational_body}
        comb_out = {circuit_name}_comb({circuit_combinational_call_args})
{comb_out_wiring}
"""


def gen_register_instances(initial_value_map):
    """
    Generates a sequence of statements to instance a set of registers from
    `initial_value_map`.

    For example,

        initial_value_map = {'x': <_ast.Call object at 0x109c17fd0>,
                             'y': <_ast.Call object at 0x109c17470>}

    will generate

        x = Register(2, init=0)
        y = Register(4, init=0)

    """
    register_instances = ""
    for name, (value, type_) in initial_value_map.items():
        # TODO: Only support m.bits(x, y) for now
        assert isinstance(value, ast.Call) and \
            isinstance(value.func, ast.Attribute) and \
            isinstance(value.func.value, ast.Name) and \
            value.func.value.id == "m" and \
            value.func.attr == "bits"
        assert isinstance(value.args[0], ast.Num)
        assert isinstance(value.args[1], ast.Num)
        n = value.args[1].n
        init = value.args[0].n
        register_instances += f"        {name} = Register({n}, init={init})\n"
    return register_instances


def gen_io_list(inputs, output_type):
    io_list = "["
    for name, type_ in inputs:
        type_ = astor.to_source(type_).rstrip()
        io_list += f"\"{name}\", m.In({type_}), "
    output_type = astor.to_source(output_type).rstrip()
    io_list += f"\"O\", m.Out({output_type})"
    return io_list + "]"


@ast_utils.inspect_enclosing_env
def sequential(defn_env : dict, cls):
    if not inspect.isclass(cls):
        raise ValueError("sequential decorator only works with classes")

    initial_value_map = get_initial_value_map(cls.__init__)

    call_def = get_ast(cls.__call__).body[0]
    inputs, output_type = get_io(call_def)
    io_list = gen_io_list(inputs, output_type)

    circuit_combinational_output_type = ""
    circuit_combinational_args = ""
    circuit_combinational_call_args = ""
    comb_out_wiring = ""
    for name, type_ in inputs:
        type_ = astor.to_source(type_).rstrip()
        circuit_combinational_args += f"{name}: {type_}, "
        circuit_combinational_call_args += f"io.{name}, "

    comb_out_count = 0
    for name, (value, type_) in initial_value_map.items():
        type_ = astor.to_source(type_).rstrip()
        circuit_combinational_args += f"self_{name}: {type_}, "
        circuit_combinational_call_args += f"{name}, "
        circuit_combinational_output_type += f"{type_}, "
        comb_out_wiring += " " * 8
        comb_out_wiring += f"{name}.I <= comb_out[{comb_out_count}]\n"
        comb_out_count += 1
    circuit_combinational_args = circuit_combinational_args[:-2]
    circuit_combinational_call_args = circuit_combinational_call_args[:-2]
    circuit_combinational_output_type += astor.to_source(output_type).rstrip()
    comb_out_wiring += " " * 8
    comb_out_wiring += f"io.O <= comb_out[{comb_out_count}]\n"

    circuit_combinational_body = ""
    for stmt in call_def.body:
        stmt = RewriteSelfAttributes().visit(stmt)
        stmt = RewriteReturn(initial_value_map).visit(stmt)
        circuit_combinational_body += " " * 12
        circuit_combinational_body += astor.to_source(stmt).rstrip() + "\n"

    circuit_definition_str = circuit_definition_template.format(
        circuit_name=cls.__name__,
        io_list=io_list,
        register_instances=gen_register_instances(initial_value_map),
        circuit_combinational_args=circuit_combinational_args,
        circuit_combinational_output_type=circuit_combinational_output_type,
        circuit_combinational_body=circuit_combinational_body,
        circuit_combinational_call_args=circuit_combinational_call_args,
        comb_out_wiring=comb_out_wiring
    )
    tree = ast.parse(circuit_definition_str)
    if "Register" not in defn_env:
        tree = ast.Module([
            ast.parse("from mantle import Register").body[0],
        ] + tree.body)
    circuit_def = ast_utils.compile_function_to_file(tree, cls.__name__, defn_env)
    circuit_def.debug_info = debug_info(circuit_def.debug_info.filename,
                                        circuit_def.debug_info.lineno,
                                        inspect.getmodule(cls))

    return circuit_def
