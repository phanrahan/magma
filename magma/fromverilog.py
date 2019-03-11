from __future__ import absolute_import
from __future__ import print_function
from collections import namedtuple

from mako.template import Template
from pyverilog.vparser.parser import VerilogParser, Node, Input, Output, ModuleDef, Ioport, Port, Decl
import pyverilog.vparser.parser as parser
from pyverilog.dataflow.visit import NodeVisitor
import pyverilog.vparser.ast as pyverilog_ast

from .t import In, Out, InOut
from .bit import Bit, _BitKind
from .bits import Bits, BitsKind
from .circuit import DeclareCircuit, DefineCircuit, EndDefine
import logging

logger = logging.getLogger('magma').getChild('from_verilog')


__all__  = ['DeclareFromVerilog']
__all__ += ['DeclareFromVerilogFile']
__all__ += ['DeclareFromTemplatedVerilog']
__all__ += ['DeclareFromTemplatedVerilogFile']
__all__ += ['DefineFromVerilog']
__all__ += ['DefineFromVerilogFile']
__all__ += ['DefineFromTemplatedVerilog']
__all__ += ['DefineFromTemplatedVerilogFile']


class ModuleVisitor(NodeVisitor):
    def __init__(self):
        self.defns = {}
        self.__defn_stack = []
        self.__instances = {}

    def visit_ModuleDef(self, defn):
        if defn.name in self.defns:
            raise Exception(f"Defn with name {defn.name} appears twice")
        self.defns[defn.name] = defn
        # Get ending line number.
        end_lineno = max([item.lineno for item in defn.items])
        end_lineno += 1
        defn.end_lineno = end_lineno
        # Collect instances in this definition.
        self.__instances[defn] = set()
        self.__defn_stack.append(defn)
        self.generic_visit(defn)
        self.__defn_stack.pop()
        return defn

    def visit_Instance(self, instance):
        defn = self.__defn_stack[-1]
        assert instance not in self.__instances[defn]
        self.__instances[defn].add(instance)
        return instance

    def get_instances(self, defn):
        return self.__instances[defn]


def convert(input_type, target_type):
    if isinstance(input_type, _BitKind) and \
       isinstance(target_type, _BitKind) and \
       input_type.direction == target_type.direction:
        return target_type
    if isinstance(input_type, BitsKind) and \
       isinstance(target_type, BitsKind) and \
       input_type.N == target_type.N and \
       input_type.T.direction == target_type.T.direction:
        return target_type
    raise NotImplementedError(f"Conversion between {input_type} and "
                              f"{target_type} not supported")

def get_value(v):
    if isinstance(v, pyverilog_ast.IntConst):
        return int(v.value)
    if isinstance(v, pyverilog_ast.Minus):
        return get_value(v.left) - get_value(v.right)
    else:
        raise NotImplementedError(type(v))

def get_type(io, type_map):
    if isinstance(io, Input):
        direction = In
    elif isinstance(io, Output):
        direction = Out
    else:
        direction = InOut

    if io.width is None:
        type_ = Bit
    else:
        msb = get_value(io.width.msb)
        lsb = get_value(io.width.lsb)
        type_ = Bits[msb-lsb+1]

    type_ = direction(type_)

    if io.name in type_map:
        type_ = convert(type_, type_map[io.name])

    return type_


def ParseVerilogModule(node, type_map):
    args = []
    ports = []
    for port in node.portlist.ports:
        if isinstance(port, Ioport):
            io = port.first
            args.append(io.name)
            args.append(get_type(io, type_map))
        elif isinstance(port, Port):
            ports.append(port.name)
        else:
            raise NotImplementedError(type(port))

    if ports:
        assert not args, "Can we have mixed declared and undeclared types in a Verilog module?"
        for port in ports:
            found = False
            for child in node.children():
                if isinstance(child, Decl):
                    for sub_child in child.children():
                        if isinstance(sub_child, (parser.Input, parser.Output, parser.Inout)) and \
                                sub_child.name == port:
                            args.append(sub_child.name)
                            args.append(get_type(sub_child, type_map))
                            found = True
                            break
                if found:
                    break
            else:
                raise Exception(f"Could not find type declaration for port {port}")

    return node.name, args


def _get_lines(string, start_line, end_line):
    lines = string.split("\n")
    return "\n".join(lines[start_line - 1:end_line])


def FromVerilog(source, func, type_map, target_modules=None):
    if target_modules is not None:
        raise Exception("'target_modules' argument deprecated")
    parser = VerilogParser()
    ast = parser.parse(source)
    visitor = ModuleVisitor()
    visitor.visit(ast)

    magma_defns = {}
    for name, verilog_defn in visitor.defns.items():
        parsed_name, args = ParseVerilogModule(verilog_defn, type_map)
        assert parsed_name == name
        magma_defn = func(name, *args)
        if func == DefineCircuit:
            # Attach relevant lines of verilog source.
            magma_defn.verilogFile = _get_lines(
                source, verilog_defn.lineno, verilog_defn.end_lineno)
            for instance in visitor.get_instances(verilog_defn):
                instance_defn = magma_defns[instance.module]
                instance_defn()
            EndDefine()
        magma_defn.verilog_source = source
        magma_defns[name] = magma_defn

    if len(magma_defns) == 0:
        logger.warning(f"Did not import any modules from verilog, either could "
                       f"not parse or could not find any of the target_modules "
                       f"({target_modules})")
    return list(magma_defns.values())

def FromVerilogFile(file, func, type_map, target_modules=None):
    if file is None:
        return None
    verilog = open(file).read()
    result = FromVerilog(verilog, func, type_map, target_modules)
    # Store the original verilog file name, currently used by m.compile to
    # generate a .sv when compiling a circuit that was defined from a verilog
    # file
    for item in result:
        item.verilog_file_name = file
    return result

def FromTemplatedVerilog(templatedverilog, func, type_map, **kwargs):
    verilog = Template(templatedverilog).render(**kwargs)
    return FromVerilog(verilog, func, type_map)

def FromTemplatedVerilogFile(file, func, type_map, **kwargs):
    if file is None:
        return None
    templatedverilog = open(file).read()
    return FromTemplatedVerilog(templatedverilog, func, type_map, **kwargs)


def DeclareFromVerilog(source, type_map={}):
    return FromVerilog(source, DeclareCircuit, type_map)

def DeclareFromVerilogFile(file, target_modules=None, type_map={}):
    return FromVerilogFile(file, DeclareCircuit, type_map, target_modules)

def DeclareFromTemplatedVerilog(source, type_map={}, **kwargs):
    return FromTemplatedVerilog(source, DeclareCircuit, type_map, **kwargs)

def DeclareFromTemplatedVerilogFile(file, type_map={}, **kwargs):
    return FromTemplatedVerilogFile(file, DeclareCircuit, type_map, **kwargs)


def DefineFromVerilog(source, type_map={}, target_modules=None):
    return FromVerilog(source, DefineCircuit, type_map, target_modules)

def DefineFromVerilogFile(file, target_modules=None, type_map={}):
    return FromVerilogFile(file, DefineCircuit, type_map, target_modules)

def DefineFromTemplatedVerilog(source, type_map={}, **kwargs):
    return FromTemplatedVerilog(source, DefineCircuit, type_map, **kwargs)

def DefineFromTemplatedVerilogFile(file, type_map={}, **kwargs):
    return FromTemplatedVerilogFile(file, DefineCircuit, type_map, **kwargs)
