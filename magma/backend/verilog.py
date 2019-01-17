import os
import types
import operator
from functools import reduce
from collections import OrderedDict, Sequence
from ..port import INPUT, OUTPUT, INOUT, flip
from ..ref import DefnRef
from ..compatibility import IntegerTypes
from ..bit import _BitType, _BitKind, VCC, GND
from ..clock import ClockType, EnableType, ResetType
from ..array import ArrayKind, ArrayType
from ..bits import SIntType
from ..tuple import TupleType
from ..is_definition import isdefinition
from ..clock import wiredefaultclock
import logging
import os

logger = logging.getLogger('magma').getChild('verilog_backend')
level = os.getenv("MAGMA_VERILOG_BACKEND_LOG_LEVEL", "WARN")
# TODO: Factor this with magma.logging code for debug level validation
if level in ["DEBUG", "WARN", "INFO"]:
    logger.setLevel(getattr(logging, level))
elif level is not None:
    logging.warning("Unsupported value for MAGMA_VERILOG_BACKEND_LOG_LEVEL:"
                    f" {level}")

from .util import get_codegen_debug_info, make_relative

#__all__  = ['hstr', 'bstr']
__all__  = ['hstr']

# return the hex character for int n
def hex(n):
    if n < 10: return chr(ord('0')+n)
    else:      return chr(ord('A')+n-10)

