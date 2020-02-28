import inspect
import typing
import ast
from .util import get_ast
import astor
import magma.ast_utils as ast_utils
from magma.debug import debug_info
import functools
import magma as m
from magma.ssa import convert_tree_to_ssa
from magma.config import get_debug_mode
from collections import Counter
import itertools

from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT, SymbolTable
from ast_tools import gen_free_name

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
                ret.append(ast.parse(
                    f"self_{attr}_{name} = {astor.to_source(value).rstrip()}"
                ).body[0])
            self.calls_seen.extend(ret)
            func = astor.to_source(node.func).rstrip()
            outputs = self.initial_value_map[attr][3].interface.outputs()
            if len(outputs) == 1:
                return ast.Name(f"self_{attr}_{outputs[0]}", ast.Load())
            else:
                assert outputs, "Expected module with at least one output"
                return ast.Tuple([ast.Name(f"self_{attr}_{output}",
                                           ast.Load()) for output in outputs],
                                 ast.Load())
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


    # def visit(self, node):
    #     node = super().visit(node)
    #     if hasattr(node, 'body'):
    #         new_body = self.calls_seen
    #         self.calls_seen = []
    #         for item in node.body:
    #             if isinstance(item, list):
    #                 new_body.extend(item)
    #             else:
    #                 new_body.append(item)
    #         node.body = new_body
    #     return node


class RewriteReturn(ast.NodeTransformer):
    def __init__(self, initial_value_map):
        self.initial_value_map = initial_value_map

    def visit_Return(self, node):
        elts = []
        for name, (value, type_, eval_type, eval_value) in self.initial_value_map.items():
            if isinstance(eval_type, m.Kind):
                elts.append(ast.Name(f"self_{name}_I", ast.Load()))
            else:
                for port in eval_value.interface.inputs():
                    if isinstance(port, (m.Clock, m.AsyncReset)):
                        continue
                    elts.append(ast.Name(f"self_{name}_{port}", ast.Load()))
        if isinstance(node.value, ast.Tuple):
            elts.extend(node.value.elts)
        else:
            elts.append(node.value)
        if len(elts) == 1:
            node.value == 0
        else:
            node.value = ast.Tuple(elts, ast.Load())
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
    init_def = get_ast(init_func).body[0]
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
        m.DefineCircuit("tmp")
        eval_type = eval(astor.to_source(stmt.annotation).rstrip(), defn_env)
        eval_value = eval(astor.to_source(stmt.value).rstrip(), defn_env)
        m.EndCircuit()
        initial_value_map[stmt.target.attr] = (stmt.value, stmt.annotation,
                                               eval_type, eval_value)
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
    # assert not call_def.args.defaults
    assert not call_def.args.kw_defaults

    # Skips self
    assert call_def.args.args[0].arg == "self"
    inputs = [(arg.arg, arg.annotation) for arg in call_def.args.args[1:]]
    returns = call_def.returns
    return inputs, call_def.returns


circuit_definition_template = """
from magma import Bit, Array, Tuple, Product, Bits, SInt, UInt, IO

def make_{circuit_name}(combinational):
    class {circuit_name}({magma_name}.Circuit):
        io = IO({io_args})

        {register_instances}
        @combinational
        def {circuit_name}_comb({circuit_combinational_args}) -> ({circuit_combinational_output_type}):
            {circuit_combinational_body}
        comb_out = {circuit_name}_comb({circuit_combinational_call_args})
        {comb_out_wiring}
    return {circuit_name}
"""


def gen_array_str(eval_type, eval_value, async_reset, magma_name):
    arr = [gen_reg_inst_str(eval_type.T, eval_value[i], async_reset, magma_name) for i
           in range(len(eval_type))]
    return f"{magma_name}.join([{', '.join(arr)}])"


def gen_product_str(eval_type, eval_value, async_reset, magma_name):
    t = [
        f"'{key}':" + gen_reg_inst_str(eval_type[key], eval_value[key], async_reset, magma_name)
        for key in eval_type.keys()
    ]
    return f"{{{', '.join(t)}}}"


def gen_reg_inst_str(eval_type, eval_value, async_reset, magma_name):
    if issubclass(eval_type, m.Digital):
        n = None
        if isinstance(eval_value, (bool, int)):
            init = bool(eval_value)
        else:
            assert eval_value.name.name in ["GND", "VCC"], eval_value.name
            init = 0 if eval_value.name.name == "GND" else 1
    elif issubclass(eval_type, m.Array) and \
            issubclass(eval_type.T, m.Digital):
        n = len(eval_type)
        init = int(eval_value)
    elif issubclass(eval_type, m.Array):
        return f"{gen_array_str(eval_type, eval_value, async_reset, magma_name)}"
    elif issubclass(eval_type, m.Product):
        return f"{gen_product_str(eval_type, eval_value, async_reset, magma_name)}"
    else:
        raise NotImplementedError((eval_type))
    return f"DefineRegister({n}, init={init}, has_async_reset={async_reset})()"


