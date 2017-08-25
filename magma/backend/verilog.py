import types
import operator
from functools import reduce
from collections import OrderedDict, Sequence
from ..port import INPUT, OUTPUT, INOUT, flip
from ..ref import DefnRef
from ..compatibility import IntegerTypes
from ..bit import BitType, VCC, GND
from ..clock import ClockType
from ..array import ArrayKind, ArrayType
from ..bits import SIntType
from ..circuit import *
from ..clock import wiredefaultclock

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
        #print(str(t), t.iswhole(t.ts))
        if not t.iswhole(t.ts):
            # the sequence of values is concantenated
            t = [vname(i) for i in t.ts]
            t.reverse()
            return '{' + ','.join(t) + '}'

    assert not t.anon()
    return t.name.qualifiedname(sep='_')

# return the verilog declaration for the data type
def vdecl(t):
    if isinstance(t, ArrayType):
        signed = "signed " if isinstance(t, SIntType) else ""
        return '{}[{}:{}]'.format(signed, t.N-1, 0)
    else:
        assert isinstance(t, (BitType, ClockType))
        return ""

# return the verilog module args
def vmoduleargs(self):
    args = []
    for name, port in self.ports.items():
        if   port.isinput():  d = OUTPUT
        elif port.isoutput(): d = INPUT
        else: d = INOUT
        #d = flip(port.direction)
        args.append( "%s %s %s" % (d, vdecl(port), name) )
    return args


def compileinstance(self):

    #print('compileinstance', str(self))

    def arg(k,v):
        if not isinstance(v, str): v = str(v)
        return '.%s(%s)' % (k, v)

    args = []
    for k, v in self.interface.ports.items():
        #print('arg', k, v,)
        if v.isinput():
            # find the output connected to v
            w = v.value()
            if not w:
                print('Warning (verilog): input', str(v), 'not connected to an output')
                continue
            v = w
        if isinstance(k, IntegerTypes):
            args.append( vname(v) )
        else:
            args.append( arg(k,vname(v)) )

    params = []
    for k, v in self.kwargs.items():
       if k != 'loc':
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

    return '%s (%s)' % (s, ', '.join(args))

def compiledefinition(cls):

    # for now only allow Bit or Array(n, Bit)
    for name, port in cls.interface.ports.items():
        if isinstance(port, ArrayKind):
            if not isinstance(port.T, BitKind):
                print('Error: Argument', port, 'must be a an Array(n,Bit)')
                assert True


    if cls.verilogFile:
       s = cls.verilogFile
    else:
        args = ', '.join(vmoduleargs(cls.interface))
        s = 'module %s (%s);\n' % (cls.verilog_name, args)
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
            # declare a wire for each instance output
            for instance in cls.instances:
                for port in instance.interface.ports.values():
                    if port.isoutput():
                        s += 'wire %s %s;\n' % (vdecl(port), vname(port))

            #print('compile instances')
            # emit the structured verilog for each instance
            for instance in cls.instances:
                wiredefaultclock(cls, instance)
                s += compileinstance(instance) + ';\n'

            # assign to module output arguments
            for input in cls.interface.inputs():
                output = input.value()
                if output:
                    iname = vname(input)
                    oname = vname(output)
                    s += 'assign %s = %s;\n' % (iname, oname)

        s += "endmodule\n"

    return s

def find(circuit, defn):
    name = circuit.verilog_name
    if not isdefinition(circuit):
        return defn
    for i in circuit.instances:
        find(type(i), defn)
    if name not in defn:
        defn[name] = circuit
    return defn


def compile(main):
    defn = find(main,OrderedDict())

    code = ''
    for k, v in defn.items():
         print('compiling', k)
         code += compiledefinition(v) + '\n'
    return code
