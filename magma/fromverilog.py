from __future__ import absolute_import
from __future__ import print_function
from collections import namedtuple

from mako.template import Template
from pyverilog.vparser.parser import VerilogParser, Node, Input, Output, ModuleDef, Ioport, Port, Decl
from pyverilog.dataflow.visit import NodeVisitor

from .t import In, Out, InOut
from .bit import Bit
from .array import Array
from .circuit import DeclareCircuit, DefineCircuit, EndDefine

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

def get_type(io):
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

        type_ = Array(msb-lsb+1, Bit)
    return direction(type_)


def ParseVerilogModule(node):
    args = []
    ports = []
    for port in node.portlist.ports:
        if isinstance(port, Ioport):
            io = port.first
            args.append(io.name)
            args.append(get_type(io))
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
                    if isinstance(first_child, (Input, Output)) and first_child.name == port:
                        args.append(first_child.name)
                        args.append(get_type(first_child))
                        break
            else:
                raise Exception(f"Could not find type declaration for port {port}")

    return node.name, args

def FromVerilog(source, func):
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
         name, args = ParseVerilogModule(node)
         circuit = func(name, *args)
         if func == DefineCircuit:
             # inline source
             circuit.verilogFile = source
         EndDefine()
         modules.append(circuit)
    return modules

def FromVerilogFile(file, func):
    if file is None:
        return None
    verilog = open(file).read()
    return FromVerilog(verilog, func)

def FromTemplatedVerilog(templatedverilog, func, **kwargs):
    verilog = Template(templatedverilog).render(**kwargs)
    return FromVerilog(verilog, func)

def FromTemplatedVerilogFile(file, func, **kwargs):
    if file is None:
        return None
    templatedverilog = open(file).read()
    return FromTemplatedVerilog(templatedverilog, func, **kwargs)


def DeclareFromVerilog(source):
    return FromVerilog(source, DeclareCircuit)

def DeclareFromVerilogFile(file):
    return FromVerilogFile(file, DeclareCircuit)

def DeclareFromTemplatedVerilog(source, **kwargs):
    return FromTemplatedVerilog(source, DeclareCircuit, **kwargs)

def DeclareFromTemplatedVerilogFile(file, **kwargs):
    return FromTemplatedVerilogFile(file, DeclareCircuit, **kwargs)


def DefineFromVerilog(source):
    return FromVerilog(source, DefineCircuit)

def DefineFromVerilogFile(file):
    return FromVerilogFile(file, DefineCircuit)

def DefineFromTemplatedVerilog(source, **kwargs):
    return FromTemplatedVerilog(source, DefineCircuit, **kwargs)

def DefineFromTemplatedVerilogFile(file, **kwargs):
    return FromTemplatedVerilogFile(file, DefineCircuit, **kwargs)

