from __future__ import absolute_import
from __future__ import print_function
from collections import namedtuple

from mako.template import Template
from pyverilog.vparser.parser import VerilogParser, Node, Input, Output, ModuleDef, Ioport, Port, Decl
import pyverilog.vparser.parser as parser
from pyverilog.dataflow.visit import NodeVisitor

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
        self.nodes = []

    def visit_ModuleDef(self, node):
        self.nodes.append(node)
        return node

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
        msb = int(io.width.msb.value)
        lsb = int(io.width.lsb.value)
        type_ = Bits(msb-lsb+1)

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
            for child in node.children():
                if isinstance(child, Decl):
                    first_child = child.children()[0]
                    if isinstance(first_child, (parser.Input, parser.Output, parser.Inout)) and \
                            first_child.name == port:
                        args.append(first_child.name)
                        args.append(get_type(first_child, type_map))
                        break
            else:
                raise Exception(f"Could not find type declaration for port {port}")

    return node.name, args

def FromVerilog(source, func, type_map, module=None):
    parser = VerilogParser()

    ast = parser.parse(source)
    #ast.show()

    v = ModuleVisitor()
    v.visit(ast)

    if func == DefineCircuit:
        # only allow a single verilog module
        assert len(v.nodes) == 1
    modules = []
    for node in v.nodes:
        if module is not None and node.name != module:
            continue
        try:
            name, args = ParseVerilogModule(node, type_map)
            circuit = func(name, *args)
            if func == DefineCircuit:
                # inline source
                circuit.verilogFile = source
                EndDefine()
            if module is not None:
                assert node.name == module
                return circuit
            modules.append(circuit)
        except Exception as e:
            logger.warning(f"Could not parse module {node.name} ({e}), "
                           f"skipping")
    if module is not None:
        raise Exception(f"Could not find module {module}")

    return modules

def FromVerilogFile(file, func, type_map, module=None):
    if file is None:
        return None
    verilog = open(file).read()
    return FromVerilog(verilog, func, type_map, module)

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

def DeclareFromVerilogFile(file, module=None, type_map={}):
    return FromVerilogFile(file, DeclareCircuit, type_map, module)

def DeclareFromTemplatedVerilog(source, type_map={}, **kwargs):
    return FromTemplatedVerilog(source, DeclareCircuit, type_map, **kwargs)

def DeclareFromTemplatedVerilogFile(file, type_map={}, **kwargs):
    return FromTemplatedVerilogFile(file, DeclareCircuit, type_map, **kwargs)


def DefineFromVerilog(source, type_map={}):
    return FromVerilog(source, DefineCircuit, type_map)

def DefineFromVerilogFile(file, module=None, type_map={}):
    return FromVerilogFile(file, DefineCircuit, type_map, module)

def DefineFromTemplatedVerilog(source, type_map={}, **kwargs):
    return FromTemplatedVerilog(source, DefineCircuit, type_map, **kwargs)

def DefineFromTemplatedVerilogFile(file, type_map={}, **kwargs):
    return FromTemplatedVerilogFile(file, DefineCircuit, type_map, **kwargs)

