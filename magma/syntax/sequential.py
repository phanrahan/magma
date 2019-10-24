import re
import inspect
import typing
import ast
from .util import get_ast
import astor
import magma.ast_utils as ast_utils
from magma.debug import debug_info
import functools
import magma as m
from magma.config import get_debug_mode
from collections import Counter
import itertools

from ast_tools.stack import _SKIP_FRAME_DEBUG_STMT
from ast_tools import immutable_ast as iast
import ast_tools


class RewriteSelfAttributes(ast.NodeTransformer):
    def __init__(self, initial_value_map):
        self.initial_value_map = initial_value_map
        self.calls_seen = []

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == "self":
            if isinstance(node.ctx, ast.Store):
                return ast.Name(f"self_{node.attr}_I", ast.Store())
            else:
                return ast.Name(f"self_{node.attr}_O", ast.Load())
        return node

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
                    if isinstance(port, (m.ClockType, m.AsyncResetType)):
                        continue
                    elts.append(ast.Name(f"self_{name}_{port}", ast.Load()))
        if isinstance(node.value, ast.Tuple):
            elts.extend(node.value.elts)
        else:
            elts.append(node.value)
        node.value = ast.Tuple(elts, ast.Load())
        return node


def get_initial_value_map(init_def, defn_env):
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
        eval_type = eval(astor.to_source(stmt.annotation).rstrip(),
                         dict(defn_env.globals, **defn_env.locals))
        eval_value = eval(astor.to_source(stmt.value).rstrip(),
                          dict(defn_env.globals, **defn_env.locals))
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
class {circuit_name}(m.Circuit):
    IO = {io_list}

    @classmethod
    def definition(io):
        {register_instances}
        @ast_tools.passes.end_rewrite()
        @m.circuit.combinational()
        @ast_tools.passes.begin_rewrite()
        def {circuit_name}_comb({circuit_combinational_args}) -> ({circuit_combinational_output_type}):
            {circuit_combinational_body}
        comb_out = {circuit_name}_comb()({circuit_combinational_call_args})
        {comb_out_wiring}
"""


def gen_register_instances(initial_value_map, async_reset):
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
            if isinstance(eval_type, m._BitKind):
                n = None
                if isinstance(eval_value, (bool, int)):
                    init = bool(eval_value)
                else:
                    assert eval_value.name.name in ["GND", "VCC"], eval_value.name
                    init = 0 if eval_value.name.name == "GND" else 1
            else:
                n = len(eval_type)
                init = int(eval_value)
            register_instances.append(f"{name} = DefineRegister({n}, init={init}, has_async_reset={async_reset})()")  # noqa
        else:
            value = astor.to_source(value).rstrip()
            register_instances.append(f"{name} = {value}")
    return register_instances


def gen_io_list(inputs, output_type, async_reset):
    io_list = []
    for name, type_ in inputs:
        type_ = astor.to_source(type_).rstrip()
        io_list.append(f"\"{name}\", m.In({type_})")
    io_list.append(f"\"CLK\", m.In(m.Clock)")
    if async_reset:
        io_list.append(f"\"ASYNCRESET\", m.In(m.AsyncReset)")
    if isinstance(output_type, ast.Tuple):
        outputs = []
        for i, elem in enumerate(output_type.elts):
            output_type_str = astor.to_source(elem).rstrip()
            io_list.append(f"\"O{i}\", m.Out({output_type_str})")
    else:
        output_type_str = astor.to_source(output_type).rstrip()
        io_list.append(f"\"O\", m.Out({output_type_str})")
    return '[' + ', '.join(io_list) + ']'


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
        result = eval(astor.to_source(node.elts[0]).rstrip(),
                      self.defn_env.globals, self.defn_env.locals)
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


def _sequential(tree, env, metadata, async_reset: bool):
    tree = iast.mutable(tree)
    cls__init__ = None
    cls__call__ = None
    for statement in tree.body:
        if isinstance(statement, ast.FunctionDef) and statement.name == "__init__":
            cls__init__ = statement
        if isinstance(statement, ast.FunctionDef) and statement.name == "__call__":
            cls__call__ = statement
    if cls__init__ is None:
        raise Exception("Sequential circuit has no __init__")
    if cls__call__ is None:
        raise Exception("Sequential circuit has no __call__")
    initial_value_map = get_initial_value_map(cls__init__, env)

    inputs, output_type = get_io(cls__call__)
    io_list = gen_io_list(inputs, output_type, async_reset)

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
            circuit_combinational_call_args.append(f"{name}")
            circuit_combinational_output_type.append(f"{type_}")
            comb_out_wiring.append(f"{name}.I <= comb_out[{comb_out_count}]\n")
            comb_out_count += 1
        else:
            for key, value in eval_value.interface.ports.items():
                if isinstance(value, (m.ClockType, m.AsyncResetType)):
                    continue
                type_ = repr(type(value))
                if value.isoutput():
                    circuit_combinational_args.append(f"self_{name}_{value}: m.{type_}")
                    circuit_combinational_call_args.append(f"{name}.{value}")
                if value.isinput():
                    circuit_combinational_output_type.append(f"m.{type_}")
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
        comb_out_wiring.append(f"io.O <= comb_out[{comb_out_count}]\n")

    tab = 4 * ' '
    comb_out_wiring = (2 * tab).join(comb_out_wiring)
    circuit_combinational_output_type = ', '.join(circuit_combinational_output_type)
    circuit_combinational_body = []
    for stmt in cls__call__.body:
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
    register_instances = gen_register_instances(initial_value_map, async_reset)
    register_instances = ('\n' + 2*tab).join(register_instances)

    circuit_definition_str = circuit_definition_template.format(
        circuit_name=tree.name,
        io_list=io_list,
        register_instances=register_instances,
        circuit_combinational_args=circuit_combinational_args,
        circuit_combinational_output_type=circuit_combinational_output_type,
        circuit_combinational_body=circuit_combinational_body,
        circuit_combinational_call_args=circuit_combinational_call_args,
        comb_out_wiring=comb_out_wiring
    )
    tree = ast.parse(circuit_definition_str)
    if "DefineRegister" not in env:
        from mantle import DefineRegister
        env["DefineRegister"] = DefineRegister
    if "m" not in env:
        env["m"] = m
    # FIXME: Hack, insert function/types used by repr of a magma type
    if "Bit" not in env:
        env.globals["Bit"] = m.Bit
    if "In" not in env:
        env.globals["In"] = m.In
    if "Out" not in env:
        env.globals["Out"] = m.Out

    if "ast_tools" not in env:
        import ast_tools
        env["ast_tools"] = ast_tools

    tree = iast.immutable(tree)
    return tree.body[0], env, metadata

class sequential(ast_tools.passes.Pass):
    def __init__(self, async_reset=True):
        self.async_reset = async_reset

    def rewrite(self, tree: ast.AST, env: ast_tools.SymbolTable, metadata: dict):
        return _sequential(tree, env, metadata, self.async_reset)
