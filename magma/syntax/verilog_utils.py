import inspect
import sys
import re
import ast


# The code in this file is adapted from the Silica compiler, shout out to Teguh
# for the help on the original implementation!
# Automatically generate is_{} functions for classes in the ast module
module_obj = sys.modules[__name__]

_first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
_all_cap_re = re.compile(r'([a-z0-9])([A-Z])')


def to_snake_case(name):
    """ Converts name from CamelCase to snake_case

    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    """
    s1 = re.sub(_first_cap_re, r'\1_\2', name)
    return re.sub(_all_cap_re, r'\1_\2', s1).lower()


def is_generator(name):
    def f(node):
        return isinstance(node, getattr(ast, name))

    setattr(module_obj, "is_" + to_snake_case(name), f)


if sys.version_info < (3, 9):
    for x in (m[0] for m in inspect.getmembers(ast, inspect.isclass) if
              m[1].__module__ == '_ast'):
        is_generator(x)
else:
    for x in (m[0] for m in inspect.getmembers(ast, inspect.isclass) if
              m[1].__module__ == 'ast'):
        is_generator(x)


def get_width(node, width_table, defn_env={}):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
       node.func.id in {"bits", "uint", "BitVector"}:
        if isinstance(node.args[1], ast.Call) and \
                node.args[1].func.id == "eval":
            return eval(astor.to_source(node.args[1]).rstrip())
        if not isinstance(node.args[1], ast.Num):
            raise TypeError(f"Cannot get width of "
                            f"{astor.to_source(node.args[1]).rstrip()}, we "
                            f"should know all widths at compile time.")
        return node.args[1].n
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
       node.func.id in {"bit"}:
        return None
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
            node.func.id in {"memory"}:
        return MemoryType(node.args[0].n, node.args[1].n)
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
            node.func.id in {"zext"}:
        assert isinstance(node.args[1], ast.Num), \
            "We should know all widths at compile time"
        return get_width(node.args[0], width_table) + node.args[1].n
    elif isinstance(node, ast.Name):
        if node.id not in width_table:
            raise Exception(f"Trying to get width of variable that hasn't "
                            f"been previously added to the width_table: "
                            f"{node.id} (width_table={width_table})")
        return width_table[node.id]
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            widths = [get_width(arg, width_table) for arg in node.args]
            if node.func.id in {"add", "xor", "sub", "and_", "not_"}:
                if not all(widths[0] == x for x in widths):
                    raise TypeError(f"Calling {node.func.id} with different "
                                    "length types")
                width = widths[0]
                if node.func.id == "add":
                    for keyword in node.keywords:
                        if keyword.arg == "cout" and \
                                isinstance(keyword.value, ast.NameConstant) \
                                and keyword.value.value is True:
                            width = (width, None)
                return width
            elif node.func.id == "eq":
                if not all(widths[0] == x for x in widths):
                    raise TypeError("Calling eq with different length types")
                return None
            elif node.func.id == "decoder":
                return 2 ** get_width(node.args[0], width_table)
            else:
                raise NotImplementedError(ast.dump(node))
        else:
            raise NotImplementedError(ast.dump(node))
    elif isinstance(node, ast.UnaryOp):
        return get_width(node.operand, width_table)
    elif isinstance(node, ast.BinOp):
        left_width = get_width(node.left, width_table)
        right_width = get_width(node.right, width_table)
        if left_width != right_width:
            raise TypeError(f"Binary operation with mismatched widths "
                            f"({left_width}, {right_width}) {ast.dump(node)}")
        return left_width
    elif isinstance(node, ast.IfExp):
        left_width = get_width(node.body, width_table)
        if node.orelse:
            right_width = get_width(node.orelse, width_table)
            if left_width != right_width:
                raise TypeError(f"Binary operation with mismatched widths "
                                f"{ast.dump(node)}")
        return left_width
    elif isinstance(node, ast.Compare):
        # TODO: Check widths of operands
        return None
    elif isinstance(node, ast.NameConstant) and node.value in [True, False]:
        return None
    elif isinstance(node, ast.List):
        widths = [get_width(arg, width_table) for arg in node.elts]
        assert all(widths[0] == width for width in widths)
        return MemoryType(len(node.elts), widths[0])
    elif isinstance(node, ast.Subscript):
        if isinstance(node.slice, ast.Index):
            width = get_width(node.value, width_table)
            if isinstance(width, tuple):
                return width[1]
            elif isinstance(width, MemoryType):
                return width.width
            return None
        elif isinstance(node.slice, ast.Slice):
            width = get_width(node.value, width_table)
            if node.slice.lower is None and isinstance(node.slice.upper,
                                                       ast.Num):
                if node.slice.step is not None:
                    raise NotImplementedError()
                return node.slice.upper.n
            elif node.slice.upper is None:
                lower = 0
                if isinstance(node.slice.lower, ast.Num):
                    lower = node.slice.lower.n
                width = width_table[node.value.id]
                if isinstance(width, MemoryType):
                    return MemoryType(width.height - lower, width.width)
                else:
                    return width - lower
            elif isinstance(node.slice.upper, ast.Num):
                lower = node.slice.lower.n
                upper = node.slice.upper.n
                width = width_table[node.value.id]
                if isinstance(width, MemoryType):
                    return MemoryType(upper - lower - 1, width.width)
                else:
                    return upper - lower - 1
    elif isinstance(node, ast.Num):
        return max(node.n.bit_length(), 1)
    elif isinstance(node, ast.Attribute):
        type_ = width_table[node.value.id]._outputs[node.attr]
        if isinstance(type_, m.BitKind):
            return None
        raise NotImplementedError(type_)

    raise NotImplementedError(ast.dump(node))