def gen_register_instances(initial_value_map, async_reset, magma_name):
    """
    Generates a sequence of statements to instance a set of registers from
    `initial_value_map`.

    For example,

        initial_value_map = {'x': <_ast.Call object at 0x109c17fd0>,
                             'y': <_ast.Call object at 0x109c17470>}

    will generate

        ['x = Register(2, init=0)', 'y = Register(4, init=0)']

    """
    register_instances = []
    for name, (value, type_, eval_type, eval_value) in initial_value_map.items():
        if isinstance(eval_type, m.Kind):
            reg_inst_str = gen_reg_inst_str(eval_type, eval_value,
                                            async_reset, magma_name)
            register_instances.append(f"{name} = {reg_inst_str}")
        else:
            value = astor.to_source(value).rstrip()
            register_instances.append(f"{name} = {value}")
    return register_instances


def gen_io_args(inputs, output_type, async_reset, magma_name):
    io_args = []
    for name, type_ in inputs:
        type_ = astor.to_source(type_).rstrip()
        io_args.append(f"{name}={magma_name}.In({type_})")
    io_args.append(f"CLK={magma_name}.In({magma_name}.Clock)")
    if async_reset:
        io_args.append(f"ASYNCRESET={magma_name}.In({magma_name}.AsyncReset)")
    if isinstance(output_type, ast.Tuple):
        outputs = []
        for i, elem in enumerate(output_type.elts):
            output_type_str = astor.to_source(elem).rstrip()
            io_args.append(f"O{i}={magma_name}.Out({output_type_str})")
    else:
        output_type_str = astor.to_source(output_type).rstrip()
        io_args.append(f"O={magma_name}.Out({output_type_str})")
    return ', '.join(io_args)


class EscapedExpression(ast.AST):
    def __init__(self, value, orig):
        self.value = value
        self.orig = orig


class ExecuteEscapedPythonExpressions(ast.NodeTransformer):
    def __init__(self, defn_env):
        self.defn_env = defn_env

    def visit_List(self, node):
        assert len(node.elts) == 1, "Expected only list literatals that " \
            "contain a single expression"
        # FIXME: Hack to prevent instancing logic from polluting currently open
        # definition
        m.DefineCircuit("tmp")
        result = eval(astor.to_source(node.elts[0]).rstrip(), self.defn_env)
        m.EndCircuit()
        return EscapedExpression(result, node)


class SpecializeConstantInts(ast.NodeTransformer):
    def __init__(self, defn_env):
        self.defn_env = defn_env

    def visit_Name(self, node):
        if node.id in self.defn_env:
            value = self.defn_env[node.id]
            if isinstance(value, int):
                return ast.Num(value)
        return node


def gen_product_call_args(name, comb_out_count, eval_type, keys, comb_out_wiring, magma_name):
    call_args = []
    for key in eval_type.keys():
        if isinstance(eval_type[key], m.ProductKind):
            call_args.append(
                f"{key}="
                + gen_product_call_args(
                    name, comb_out_count, eval_type[key], keys + [key], comb_out_wiring, magma_name
                )
            )
        else:
            arrays = "".join([f"['{k}']" for k in keys + [key]])
            dots = ".".join(keys + [key])
            comb_out_wiring.append(
                f"{name}{arrays}.I <= comb_out[{comb_out_count}].{dots} \n"
            )
            call_args.append(f"{key}={name}{arrays}.O")
    return f"{magma_name}.namedtuple(" + ", ".join(call_args) + ")"


