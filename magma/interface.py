from __future__ import division
from collections import OrderedDict
from .ref import AnonRef, InstRef, DefnRef
from .t import *
from .port import *
from .bit import *
from .array import *
from .tuple import TupleType
from .compatibility import IntegerTypes, StringTypes

__all__  = ['DeclareInterface']
__all__ += ['Interface']
__all__ += ['ClockInterface']

def parse(decl):
    n = len(decl)
    assert n % 2 == 0

    directions = []
    names = []
    ports = []
    for i in range(0,n,2):
        argi = decl[i].split() # [input|output] name
        port = decl[i+1]       # type

        assert len(argi) > 0 and len(argi) <= 2

        #print(str(port), isinstance(port, Kind))
        assert isinstance(port, Kind) or isinstance(port, Type)
        if isinstance(port, Kind):
            if   port._isinput():  portdirection = INPUT
            elif port._isoutput(): portdirection = OUTPUT
            elif port._isinout():  portdirection = INOUT
            else:                  portdirection = None
        else:
            if   port.isinput():  portdirection = INPUT
            elif port.isoutput(): portdirection = OUTPUT
            elif port.isinout():  portdirection = INOUT
            else:                 portdirection = None

        if len(argi) == 2:
            # depreciate this method of setting input and output
            direction = argi[0]
            name = argi[1]
        else: # len(argi) == 1
            if argi[0] in [INPUT, OUTPUT, INOUT]:
                direction = argi[0]
                name = i // 2
            else:
                direction = portdirection
                name = argi[0]

        if direction is None:
            direction = portdirection

        if direction is None:
            print("Error:", name, "must have a direciton")
        else: 
            if portdirection is not None and direction != portdirection:
                print('Warning: directions inconsistent {} {}'.format(direction, portdirection))
            # direction has priority

        directions.append(direction)
        names.append(name)
        ports.append(port)

    return directions, names, ports

#
# Abstract Base Class for an Interface
#
class _Interface(Type):

    def __str__(self):
        I = []
        for name, port in self.ports.items():
            if port.isinput():
                s = '%s : %s' % (name, type(port))
                I.append(s)

        O = []
        for name, port in self.ports.items():
            if port.isoutput():
                s = '%s : %s' % (name, type(port))
                O.append(s)

        return ', '.join(I) + ' -> ' + ', '.join(O)

    def __repr__(self):
        s = ""
        for input in self.inputs():
            output = input.value()
            if isinstance(output, ArrayType) or isinstance(output, TupleType):
                if not output.iswhole(output.ts):
                    for i in range(len(input)):
                        iname = repr( input[i] )
                        oname = repr( output[i] )
                        s += 'wire(%s, %s)\n' % (oname, iname)
            else:
                iname = repr( input )
                oname = repr( output )
                s += 'wire(%s, %s)\n' % (oname, iname)
        return s

    def __len__(self):
        return len(self.ports.keys())
                
    def __getitem__(self, key):
        if isinstance(key,slice):
            return array(*[self[i] for i in range(*key.indices(len(self)))])
        else:
            assert 0 <= key and key < len(self), "key: %d, self.N: %d" %(key,len(self))
            return self.arguments()[key]

    def inputs(self):
        input = []
        for name, port in self.ports.items():
            if port.isinput():
                if name in ['RESET', 'SET', 'CE', 'CLK', 'CIN']: 
                    continue
                input.append(port)
        return input

    def outputs(self):
        l = []
        for name, port in self.ports.items():
            if port.isoutput():
                if name in ['COUT']: 
                    continue
                l.append(port)
        return l

    def arguments(self):
        l = []
        for name, port in self.ports.items():
            l.append(port)
        return l

    def inputargs(self):
        l = []
        for name, port in self.ports.items():
            if port.isinput():
                if name in ['RESET', 'SET', 'CE', 'CLK', 'CIN']: 
                    continue
                l.append('input %s' % name)
                l.append(port)
        return l

    def outputargs(self):
        l = []
        for name, port in self.ports.items():
            if port.isoutput():
                if name in ['COUT']: 
                    continue
                l.append('output %s' % name)
                l.append(port)
        return l

    def clockargs(self):
        l = []
        for name, port in self.ports.items():
            if name in ['RESET', 'SET', 'CE', 'CLK']: 
                l.append('input %s' % name)
                l.append(port)
        return l

    def args(self):
        l = []
        for name, port in self.ports.items():
            if   port.isinput():  d = INPUT
            elif port.isoutput(): d = OUTPUT
            elif port.isinout():  d = INOUT
            l.append('%s %s' % (d, name))
            l.append(port)
        return l

    def decl(self):
        d = []
        for name, port in self.ports.items():
            if   port.isinput(): t = 'output'
            elif port.isoutput(): t = 'input'

            d  += [t + ' ' + name, type(port).flip()]

        return d

    def isclocked(self):
        for name, port in self.ports.items():
            if name in ['RESET', 'SET', 'CE', 'CLK']: 
                return True
        return False

#
# Interface class
#
# An interface is an OrderedDict that maps from names to ports
#
# This function assumes the port instances are provided
#
#  e.g. Interface('input I0', Bit(), 'input I1', Bit(), 'output O', Bit())
#
class Interface(_Interface):
    def __init__(self, decl):

        directions, names, ports = parse(decl)

        # setup ports
        args = OrderedDict()

        for i in range(len(directions)):
            direction = directions[i]
            name = names[i]
            port = ports[i]

            if isinstance(name, IntegerTypes):
                name = str(name)

            args[name] = port

        self.ports = args


#
# _DeclareInterface class
#
# An interface is an OrderedDict that maps from names to ports
#
# This function assumes the ports are types. When an instance
# of the interface is created.
#
#  Interface = DeclareInterface('I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))
#
#  interface = Interface() will instantiate the ports
#
class _DeclareInterface(_Interface):
    def __init__(self, inst=None, defn=None):

        directions, names, ports = parse(self.Decl)

        # setup ports
        args = OrderedDict()

        for i in range(len(directions)):
            direction = directions[i]
            name = names[i]
            port = ports[i]

            if defn:
               if   direction == OUTPUT: direction = INPUT
               elif direction == INPUT:  direction = OUTPUT

            if   inst: ref = InstRef(inst, name)
            elif defn: ref = DefnRef(defn, name)
            else:      ref = AnonRef(name)

            port = port.qualify(direction)

            args[name] = port(name=ref)

        self.ports = args

class InterfaceKind(Kind):
    def __eq__(cls, rhs):
        if not isinstance(rhs, InterfaceKind): return False

        if cls.Decl != rhs.Decl: return False
        return True

    __ne__=Kind.__ne__
    __hash__=Kind.__hash__


#
# Interface factory
#
def DeclareInterface(*decl):
    name = '%s[%s]' % ('Interface', ', '.join([str(a) for a in decl]))
    #print('DeclareInterface', name)
    dct = dict(Decl=decl)
    return InterfaceKind(name, (_DeclareInterface,), dct)


def ClockInterface(ce=False, r=False, s=False):
    args = ['input CLK', Bit]
    if ce: args += ['input CE', Bit]
    if r:  args += ['input RESET', Bit]
    if s:  args += ['input SET', Bit]
    return args

if __name__ == '__main__':
    I0 = DeclareInterface("input a", Bit, "output b", Array2)
    print(I0)
    i0 = I0()
    print(i0)

    I1 = DeclareInterface("input a", Bit, "output b", Array2)
    assert I0 == I1

