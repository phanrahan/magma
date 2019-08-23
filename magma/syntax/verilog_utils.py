import inspect
import sys
import re
import veriloggen as vg
import ast


# The code in this file is adapted from the Silica compiler, shout out to Teguh
# for the help on the original implementation!
# Automatically generate is_{} functions for classes in the ast module
module_obj = sys.modules[__name__]

_first_cap_re=re.compile(r'(.)([A-Z][a-z]+)')
_all_cap_re=re.compile(r'([a-z0-9])([A-Z])')
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


for x in (m[0] for m in inspect.getmembers(ast, inspect.isclass) if m[1].__module__ == '_ast'):
    is_generator(x)


class Context:
    def __init__(self, name, sub_coroutines=[]):
        self.module = vg.Module(name)
        self.sub_coroutines = sub_coroutines

    def declare_ports(self, inputs, outputs):
        if outputs:
            for o,n in outputs.items():
                if n > 1:
                    self.module.Output(o, n)
                else:
                    self.module.Output(o)
        if inputs:
            for i,n in inputs.items():
                if n > 1:
                    self.module.Input(i, n)
                else:
                    self.module.Input(i)

    def declare_wire(self, name, width=None, height=None):
        self.module.Wire(name, width, height)

    def declare_reg(self, name, width=None, height=None):
        self.module.Reg(name, width, height)

    def assign(self, lhs, rhs):
        # return vg.Subst(lhs, rhs, not self.is_reg(lhs))
        return vg.Subst(lhs, rhs, 1)

    def initial(self, body=[]):
        return self.module.Initial(body)

    def get_by_name(self, name):
        if name in self.module.get_vars():
            return self.module.get_vars()[name]
        elif name in self.module.get_ports():
            return self.module.get_ports()[name]

        raise KeyError(f"`{name}` is not a valid port or variable.")

    def is_reg(self, obj):
        return isinstance(obj, vg.core.vtypes.Reg)

    def translate_assign(self, target, value, blk=1):
        return vg.Subst(
            self.translate(target),
            value,
            blk
        )


    # TODO: should reorder the switch into more sensible ordering
    # TODO: should split this up into a few translate functions that translate certain classes of inputs
    def translate(self, stmt):
        if isinstance(stmt, bool):
            return vg.Int(1 if stmt else 0)
        elif is_add(stmt):
            return vg.Add
        elif is_mult(stmt):
            return vg.Mul
        elif is_or(stmt):
            return vg.Or
        elif is_r_shift(stmt):
            return vg.Srl
        elif is_l_shift(stmt):
            return vg.Sll
        elif is_bool_op(stmt):
            result = self.translate(stmt.op)(
                self.translate(stmt.values[0]),
                self.translate(stmt.values[1])
            )
            for value in stmt.values[2:]:
                result = self.translate(stmt.op)(result, self.translate(value))
            return result
        elif is_bin_op(stmt):
            if is_list(stmt.left) or is_list(stmt.right):
                if is_add(stmt.op): # list concatenation
                    return vg.Cat(
                        self.translate(stmt.left),
                        self.translate(stmt.right)
                    )
                elif is_mult(stmt.op): # list replication
                    var = self.translate(stmt.left) if is_list(stmt.left) else self.translate(stmt.right)
                    times = self.translate(stmt.right) if is_list(stmt.left) else self.translate(stmt.left)
                    return vg.Repeat(var, times)

            return self.translate(stmt.op)(
                self.translate(stmt.left),
                self.translate(stmt.right)
            )
        elif is_bit_and(stmt):
            return vg.And
        elif is_bit_xor(stmt):
            return vg.Xor
        elif is_bit_or(stmt):
            return vg.Or
        elif is_compare(stmt):
            curr = self.translate(stmt.ops[0])(
                self.translate(stmt.left),
                self.translate(stmt.comparators[0])
            )
            for op, comp in zip(stmt.ops[1:], stmt.comparators[1:]):
                curr = self.translate(op)(curr, self.translate(comp))
            return curr
        elif is_eq(stmt):
            return vg.Eq
        elif is_if(stmt):
            body = [self.translate(stmt) for stmt in stmt.body]
            if_ = vg.If(
                self.translate(stmt.test),
            )(body)
            if stmt.orelse:
                if_.Else(
                    [self.translate(stmt) for stmt in stmt.orelse]
                )
            return if_
        elif is_if_exp(stmt):
            return vg.Cond(
                self.translate(stmt.test),
                self.translate(stmt.body),
                self.translate(stmt.orelse)
            )
        elif is_invert(stmt):
            return vg.Unot
        elif is_list(stmt):
            return vg.Cat(*[self.translate(elt) for elt in stmt.elts])
        elif is_lt(stmt):
            return vg.LessThan
        elif is_gt(stmt):
            return vg.GreaterThan
        elif is_gt_e(stmt):
            return vg.GreaterEq
        elif is_name(stmt):
            return self.get_by_name(stmt.id)
        elif is_name_constant(stmt):
            # TODO: distinguish between int, bool, etc.
            return self.translate(stmt.value)
        elif is_not_eq(stmt):
            return vg.NotEq
        elif is_num(stmt):
            return vg.Int(stmt.n)
        elif is_sub(stmt):
            return vg.Sub
        elif is_subscript(stmt):
            if is_index(stmt.slice):
                return vg.Pointer(
                    self.translate(stmt.value),
                    self.translate(stmt.slice.value)
                )
            elif is_slice(stmt.slice):
                return vg.Slice(
                    self.translate(stmt.value),
                    self.translate(stmt.slice.lower),
                    self.translate(stmt.slice.upper)
                )
        elif is_tuple(stmt):
            return vg.Cat(*[self.translate(elt) for elt in stmt.elts])
        elif is_unary_op(stmt):
            return self.translate(stmt.op)(self.translate(stmt.operand))
        elif is_assign(stmt):
            # blk = not self.is_reg(target)
            return self.translate_assign(stmt.targets[0], self.translate(stmt.value))
        elif isinstance(stmt, ast.Expr) and is_call(stmt.value) and is_name(stmt.value.func) and stmt.value.func.id == "print":
            # Skip print statements for now, maybe translate to display?
            return
        elif is_call(stmt) and is_attribute(stmt.func) and \
                is_name(stmt.func.value) and stmt.func.value.id == "m" and \
                stmt.func.attr == "bits":
            return self.translate(stmt.args[0])
        elif is_pass(stmt):
            return
        raise NotImplementedError(ast.dump(stmt))

    def to_verilog(self):
        return self.module.to_verilog()


