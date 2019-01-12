import inspect
import ast
from .util import get_ast
import astor


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
        # We only support basic assignments of the form self.x = m.bits(0, 2)
        assert isinstance(stmt, ast.Assign)
        assert len(stmt.targets) == 1
        assert isinstance(stmt.targets[0], ast.Attribute)
        assert isinstance(stmt.targets[0].value, ast.Name)
        assert stmt.targets[0].value.id == "self"
        print(astor.to_source(stmt))
        # TODO: Should we deal with multiple assignments? For now we take the
        # last one
        initial_value_map[stmt.targets[0].attr] = stmt.value
    return initial_value_map


def get_args(call_func):
    """
    Parses a __call__ method of the form

        def __call__(self, I):
            O = self.y
            self.y = self.x
            self.x = I
            return O

    Returns the list of arguments excluding `self`
    """
    call_def = get_ast(call_func).body[0]
    inputs = []
    # Only support basic args for now
    assert not call_def.args.vararg
    assert not call_def.args.kwonlyargs
    assert not call_def.args.kwarg
    assert not call_def.args.defaults
    assert not call_def.args.kw_defaults

    # Skips self
    assert call_def.args.args[0].arg == "self"
    return [arg.arg for arg in call_def.args.args[1:]]


circuit_definition_template = """
class {circuit_name}(m.Circuit):
    IO = {io_list}

    @classmethod
    def definition(io):
{register_instances}
{circuit_combinational_def}
{circuit_combinational_call}
{output_wiring}
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
    for name, value in initial_value_map.items():
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


def sequential(cls):
    if not inspect.isclass(cls):
        raise ValueError("sequential decorator only works with classes")

    initial_value_map = get_initial_value_map(cls.__init__)

    # TODO: args should include the type
    args = get_args(cls.__call__)

    circuit_definition_str = circuit_definition_template.format(
        circuit_name=cls.__name__,
        io_list="",
        register_instances=gen_register_instances(initial_value_map),
        circuit_combinational_def="",
        circuit_combinational_call="",
        output_wiring=""
    )
    print(circuit_definition_str)
