from __future__ import absolute_import
from __future__ import print_function
from collections import namedtuple
#from functools import lru_cache

from mako.template import Template
from pyverilog.vparser.parser import VerilogParser, Node, Input, Output, ModuleDef
from pyverilog.dataflow.visit import NodeVisitor

from .t import In, Out
from .bit import Bit
from .array import Array
from .circuit import DeclareCircuit, DefineCircuit, EndCircuit

__all__  = ['DeclareFromVerilog']
__all__ += ['DeclareFromVerilogFile']
#__all__ += ['DefineFromVerilog']
#__all__ += ['DefineFromVerilogFile']
#__all__ += ['DefineFromTemplatedVerilog']
#__all__ += ['DefineFromTemplatedVerilogFile']


class ModuleVisitor(NodeVisitor):
    def __init__(self):
        self.nodes = []

    def visit_ModuleDef(self, node):
        self.nodes.append(node)
        return node

def ParseVerilogModule(node):
    args = []
    for port in node.portlist.ports:
        io = port.first
        args.append(io.name)
        msb = int(io.width.msb.value)
        lsb = int(io.width.lsb.value)
        if   isinstance(io, Input):  dir = 'In'
        elif isinstance(io, Output): dir = 'Out'
        else: continue
        if msb == 0 and lsb == 0:
            t = Bit
        else:
            t = Array(msb-lsb+1, Bit)
        args.append( In(t) if dir == 'In' else Out(t) )

    return node.name, args

def FromVerilog(source, func):
    parser = VerilogParser()

    ast = parser.parse(source)
    ast.show()

    v = ModuleVisitor()
    v.visit(ast)

    modules = []
    for node in v.nodes:
         name, args = ParseVerilogModule(node)
         print(name, args)
         modules.append(func(name, *args))
    return modules

def FromVerilogFile(file, func):
    if file is None:
        return None
    source = open(file).read()
    return FromVerilog(source, func)


#@lru_cache(maxsize=32)
def DeclareVerilogModule(module):
    name, args = ParseVerilogModule(module)
    return DeclareCircuit(name, *args)

def DeclareFromVerilog(source):
    return FromVerilog(source, DeclareVerilogModule)

def DeclareFromVerilogFile(file):
    return FromVerilogFile(file, DeclareVerilogModule)


#@lru_cache(maxsize=32)
def DefineVerilogModule(module):
    name, args = ParseVerilogModule(module)
    return DefineCircuit(name, *args)

def DefineFromVerilog(source):
    return FromVerilog(source, DefineVerilogModule)

def DefineFromVerilogFile(file):
    return FromVerilogFile(source, DefineVerilogModule)


def DefineFromTemplatedVerilogFile(file, **kwargs):
    if file is None:
        return None

    source = open(file).read()

    verilog = Template(source).render(**kwargs)

    return DefineFromVerilog(verilog)

