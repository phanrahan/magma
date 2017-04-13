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

def qualifiedname(t):
    if t is VCC: return '1'
    if t is GND: return '0'

    #assert not t.anon()
    return t.name.qualifiedname(sep='.')

def compileclocks(cls):
    for instance in cls.instances:
        wiredefaultclock(cls, instance)

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