class SwapSlices(ast.NodeTransformer):
    def visit_Subscript(self, node):
        node.slice = self.visit(node.slice)
        if isinstance(node.slice, ast.Slice):
            if node.slice.lower is None and isinstance(node.slice.upper, ast.Num):
                if node.slice.step is not None:
                    raise NotImplementedError()
                node.slice.lower = ast.Num(node.slice.upper.n - 1)
                node.slice.upper = ast.Num(0)
        return node


def get_width(node, width_table, defn_env={}):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
       node.func.id in {"bits", "uint", "BitVector"}:
        if isinstance(node.args[1], ast.Call) and node.args[1].func.id == "eval":
            return eval(astor.to_source(node.args[1]).rstrip())
        if not isinstance(node.args[1], ast.Num):
            raise TypeError(f"Cannot get width of {astor.to_source(node.args[1]).rstrip()}, we should know all widths at compile time.")
        return node.args[1].n
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
       node.func.id in {"bit"}:
        return None
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
       node.func.id in {"memory"}:
           return MemoryType(node.args[0].n, node.args[1].n)
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
       node.func.id in {"zext"}:
        assert isinstance(node.args[1], ast.Num), "We should know all widths at compile time"
        return get_width(node.args[0], width_table) + node.args[1].n
    elif isinstance(node, ast.Name):
        if node.id not in width_table:
            raise Exception(f"Trying to get width of variable that hasn't been previously added to the width_table: {node.id} (width_table={width_table})")
        return width_table[node.id]
    elif is_call(node) and is_name(node.func) and node.func.id == "coroutine_create":
        return eval(astor.to_source(node.args[0]), defn_env)()
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            widths = [get_width(arg, width_table) for arg in node.args]
            if node.func.id in {"add", "xor", "sub", "and_", "not_"}:
                if not all(widths[0] == x for x in widths):
                    raise TypeError(f"Calling {node.func.id} with different length types")
                width = widths[0]
                if node.func.id == "add":
                    for keyword in node.keywords:
                        if keyword.arg == "cout" and isinstance(keyword.value, ast.NameConstant) and keyword.value.value == True:
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
            raise TypeError(f"Binary operation with mismatched widths ({left_width}, {right_width}) {ast.dump(node)}")
        return left_width
    elif isinstance(node, ast.IfExp):
        left_width = get_width(node.body, width_table)
        if node.orelse:
            right_width = get_width(node.orelse, width_table)
            if left_width != right_width:
                raise TypeError(f"Binary operation with mismatched widths {ast.dump(node)}")
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
            if node.slice.lower is None and isinstance(node.slice.upper, ast.Num):
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
                elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and \
                     node.value.func.attr == "send":
                    pass
                elif node.targets[0].id not in self.width_table:
                    self.width_table[node.targets[0].id] = get_width(node.value, self.width_table, self.defn_env)
                    if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and \
                       node.value.func.id in {"bits", "uint", "bit"}:
                        self.type_table[node.targets[0].id] = node.value.func.id
                    elif isinstance(node.value, ast.NameConstant) and node.value.value in [True, False]:
                        self.type_table[node.targets[0].id] = "bit"
                    elif isinstance(node.value, ast.Name) and node.value.id in self.type_table:
                        self.type_table[node.targets[0].id] = self.type_table[node.value.id]



