from __future__ import division
from itertools import chain
from collections import OrderedDict
from .ref import AnonRef, InstRef, DefnRef
from .t import Type, Kind, In, Out, Flip
from .bit import BitKind, MakeBit
from .port import INPUT, OUTPUT, INOUT
#from .bit import *
from .clock import ClockType, ClockTypes
from .array import ArrayType
from .tuple import TupleType
from .compatibility import IntegerTypes, StringTypes

__all__  = ['DeclareInterface']
__all__ += ['Interface']
__all__ += ['InterfaceKind']

# flatten an iterable of iterables to list
def flatten(l):
    return list(chain(*l))

#
# parse argument declaration of the form
#
#  (name0, type0, name1, type1, ..., namen, typen)
#
def parse(decl):
    #print(decl)
    n = len(decl)
    assert n % 2 == 0

    names = []
    ports = []
    for i in range(0,n,2):
        name = decl[i]   # name
        if not name:
            name = i//2
        port = decl[i+1] # type

        assert isinstance(port, Kind) or isinstance(port, Type)


        names.append(name)
        ports.append(port)

    return names, ports

#
# Abstract Base Class for an Interface
#
class _Interface(Type):

    def __str__(self):
        return str(type(self))

    def __repr__(self):
        s = ""
        for name, input in self.ports.items():
            if input.isinput():
                output = input.value()
                if isinstance(output, ArrayType) \
                  or isinstance(output, TupleType):
                    if not output.iswhole(output.ts):
                        for i in range(len(input)):
                            iname = repr( input[i] )
                            oname = repr( output[i] )
                            s += 'wire({}, {})\n'.format(oname, iname)
                        continue
                iname = repr( input )
                oname = repr( output )
                s += 'wire({}, {})\n'.format(oname, iname)
        return s

    @classmethod
    def items(cls):
        return cls.ports.items()

    def __iter__(self):
        return iter(self.ports)

    def __len__(self):
        return len(self.ports.keys())

    def __getitem__(self, key):
        if isinstance(key, int):
            if isinstance(key,slice):
                return array([self[i] for i in range(*key.indices(len(self)))])
            else:
                n = len(self)
                assert -n < key and key < n, "key: %d, self.N: %d" %(key,len(self))
                return self.arguments()[key]
        else:
            assert isinstance(key, str)
            return self.ports[key]

    # return all the argument ports
    def arguments(self):
        return [port  for name, port in self.ports.items()]

    # return all the argument input ports
    def inputs(self, include_clocks=False):
        return [port for name, port in self.ports.items() \
                    if port.isinput() and (not isinstance(port, ClockTypes) or include_clocks) ]
#                                    name not in ['SET', 'CIN']]

    # return all the argument output ports
    def outputs(self):
        return [port for name, port in self.ports.items() if port.isoutput()]


    # return all the arguments as name, port
    def args(self):
        return flatten([name, port] for name, port in self.ports.items())

    # return all the arguments as name, flip(port)
    #   same as the declaration
    def decl(self):
        return flatten([name, type(port).flip()] \
                             for name, port in self.ports.items()  )


    # return all the input arguments as name, port
    def inputargs(self):
        return flatten( \
                [name, port] for name, port in self.ports.items() \
                    if port.isinput() and not isinstance(port, ClockTypes) )
#                                    name not in ['SET', 'CIN']] )

    # return all the output arguments as name, port
    def outputargs(self):
        return flatten( [name, port] for name, port in self.ports.items() \
                            if port.isoutput() )

    # return all the clock arguments as name, port
    def clockargs(self):
        return flatten( [name, port] for name, port in self.ports.items() \
                            if isinstance(port, ClockTypes)  )
#                                        or name in ['SET'] ] )

    # return all the clock argument names
    def clockargnames(self):
        return [name for name, port in self.ports.items() \
                    if isinstance(port, ClockTypes) ]
#                                or name in ['SET'] ]


    # return True if this interface has a Clock
    def isclocked(self):
        for name, port in self.ports.items():
            if isinstance(port, ClockType):
                return True
        return False

#
# Interface class
#
# This function assumes the port instances are provided
#
#  e.g. Interface('I0', In(Bit)(), 'I1', In(Bit)(), 'O', Out(Bit)())
#
class Interface(_Interface):
    def __init__(self, decl, renamed_ports={}):

        names, ports = parse(decl)

        # setup ports
        args = OrderedDict()

        for name, port in zip(names, ports):

            if isinstance(name, IntegerTypes):
                name = str(name) # convert integer to str, e.g. 0 to "0"

            if name in renamed_ports:
                raise NotImplementedError()

            args[name] = port

        self.ports = args

    def __str__(self):
        return f'Interface({", ".join(f"{k}: {v}" for k, v in self.ports.items())})'


#
# _DeclareInterface class
#
# First, an Interface is declared
#
#  Interface = DeclareInterface('I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))
#
# Then, the interface is instanced
#
#  interface = Interface()
#
class _DeclareInterface(_Interface):
    def __init__(self, renamed_ports={}, inst=None, defn=None):

        # parse the class Interface declaration
        names, ports = parse(self.Decl)

        args = OrderedDict()

        for name, port in zip(names, ports):
            if   inst: ref = InstRef(inst, name)
            elif defn: ref = DefnRef(defn, name)
            else:      ref = AnonRef(name)

            if hasattr(port, "origPortName"):
                ref.name = port.origPortName
            if name in renamed_ports:
                ref.name = renamed_ports[name]

            if defn:
               port = port.flip()

            args[name] = port(name=ref)

        self.ports = args

class InterfaceKind(Kind):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ports = []
        key = None
        for i, arg in enumerate(cls.Decl):
            if i % 2 == 0:
                key = arg
            else:
                ports.append((key, arg))
        cls.ports = OrderedDict(ports)

    def items(cls):
        return cls.ports.items()

    def __iter__(cls):
        return iter(cls.ports)

    def __str__(cls):
        args = []
        for i, arg in enumerate(cls.Decl):
            if i % 2 == 0:
                args.append('"{}"'.format(arg))
            else:
                args.append(str(arg))
        return ', '.join(args)

    def __eq__(cls, rhs):
        if not isinstance(rhs, InterfaceKind): return False

        if cls.Decl != rhs.Decl: return False
        return True

    __ne__=Kind.__ne__
    __hash__=Kind.__hash__


#
# Interface factory
#
def DeclareInterface(*decl, **kwargs):
    name = '%s(%s)' % ('Interface', ', '.join([str(a) for a in decl]))
    #print('DeclareInterface', name)
    dct = dict(Decl=decl, **kwargs)
    return InterfaceKind(name, (_DeclareInterface,), dct)

