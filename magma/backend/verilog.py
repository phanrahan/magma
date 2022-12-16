import os
import types
import operator
from functools import reduce
from collections import OrderedDict
from collections.abc import Sequence
from ..compiler import Compiler
from ..ref import DefnRef, TupleRef
from ..compatibility import IntegerTypes
from ..bit import Digital
from ..clock import Clock, Enable, Reset
from ..array import Array
from ..bits import SInt
from ..tuple import Tuple
from ..is_definition import isdefinition
from magma.passes.clock import drive_undriven_clock_types_in_inst
from ..logging import root_logger
from .util import get_codegen_debug_info, make_relative
from ..config import config, EnvConfig


config._register(
    verilog_backend_log_level=EnvConfig(
        "MAGMA_VERILOG_BACKEND_LOG_LEVEL", "WARN"),
)

_logger = root_logger().getChild("verilog_backend")
_logger.setLevel(config.verilog_backend_log_level)

#__all__  = ['hstr', 'bstr']
__all__  = ['hstr']


def _verilog_name_of_ref(ref):
    if isinstance(ref, TupleRef):
        return _verilog_name_of_ref(ref.tuple.name) + "_" + str(ref.index)
    return ref.qualifiedname("_")


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
    if isinstance(t, Digital):
        if t is type(t).VCC: return "1'b1"
        if t is type(t).GND: return "1'b0"
    if t.const():
        return f"{len(t)}'d{int(t)}'"

    if isinstance(t, Array):
        # print(t.ts)
        if not t.iswhole():
            # the sequence of values is concantenated
            t = [vname(i) for i in t.ts]
            t.reverse()
            return '{' + ','.join(t) + '}'

    assert not t.anon(), (t.name)
    return _verilog_name_of_ref(t.name)

# return the verilog declaration for the data type
def vdecl(t):
    if isinstance(t, Array):
        signed = "signed " if isinstance(t, SInt) else ""
        return '{}[{}:{}]'.format(signed, t.N-1, 0)
    else:
        assert isinstance(t, Digital)
        return ""

# return the verilog module args
def vmoduleargs(self):
    def append(args, port, name):
        if   port.is_input():  d = "output"
        elif port.is_output(): d = "input"
        else: d = "inout"
        args.append("%s %s %s" % (d, vdecl(port), name))

    args = []
    for name, port in self.ports.items():
        if isinstance(port, Tuple):
            for i in range(len(port)):
                append(args, port[i], vname(port[i]))
        else:
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
        if getattr(v, "debug_info", False) and get_codegen_debug_info():
            filename, lineno, module = (
                v.debug_info.filename, v.debug_info.lineno, v.debug_info.module
            )
        #print('arg', k, v,)
        if v.is_input():
            # find the output connected to v
            w = v.trace()
            if w is None:
                _logger.warning(f'{v.debug_name} not connected')
                continue
            v = w
        if isinstance(v, Tuple):
            for i in range(len(v)):
                args.append(arg('%s_%s' %
                    (v[i].name.tuple.name, v[i].name.index), vname(v[i])))
        elif isinstance(k, IntegerTypes):
            args.append( vname(v) )
        else:
            args.append( arg(k,vname(v)) )
        if getattr(v, "debug_info", False) and get_codegen_debug_info():
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
    if cls.verilogFile:
       return cls.verilogFile

    # for now only allow Bit or Array(n, Bit)
    for name, port in cls.interface.ports.items():
        if isinstance(port, Array):
            if not issubclass(port.T, Digital):
                raise Exception(f'Argument {cls.__name__}.{name} of type {type(port)} is not supported, the verilog backend only supports simple 1-d array of bits of the form Array(N, Bit)')


    args = ', '.join(vmoduleargs(cls.interface))
    s = ''
    if (
        get_codegen_debug_info() and
        cls.debug_info and
        cls.debug_info.filename and
        cls.debug_info.lineno
    ):
        s += f'// Defined at {make_relative(cls.debug_info.filename)}:{cls.debug_info.lineno}\n'
    s += 'module %s (%s);\n' % (cls.verilog_name, args)
    if cls.verilog:
        s += cls.verilog + '\n'
        if cls.verilogLib:
            import re
            for libName in cls.verilogLib:
                if re.search("\\.v$",libName):
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
                if isinstance(port, Tuple):
                    for i in range(len(port)):
                        s += wire(port[i])
                else:
                    if not port.is_input():
                        s += wire(port)

        #print('compile instances')
        # emit the structured verilog for each instance
        for instance in cls.instances:
            with cls.open():
                drive_undriven_clock_types_in_inst(cls, instance)
            if getattr(instance, "debug_info", False) and \
                    instance.debug_info.filename and instance.debug_info.lineno and \
                    get_codegen_debug_info():
                s += f"// Instanced at {make_relative(instance.debug_info.filename)}:{instance.debug_info.lineno}\n"
            s += compileinstance(instance) + ";\n"

        # assign to module output arguments
        for port in cls.interface.ports.values():
            if port.is_input():
                output = port.trace()
                if output is not None:
                    if isinstance(output, Tuple):
                        for name, input in cls.interface.ports.items():
                            if input.is_input():
                                output = input.trace()
                                assert isinstance(output, Tuple)
                                for i in range(len(input)):
                                    iname = vname(input[i])
                                    oname = vname(output[i])
                                    s += 'assign %s = %s;\n' % (iname, oname)
                    else:
                        iname = vname(port)
                        oname = vname(output)
                        if getattr(port, "debug_info", False) and get_codegen_debug_info():
                            s += f"// Wired at {make_relative(port.debug_info.filename)}:{port.debug_info.lineno}\n"
                        s += 'assign %s = %s;\n' % (iname, oname)
                else:
                    _logger.warning(f"{cls.__name__}.{port.name} is unwired")

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
         _logger.debug(f'compiling circuit {k}')
         code += compiledefinition(v) + '\n'
    return code


class VerilogCompiler(Compiler):
    def suffix(self):
        if hasattr(self.main, "verilog_file_name") and \
           os.path.splitext(self.main.verilog_file_name)[-1] == ".sv":
            return "sv"
        return "v"

    def generate_code(self):
        return compile(self.main)