class PromoteWidths(ast.NodeTransformer):
    def __init__(self, width_table, type_table):
        self.width_table = width_table
        self.type_table = type_table

    def check_valid(self, int_length, expected_length):
        if expected_length is None and int_length <= 1:
            return
        if int_length <= expected_length:
            return
        raise TypeError("Cannot promote integer with greater width than other operand")

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
                    if node.slice.lower is None and isinstance(node.slice.upper, ast.Num):
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
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ["bits"]:
            return node.func.id
        raise NotImplementedError(ast.dump(node))

    def visit_Assign(self, node):
        node.value = self.visit(node.value)
        if isinstance(node.value, ast.Num):
            width = get_width(node.targets[0], self.width_table)
            self.check_valid(node.value.n.bit_length(), width)
            node.value = self.make(node.value.n, width, self.get_type(node.targets[0]))
        elif isinstance(node.value, ast.NameConstant):
            width = get_width(node.targets[0], self.width_table)
            node.value = ast.parse(f"bit({node.value.value})").body[0].value
        return node

    def visit_AugAssign(self, node):
        node.value = self.visit(node.value)
        if isinstance(node.value, ast.Num):
            width = get_width(node.target, self.width_table)
            self.check_valid(node.value.n.bit_length(), width)
            node.value = self.make(node.value.n, width, self.get_type(node.target))
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
            node.left = self.make(node.left.n, right_width, self.get_type(node.right))
        elif isinstance(node.right, ast.Num):
            left_width = get_width(node.left, self.width_table)
            try:
                self.check_valid(node.right.n.bit_length(), left_width)
            except TypeError as e:
                print(f"Error type checking node {ast.dump(node)}")
                raise e
            node.right = self.make(node.right.n, left_width, self.get_type(node.left))
        return node

    def visit_Compare(self, node):
        node.left = self.visit(node.left)
        node.comparators = [self.visit(x) for x in node.comparators]
        if not isinstance(node.left, ast.Num):
            left_width = get_width(node.left, self.width_table)
            type_ = self.get_type(node.left)
            for i in range(len(node.comparators)):
                if isinstance(node.comparators[i], ast.Num):
                    self.check_valid(node.comparators[i].n.bit_length(), left_width)
                    node.comparators[i] = self.make(node.comparators[i].n, left_width, type_)
        else:
            for comparator in node.comparators:
                if not isinstance(comparator, ast.Num):
                    width = get_width(comparator, self.width_table)
                    type_ = self.get_type(comparator)
                    break
            else:
                assert False, "Constant fold should have folded this expression {ast.dump(node)}"
            self.check_valid(node.left.n.bit_length(), width)
            node.left = self.make(node.left.n, width, type_)
            for i in range(len(node.comparators)):
                if isinstance(node.comparators[i], ast.Num):
                    self.check_valid(node.comparators[i].n.bit_length(), width)
                    node.comparators[i] = self.make(node.comparators[i].n, width, type_)
        return node

