import types
import operator
from collections import OrderedDict, Sequence
from .compatibility import IntegerTypes
from .port import INPUT, OUTPUT, INOUT
from .bit import BitType, VCC, GND
from .array import ArrayType
from .tuple import TupleType
# from .circuit import isdefinition
from .wire import wiredefaultclock

def hex(i):
    if i < 10: return chr(ord('0')+i)
    else:      return chr(ord('A')+i-10)

def hstr(init, nbits):
    bits = 1 << nbits
    format = "0x" 
    nformat = []
    for i in range(bits/4):
        nformat.append(init%16)
        init /= 16
    nformat.reverse()
    return format + reduce(operator.add, map(hex, nformat))

def qualifiedname(t):
    if t is VCC: return '1'
    if t is GND: return '0'

    #assert not t.anon()
    return t.name.qualifiedname(sep='.')

def compileclocks(cls):
    for instance in cls.instances:
        wiredefaultclock(cls, instance)

def compileinstance(self):
    args = []
    for k, v in self.kwargs.items():
        if isinstance(v, tuple):
             v = hstr(v[0], v[1])
        else:
             v = str(v)
        args.append("%s=%s"%(k, v))
    return '%s = %s(%s)' % (str(self), str(type(self)), ', '.join(args))

def compilewire(input):

    output = input.value()
    if isinstance(output, ArrayType) or isinstance(output, TupleType):
        if not output.iswhole(output.ts):
            s = ''
            for i in range(len(input)):
                s += compilewire( input[i] )
            return s

    iname = qualifiedname( input )
    oname = qualifiedname( output )
    return 'wire(%s, %s)\n' % (oname, iname)

def compile(main):

    compileclocks(main)

    defn = main.find(OrderedDict())

    code = ''
    for k, v in defn.items():
         #print('compiling', k)
         code += repr(v) + '\n'
    return code