class CollectInitialWidthsAndTypes(ast.NodeVisitor):
    def __init__(self, width_table, type_table, defn_env):
        self.width_table = width_table
        self.type_table = type_table
        self.defn_env = defn_env

    def visit_Assign(self, node):
        if len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name):
                if isinstance(node.value, ast.Yield):
                    pass  # width specified at compile time
                elif isinstance(node.value, ast.Call) and \
                        isinstance(node.value.func, ast.Attribute) and \
                        node.value.func.attr == "send":
                    pass
                elif node.targets[0].id not in self.width_table:
                    self.width_table[node.targets[0].id] = \
                        get_width(node.value, self.width_table, self.defn_env)
                    if isinstance(node.value, ast.Call) and \
                            isinstance(node.value.func, ast.Name) and \
                            node.value.func.id in {"bits", "uint", "bit"}:
                        self.type_table[node.targets[0].id] = node.value.func.id
                    elif isinstance(node.value, ast.NameConstant) and \
                            node.value.value in [True, False]:
                        self.type_table[node.targets[0].id] = "bit"
                    elif isinstance(node.value, ast.Name) and \
                            node.value.id in self.type_table:
                        self.type_table[node.targets[0].id] = \
                            self.type_table[node.value.id]


class PromoteWidths(ast.NodeTransformer):
    def __init__(self, width_table, type_table):
        self.width_table = width_table
        self.type_table = type_table

    def check_valid(self, int_length, expected_length):
        if expected_length is None and int_length <= 1:
            return
        if int_length <= expected_length:
            return
        raise TypeError("Cannot promote integer with greater width than other "
                        "operand")

    def make(self, value, width, type_):
        if type_ == "bit":
            return ast.parse(f"{type_}({value})").body[0].value
        else:
            return ast.parse(f"{type_}({value}, {width})").body[0].value

    def get_type(self, node):
        if isinstance(node, ast.Name):
            return self.type_table[node.id]
        elif isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name):
                type_ = self.type_table[node.value.id]
                if type_ == "uint" and isinstance(node.slice, ast.Index):
                    return "bit"
                elif type_ == "uint" and isinstance(node.slice, ast.Slice):
                    if node.slice.lower is None and \
                            isinstance(node.slice.upper, ast.Num):
                        if node.slice.step is not None:
                            raise NotImplementedError()
                        # return node.slice.upper.n
                        return "bits"
                else:
                    raise NotImplementedError(ast.dump(node))
        elif isinstance(node, ast.BinOp):
            left_type = self.get_type(node.left)
            right_type = self.get_type(node.right)
            assert left_type == right_type, (left_type, right_type)
            return left_type
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ["bits"]:
            return node.func.id
        raise NotImplementedError(ast.dump(node))

    def visit_Assign(self, node):
        node.value = self.visit(node.value)
        if isinstance(node.value, ast.Num):
            width = get_width(node.targets[0], self.width_table)
            self.check_valid(node.value.n.bit_length(), width)
            node.value = self.make(node.value.n, width,
                                   self.get_type(node.targets[0]))
        elif isinstance(node.value, ast.NameConstant):
            width = get_width(node.targets[0], self.width_table)
            node.value = ast.parse(f"bit({node.value.value})").body[0].value
        return node

    def visit_AugAssign(self, node):
        node.value = self.visit(node.value)
        if isinstance(node.value, ast.Num):
            width = get_width(node.target, self.width_table)
            self.check_valid(node.value.n.bit_length(), width)
            node.value = self.make(node.value.n, width,
                                   self.get_type(node.target))
        return node

    def visit_BinOp(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        if isinstance(node.left, ast.Num):
            right_width = get_width(node.right, self.width_table)
            try:
                self.check_valid(node.left.n.bit_length(), right_width)
            except TypeError as e:
                print(f"Error type checking node {ast.dump(node)}")
                raise e
            node.left = self.make(node.left.n, right_width,
                                  self.get_type(node.right))
        elif isinstance(node.right, ast.Num):
            left_width = get_width(node.left, self.width_table)
            try:
                self.check_valid(node.right.n.bit_length(), left_width)
            except TypeError as e:
                print(f"Error type checking node {ast.dump(node)}")
                raise e
            node.right = self.make(node.right.n, left_width,
                                   self.get_type(node.left))
        return node

    def visit_Compare(self, node):
        node.left = self.visit(node.left)
        node.comparators = [self.visit(x) for x in node.comparators]
        if not isinstance(node.left, ast.Num):
            left_width = get_width(node.left, self.width_table)
            type_ = self.get_type(node.left)
            for i in range(len(node.comparators)):
                if isinstance(node.comparators[i], ast.Num):
                    self.check_valid(node.comparators[i].n.bit_length(),
                                     left_width)
                    node.comparators[i] = self.make(node.comparators[i].n,
                                                    left_width, type_)
        else:
            for comparator in node.comparators:
                if not isinstance(comparator, ast.Num):
                    width = get_width(comparator, self.width_table)
                    type_ = self.get_type(comparator)
                    break
            else:
                assert False, \
                    "Constant fold should have folded this expression " \
                    f"{ast.dump(node)}"
            self.check_valid(node.left.n.bit_length(), width)
            node.left = self.make(node.left.n, width, type_)
            for i in range(len(node.comparators)):
                if isinstance(node.comparators[i], ast.Num):
                    self.check_valid(node.comparators[i].n.bit_length(), width)
                    node.comparators[i] = self.make(node.comparators[i].n,
                                                    width, type_)
        return node


class RemoveBits(ast.NodeTransformer):
    def visit_Call(self, node):
        if is_attribute(node.func) and \
                is_name(node.func.value) and node.func.value.id == "m" and \
                node.func.attr == "bits":
            return node.args[0]
        return node