def _sequential(
        defn_env: dict,
        async_reset: bool,
        cls,
        combinational_decorator: typing.Callable):
    # if not inspect.isclass(cls):
    #     raise ValueError("sequential decorator only works with classes")


    initial_value_map = get_initial_value_map(cls.__init__, defn_env)

    call_def = get_ast(cls.__call__).body[0]
    magma_name = gen_free_name(call_def, defn_env, 'm')
    defn_env[magma_name] = m

    inputs, output_type = get_io(call_def)
    io_args = gen_io_args(inputs, output_type, async_reset, magma_name)

    circuit_combinational_output_type = []
    circuit_combinational_args = []
    circuit_combinational_call_args = []
    comb_out_wiring = []
    for name, type_ in inputs:
        type_ = astor.to_source(type_).rstrip()
        circuit_combinational_args.append(f"{name}: {type_}")
        circuit_combinational_call_args.append(f"io.{name}")

    comb_out_count = 0
    for name, (value, type_, eval_type, eval_value) in initial_value_map.items():
        if isinstance(eval_type, m.Kind):
            type_ = astor.to_source(type_).rstrip()
            circuit_combinational_args.append(f"self_{name}_O: {type_}")
            circuit_combinational_output_type.append(f"{type_}")
            if isinstance(eval_type, m.ProductKind):
                call_args = gen_product_call_args(
                    name, comb_out_count, eval_type, [], comb_out_wiring, magma_name
                )
                circuit_combinational_call_args.append(f"self_{name}_O=" + call_args)
            else:
                circuit_combinational_call_args.append(f"self_{name}_O={name}")
                comb_out_wiring.append(f"{name}.I <= comb_out[{comb_out_count}]\n")
            comb_out_count += 1
        else:
            for key, value in eval_value.interface.ports.items():
                if isinstance(value, (m.Clock, m.AsyncReset)):
                    continue
                type_ = repr(type(value))
                if value.is_output():
                    circuit_combinational_args.append(f"self_{name}_{value}: {magma_name}.{type_}")
                    circuit_combinational_call_args.append(f"{name}.{value}")
                if value.is_input():
                    circuit_combinational_output_type.append(f"{magma_name}.{type_}")
                    comb_out_wiring.append(f"{name}.{value} <= comb_out[{comb_out_count}]\n")
                    comb_out_count += 1

    circuit_combinational_args = ', '.join(circuit_combinational_args)
    circuit_combinational_call_args = ', '.join(circuit_combinational_call_args)

    if isinstance(output_type, ast.Tuple):
        output_types = []
        for i, elem in enumerate(output_type.elts):
            circuit_combinational_output_type.append(astor.to_source(elem).rstrip())
            comb_out_wiring.append(f"io.O{i} <= comb_out[{comb_out_count + i}]\n")
    else:
        output_type_str = astor.to_source(output_type).rstrip()
        circuit_combinational_output_type.append(output_type_str)
        # Handle case when no registers, so only one output
        index_str = ""
        if comb_out_count > 0:
            index_str = f"[{comb_out_count}]"
        comb_out_wiring.append(f"io.O <= comb_out{index_str}\n")

    tab = 4 * ' '
    comb_out_wiring = (2 * tab).join(comb_out_wiring)
    circuit_combinational_output_type = ', '.join(circuit_combinational_output_type)
    circuit_combinational_body = []
    for name, (value, type_, eval_type, eval_value) in initial_value_map.items():
        if isinstance(eval_type, m.Kind):
            circuit_combinational_body.append(
                f"self_{name}_I = self_{name}_O")
    for stmt in call_def.body:
        rewriter = RewriteSelfAttributes(initial_value_map)
        stmt = rewriter.visit(stmt)
        code = [stmt]
        if rewriter.calls_seen:
            code = rewriter.calls_seen + code
        stmt = RewriteReturn(initial_value_map).visit(stmt)
        for stmt in code:
            for line in astor.to_source(stmt).rstrip().splitlines():
                circuit_combinational_body.append(line)

    circuit_combinational_body = ('\n' + 3*tab).join(circuit_combinational_body)
    register_instances = gen_register_instances(initial_value_map, async_reset, magma_name)
    register_instances = ('\n' + 2*tab).join(register_instances)

    circuit_definition_str = circuit_definition_template.format(
        circuit_name=cls.__name__,
        io_args=io_args,
        register_instances=register_instances,
        circuit_combinational_args=circuit_combinational_args,
        circuit_combinational_output_type=circuit_combinational_output_type,
        circuit_combinational_body=circuit_combinational_body,
        circuit_combinational_call_args=circuit_combinational_call_args,
        comb_out_wiring=comb_out_wiring,
        magma_name=magma_name,
    )
    tree = ast.parse(circuit_definition_str)
    if "DefineRegister" not in defn_env:
        tree = ast.Module([
            ast.parse("from mantle import DefineRegister").body[0],
        ] + tree.body)

    circuit_def_constructor = ast_utils.compile_function_to_file(tree, 'make_' + cls.__name__, defn_env)
    circuit_def = circuit_def_constructor(combinational_decorator)

    if get_debug_mode() and getattr(circuit_def, "debug_info", False):
        circuit_def.debug_info = debug_info(circuit_def.debug_info.filename,
                                            circuit_def.debug_info.lineno,
                                            inspect.getmodule(cls))

    return circuit_def

def sequential(
        cls=None,
        async_reset=None,
        *,
        decorators: typing.Optional[typing.Sequence[typing.Callable]] = None,
        env: SymbolTable = None):

    exec(_SKIP_FRAME_DEBUG_STMT)
    if async_reset is not None or decorators is not None:
        assert async_reset is None or isinstance(async_reset, bool)
        assert cls is None
        if decorators is None:
            decorators = ()

        def wrapped(cls):
            exec(_SKIP_FRAME_DEBUG_STMT)
            nonlocal decorators
            decorators = list(itertools.chain(decorators, [wrapped]))
            wrapped_sequential = ast_utils.inspect_enclosing_env(
                    _sequential,
                    decorators=decorators,
                    st=env
            )
            combinational = m.circuit.combinational(decorators=decorators, env=env)
            return wrapped_sequential(async_reset, cls, combinational)
        return wrapped
    else:
        assert cls is not None
        wrapped_sequential = ast_utils.inspect_enclosing_env(
                _sequential,
                decorators=[sequential],
                st=env
        )
        combinational = m.circuit.combinational(decorators=[sequential], env=env)
        return wrapped_sequential(True, cls, combinational)
