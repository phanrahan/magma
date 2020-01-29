from collections import OrderedDict
from hwtypes import UIntVector, SIntVector
from pyverilog.vparser.parser import VerilogParser, Node, Input, Output, ModuleDef, Ioport, Port, Decl
import pyverilog.vparser.parser as parser
from pyverilog.dataflow.visit import NodeVisitor
import pyverilog.vparser.ast as pyverilog_ast
from ..array import Array
from ..digital import Digital
from ..bit import Bit
from ..bits import Bits
from ..math import log2_ceil
from ..passes.tsort import tsort
from ..t import In, Out, InOut


def parse_int_const(value):
    if "'" in value:
        # Parse literal specifier
        size, value = value.split("'")
        if size == "":
            size = 32
        else:
            size = int(size)
        if "s" in value:
            signed = True
            value = value.replace("s", "")
        else:
            signed = False
        for specifier, base in [("h", 16), ("o", 8), ("b", 2), ("d", 10)]:
            if specifier in value:
                # Remove specifier
                value = value.replace(specifier, "")
                break
        else:
            # default base 10
            base = 10
    else:
        # Default no specifier
        size = 32
        base = 10
        signed = False
    value = int(value, base)
    if signed:
        value = SIntVector[size](value).as_uint()
    else:
        value = UIntVector[size](value).as_uint()
    return value


class ModuleVisitor(NodeVisitor):
    def __init__(self, shallow):
        self.__shallow = shallow
        self.defns = OrderedDict()
        self.__defn_stack = []
        self.__instances = {}

    def visit_ModuleDef(self, defn):
        if defn.name in self.defns:
            raise Exception(f"Defn with name {defn.name} appears twice")
        self.defns[defn.name] = defn
        if self.__shallow:
            return defn
        # Collect instances in this definition.
        self.__instances[defn] = set()
        self.__defn_stack.append(defn)
        self.generic_visit(defn)
        self.__defn_stack.pop()
        return defn

    def visit_Instance(self, instance):
        if self.__shallow:
            return instance
        defn = self.__defn_stack[-1]
        assert instance not in self.__instances[defn]
        self.__instances[defn].add(instance)
        return instance

    def get_instances(self, defn):
        return self.__instances[defn]

    def sort(self):
        graph = []
        for defn in self.defns.values():
            insts = [inst.module for inst in self.get_instances(defn)]
            graph.append((defn.name, insts))
        sorted_ = tsort(graph)
        defns = OrderedDict()
        for defn_name, _ in sorted_:
            defns[defn_name] = self.defns[defn_name]
        self.defns = defns


def get_value(v, param_map):
    if isinstance(v, pyverilog_ast.IntConst):
        return parse_int_const(v.value)
    if isinstance(v, pyverilog_ast.Rvalue):
        return get_value(v.var, param_map)
    if isinstance(v, (pyverilog_ast.Minus, pyverilog_ast.Uminus)):
        return get_value(v.left, param_map) - get_value(v.right, param_map)
    if isinstance(v, pyverilog_ast.Plus):
        return get_value(v.left, param_map) + get_value(v.right, param_map)
    if isinstance(v, pyverilog_ast.Divide):
        l = get_value(v.left, param_map)
        r = get_value(v.right, param_map)
        # NOTE(rsetaluri): Assume integer division.
        return int(l / r)
    if isinstance(v, pyverilog_ast.Identifier):
        return param_map[v.name]
    if isinstance(v, pyverilog_ast.SystemCall):
        syscall = v.syscall
        if syscall == "clog2":
            return log2_ceil(get_value(v.children()[0], param_map))
        raise NotImplementedError(f"Verilog system call {syscall}")
    raise NotImplementedError(type(v))


def get_width(width, param_map):
    msb = get_value(width.msb, param_map)
    lsb = get_value(width.lsb, param_map)
    return msb - lsb + 1


def convert(input_type, target_type):
    if issubclass(input_type, Digital) and \
       issubclass(target_type, Digital) and \
       input_type.direction == target_type.direction:
        return target_type
    if issubclass(input_type, Bits) and \
       issubclass(target_type, Bits) and \
       input_type.N == target_type.N and \
       input_type.T.direction == target_type.T.direction:
        return target_type
    raise NotImplementedError(f"Conversion between {input_type} and "
                              f"{target_type} not supported")


def get_type(io, type_map, param_map):
    if isinstance(io, Input):
        direction = In
    elif isinstance(io, Output):
        direction = Out
    else:
        direction = InOut

    if io.width is None:
        typ = Bit
    else:
        width = get_width(io.width, param_map)
        typ = Bits[width]

    # Generate multidimensional arrays if necessary. Note that we guard with
    # hasattr to make this backwards compatible.
    if hasattr(io, "dimensions") and io.dimensions is not None:
        for length in reversed(io.dimensions.lengths):
            width = get_width(length, param_map)
            typ = Array[width, typ]

    typ = direction(typ)

    if io.name in type_map:
        typ = convert(typ, type_map[io.name])

    return typ