# return a hex string reprenting n
def hstr(n, bits):
    format = "%d'h" % bits
    nformat = []
    n &= (1 << bits)-1
    for i in range((bits+3)//4):
        nformat.append(n%16)
        n //= 16
    nformat.reverse()
    return format + reduce(operator.add, map(hex, nformat))

def bstr(n, bits):
    if bits == 1:
        return "1'b1" if init else "1'b0"
    format = "%d'b" % bits
    nformat = []
    n &= (1 << bits)-1
    for i in range(bits):
        nformat.append(n%2)
        n //= 2
    nformat.reverse()
    return format + reduce(operator.add, map(hex, nformat))

# return the verilog name of a data value
def vname(t):
    if t is VCC: return "1'b1"
    if t is GND: return "1'b0"

    if isinstance(t, ArrayType):
        # print(t.ts)
        if not t.iswhole(t.ts):
            # the sequence of values is concantenated
            t = [vname(i) for i in t.ts]
            t.reverse()
            return '{' + ','.join(t) + '}'

    assert not t.anon(), (t.name)
    return t.name.qualifiedname(sep='_')

# return the verilog declaration for the data type
def vdecl(t):
    if isinstance(t, ArrayType):
        signed = "signed " if isinstance(t, SIntType) else ""
        return '{}[{}:{}]'.format(signed, t.N-1, 0)
    else:
        assert isinstance(t, _BitType)
        return ""

# return the verilog module args
def vmoduleargs(self):
    def append(args, port, name):
        if   port.isinput():  d = OUTPUT
        elif port.isoutput(): d = INPUT
        else: d = INOUT
        args.append("%s %s %s" % (d, vdecl(port), name))

    args = []
    for name, port in self.ports.items():
        if isinstance(port, TupleType):
            for i in range(len(port)):
                append(args, port[i], vname(port[i]))
        else:
            #d = flip(port.direction)
            append(args, port, name)
    return args


def compileinstance(self):

    # print('compileinstance', str(self), str(type(self)))

    def arg(k,v):
        if not isinstance(v, str): v = str(v)
        return '.%s(%s)' % (k, v)

    args = []
    debug_str = ""
    for k, v in self.interface.ports.items():
        if hasattr(v, "debug_info") and get_codegen_debug_info():
            filename, lineno, module = v.debug_info
        #print('arg', k, v,)
        if v.isinput():
            # find the output connected to v
            w = v.value()
            if not w:
                logging.warning(f'{v.debug_name} not connected')
                continue
            v = w
        if isinstance(v, TupleType):
            for i in range(len(v)):
                args.append(arg('%s_%s' %
                    (v[i].name.tuple.name, v[i].name.index), vname(v[i])))
        elif isinstance(k, IntegerTypes):
            args.append( vname(v) )
        else:
            args.append( arg(k,vname(v)) )
        if hasattr(v, "debug_info") and get_codegen_debug_info():
            debug_str += f"// Argument {k}({vname(v)}) wired at {make_relative(filename)}:{lineno}\n"

    params = []
    for k, v in self.kwargs.items():
       if k not in {'loc', 'name', 'T'}:
           if isinstance(v, tuple):
               v = hstr(v[0], v[1])
           params.append(arg(k, v))
    params = sorted(params)

    #s = '(* loc="%d,%d/%d" *)\n' % self.loc if self.loc else ""

    s = str(self.__class__.verilog_name)
    if len(params):
        if len(params) > 2:
            s += ' #(' + ",\n".join(params) + ')'
        else:
            s += ' #(' + ", ".join(params) + ')'
    s += ' ' + str(self.name)

    return debug_str + '%s (%s)' % (s, ', '.join(args))

def compiledefinition(cls):

    # for now only allow Bit or Array(n, Bit)
    for name, port in cls.interface.ports.items():
        if isinstance(port, (ArrayKind, ArrayType)):
            if not isinstance(port.T, (_BitType, _BitKind)):
                raise Exception(f'Argument {cls.__name__}.{name} of type {type(port)} is not supported, the verilog backend only supports simple 1-d array of bits of the form Array(N, Bit)')


    if cls.verilogFile:
       s = cls.verilogFile
    else:
        args = ', '.join(vmoduleargs(cls.interface))
        s = ''
        if get_codegen_debug_info() and cls.debug_info.filename and cls.debug_info.lineno:
            s += f'// Defined at {make_relative(cls.debug_info.filename)}:{cls.debug_info.lineno}\n'
        s += 'module %s (%s);\n' % (cls.verilog_name, args)
        if cls.verilog:
            s += cls.verilog + '\n'
            if cls.verilogLib:
                import re
                for libName in cls.verilogLib:
                    if re.search("\.v$",libName):
                        with open(libName,'r') as libFile:
                            s = libFile.read() + s
                    else:
                        s = libName + s
        else:
            def wire(port):
                return 'wire %s %s;\n' % (vdecl(port), vname(port))

            # declare a wire for each instance output
            for instance in cls.instances:
                for port in instance.interface.ports.values():
                    if isinstance(port, TupleType):
                        for i in range(len(port)):
                            s += wire(port[i])
                    else:
                        if not port.isinput():
                            s += wire(port)

            #print('compile instances')
            # emit the structured verilog for each instance
            for instance in cls.instances:
                wiredefaultclock(cls, instance)
                if instance.debug_info.filename and instance.debug_info.lineno and get_codegen_debug_info():
                    s += f"// Instanced at {make_relative(instance.debug_info.filename)}:{instance.debug_info.lineno}\n"
                s += compileinstance(instance) + ";\n"

            # assign to module output arguments
            for port in cls.interface.ports.values():
                if port.isinput():
                    output = port.value()
                    if output:
                        if isinstance(output, TupleType):
                            for name, input in cls.interface.ports.items():
                                if input.isinput():
                                    output = input.value()
                                    assert isinstance(output, TupleType)
                                    for i in range(len(input)):
                                        iname = vname(input[i])
                                        oname = vname(output[i])
                                        s += 'assign %s = %s;\n' % (iname, oname)
                        else:
                            iname = vname(port)
                            oname = vname(output)
                            if hasattr(port, "debug_info") and get_codegen_debug_info():
                                s += f"// Wired at {make_relative(port.debug_info[0])}:{port.debug_info[1]}\n"
                            s += 'assign %s = %s;\n' % (iname, oname)
                    else:
                        logging.warning(f"{cls.__name__}.{port.name} is unwired")

        s += "endmodule\n"

    return s

def find(circuit, defn):
    if not isdefinition(circuit):
        return defn
    for i in circuit.instances:
        find(type(i), defn)
    name = circuit.verilog_name
    if name not in defn:
        defn[name] = circuit
    return defn


def compile(main):
    defn = find(main,OrderedDict())

    code = ''

    for k, v in defn.items():
         logging.debug(f'compiling circuit {k}')
         code += compiledefinition(v) + '\n'
    return code
