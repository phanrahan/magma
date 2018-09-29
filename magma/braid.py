from .port import INPUT, OUTPUT, INOUT
from .array import Array, ArrayType
from .conversions import array
from .circuit import AnonymousCircuit
from .wire import wire

__ALL__  = ['compose']
__ALL__ += ['curry', 'uncurry']
__ALL__ += ['flat', 'partition']
__ALL__ += ['row', 'col', 'map_']
__ALL__ += ['fork', 'join']
__ALL__ += ['fold', 'scan']
__ALL__ += ['braid']

# flatten list of lists
def flatten(l):
    return sum(l, [])

# return a list of all the arguments
# with a given name from a list of interfaces
def getarg(arg, interfaces):
    return [i.ports[arg] for i in interfaces]

def getdirection(args):
    a = args[0]
    if isinstance(a, list):
        a = a[0]
    if a.isinput():  return INPUT
    if a.isoutput(): return OUTPUT
    if a.isinout():  return INOUT
    return None

# return a list of all the arguments
# in a given direction from a list of interfaces
def getargbydirection(interface, direction):
    args = []
    for name, port in interface.ports.items():
        if port.isoriented(direction):
            args.append(name)
    return args

#
def lscanarg(iarg, oarg, interfaces, noiarg=False, nooarg=False):
    iargs = getarg(iarg, interfaces)
    oargs = getarg(oarg, interfaces)
    n = len(interfaces)
    for i in range(n-1):
        wire(oargs[i], iargs[i+1])

    args = []
    if not noiarg:
        args += [iarg, iargs[0]]
    if not nooarg:
        args += [oarg, array(oargs)]
    return args

#
def rscanarg(iarg, oarg, interfaces, noiarg=False, nooarg=False):
    iargs = getarg(iarg, interfaces)
    oargs = getarg(oarg, interfaces)
    n = len(interfaces)
    for i in range(n-1):
        wire(oargs[i+1], iargs[i])

    args = []
    if not noiarg:
        args += [iarg, iargs[0]]
    if not nooarg:
        args += [oarg, array(oargs)]
    return args

#
def lfoldarg(iarg, oarg, interfaces, noiarg=False, nooarg=False):
    iargs = getarg(iarg, interfaces)
    oargs = getarg(oarg, interfaces)
    n = len(interfaces)
    for i in range(n-1):
        wire(oargs[i], iargs[i+1])
    args = []
    if not noiarg:
        args += [iarg, iargs[0]]
    if not nooarg:
        args += [oarg, oargs[n-1]]
    return args

def rfoldarg(iarg, oarg, interfaces, noiarg=False, nooarg=False):
    iargs = getarg(iarg, interfaces)
    oargs = getarg(oarg, interfaces)
    n = len(interfaces)
    for i in range(n-1):
        wire(oargs[i+1], iargs[i])
    args = []
    if not noiarg:
        args += [iarg, iargs[0]]
    if not nooarg:
        args += [oarg, oargs[n-1]]
    return args

# return [arg, args] from a list of interfaces
def forkarg(arg, interfaces):
    iargs = getarg(arg, interfaces)
    oarg = type(iargs[0])() # create a single anonymous value
    for iarg in iargs:
         wire(oarg, iarg) # wire the anonymous value to all the forked args
    return [arg, oarg]

# return [arg, array] from a list of interfaces
def joinarg(arg, interfaces):
    args = getarg(arg, interfaces)
    #direction = getdirection(args)
    #print('joinarg', args)
    return [arg, array(args)]


# all powerful braid functions
#
#  circuits : list of circuits which should all have the same signature
#
#  forkargs : list of argument names to fork
#   this argument is wired to all the circuits
#  joinargs : list of argument names to join
#   this argument is equal an array of all the arguments from circuits
#  foldargs : dict of argument namein:nameout, set namein[i+1] to namout[i]
#  rfoldargs : dict of argument namein:nameout, set namein[i-1] to namout[i]
#    namein[0] is retained in the result,
#    nameout[n-1] is retained in the result
#  scanargs : dict of argument namein:nameout, set namein[i+1] to namout[i]
#  rscanargs : dict of argument namein:nameout, set namein[i-1] to namout[i]
#    namein[0] is retained in the result,
#    the array nameout is retained in the result
#
# by default, clock arguments are forked,
#  unless they appear in another keyword
#
# by default, any arguments not appearing in a keyword are joined
#
def braid(circuits,
            forkargs=[],
            joinargs=[],
            foldargs={}, rfoldargs={},
            scanargs={}, rscanargs={}):

    forkargs = list(forkargs)

    interfaces = [circuit.interface for circuit in circuits]

    # by default, clkargs are added to forkargs,
    # unless they appear in another keyword
    for clkarg in interfaces[0].clockargnames():
        if clkarg in forkargs: continue
        if clkarg in joinargs: continue
        if clkarg in foldargs.keys(): continue
        if clkarg in rfoldargs.keys(): continue
        if clkarg in scanargs.keys(): continue
        if clkarg in rscanargs.keys(): continue
        forkargs.append(clkarg)

    # do NOT join arguments if they appear in another keyword
    nojoinargs = list(forkargs)
    nojoinargs += flatten( [[k, v] for k, v in foldargs.items()] )
    nojoinargs += flatten( [[k, v] for k, v in rfoldargs.items()] )
    nojoinargs += flatten( [[k, v] for k, v in scanargs.items()] )
    nojoinargs += flatten( [[k, v] for k, v in rscanargs.items()] )

    joinargs = [name for name in interfaces[0].ports.keys() \
                    if name not in nojoinargs]

    #print('fork', forkargs)
    #print('flat', flatargs)
    #print('join', joinargs)
    #print('fold', foldargs)
    #print('scan', scanargs)
    args = []
    for key in interfaces[0].ports.keys():
        if   key in foldargs:
            iarg = key
            oarg = foldargs[key]
            noiarg = iarg in forkargs or iarg in joinargs
            nooarg = oarg in joinargs
            #print('lfolding', iarg, key, noiarg, nooarg)
            args += lfoldarg(iarg, oarg, interfaces, noiarg, nooarg)
        elif key in rfoldargs:
            iarg = key
            oarg = rfoldargs[key]
            #print('rfolding', iarg, key)
            noiarg = iarg in forkargs or iarg in joinargs
            nooarg = oarg in joinargs
            args += rfoldarg(iarg, oarg, interfaces, noiarg, nooarg)

        elif key in scanargs:
            iarg = key
            oarg = scanargs[key]
            #print('scanning', iarg, key)
            noiarg = iarg in forkargs or iarg in joinargs
            nooarg = oarg in joinargs
            args += lscanarg(iarg, oarg, interfaces, noiarg, nooarg)
        elif key in rscanargs:
            iarg = key
            oarg = rscanargs[key]
            #print('scanning', iarg, key)
            noiarg = iarg in forkargs or iarg in joinargs
            nooarg = oarg in joinargs
            args += rscanarg(iarg, oarg, interfaces, noiarg, nooarg)

        elif key in forkargs:
            #print('forking', key)
            args += forkarg(key, interfaces)

        elif key in joinargs:
            #print('joining', key)
            args += joinarg(key, interfaces)

    #print(args)
    return AnonymousCircuit(args)

# fork all inputs
def fork(*circuits):
    """Wire input to all the inputs, concatenate output"""
    if len(circuits) == 1:
        circuits = circuits[0]
    forkargs = getargbydirection(circuits[0].interface, INPUT)
    return braid(circuits, forkargs=forkargs)

# join all inputs
def join(*circuits, joinargs=[]):
    """concatenate input and concatenate output"""
    if len(circuits) == 1:
        circuits = circuits[0]
    return braid(circuits)



def fold(*circuits, foldargs={"I":"O"}, **kwargs):
    """fold"""
    if len(circuits) == 1:
        circuits = circuits[0]
    return braid(circuits, foldargs=foldargs, **kwargs)

def scan(*circuits, scanargs={"I":"O"}, **kwargs):
    """scan"""
    if len(circuits) == 1:
        circuits = circuits[0]
    return braid(circuits, scanargs=scanargs, **kwargs)


def compose2(circuit1, circuit2):
    # collect input argument names from circuit1
    iargs = circuit1.interface.inputargs()
    iargs = [iargs[2*i] for i in range(len(iargs)//2)]

    # collect output argument names from circuit2
    oargs = circuit2.interface.outputargs()
    oargs = [oargs[2*i] for i in range(len(oargs)//2)]

    if len(iargs) != len(oargs):
        error("Number of inputs must equal the number of outputs")

    # wire outputs of circuit2 to the inputs of circuit1
    for I, O in zip(iargs, oargs):
        #print('wire({},{})'.format(O,I))
        wire( getattr(circuit2,O), getattr(circuit1,I) )

    # compute new arguments
    args = circuit2.interface.inputargs() + circuit1.interface.outputargs()

    # fork clock arguments
    clkargs1 = set(circuit1.interface.clockargnames())
    clkargs2 = set(circuit2.interface.clockargnames())
    if clkargs1 != clkargs2:
        error("Circuits have different clock arguments")
    interfaces = [circuit2.interface, circuit1.interface]
    for clkarg in clkargs1:
        args += forkarg(clkarg, interfaces)

    return AnonymousCircuit(args)

def compose(*circuits):
    if len(circuits) == 1:
        circuits = circuits[0]

    if len(circuits) == 1:
        return circuits[0]

    return compose2(circuits[0], compose(circuits[1:])) # right associative


#
# curry a circuit
#
#  the input argument named prefix, which must be an array,
#  is broken into separate input arguments
#
#  for example, if prefix='I',
#    then "I", array([i0, i1]) -> "I0", i0, "I1", i1
#
# all other inputs remain unchanged
#
def curry(circuit, prefix='I'):
    args = []
    for name, port in circuit.interface.ports.items():
        if not port.wired() and name == prefix and port.isinput():
           for i in range(len(port)):
               args.append('{}{}'.format(name, i))
               args.append(port[i])
        else:
           args.append(name)
           args.append(port)

    #print(args)
    return AnonymousCircuit(args)

#
# uncurry a circuit
#
#  all input arguments whose names begin with prefix
#  are collected into a single input argument named prefix,
#  which is an array constructed from of the input arguments
#
#  for example, if prefix='I',
#    then "I0", i0, "I1", i1 -> "I", array([i0, i1])
#
#  the uncurry argument is the first argument in the result
#
# all other inputs remain unchanged.
#
def uncurry(circuit, prefix='I'):

    otherargs = []
    uncurryargs = []
    for name, port in circuit.interface.ports.items():
        # should we insert the argument in the position of the first match?
        if not port.wired() and name.startswith(prefix) and port.isinput():
           #print('uncurry', name)
           uncurryargs.append(port)
        else:
           otherargs += [name, port]

    return AnonymousCircuit( [prefix, array(uncurryargs)] + otherargs )

# flatten all the args matching names in flatargs
#  each input must be an array
def flat(circuit, flatargs=['I', 'O']):
    args = []
    for name, port in circuit.interface.ports.items():
        if not port.wired() and name in flatargs \
               and isinstance(port, ArrayType) \
                   and isinstance(port[0], ArrayType):
           #print('flat',name)
           ts = sum([p.as_list() for p in port], [])
           args += [name, array(ts)]
        else:
           args += [name, port]
    return AnonymousCircuit( args )

# concat all the inputs whose name starts with prefix
#  each input must be an array
def partition(circuit, n, prefix='I'):
    args = []
    for name, port in circuit.interface.ports.items():
        # should we insert the argument in the position of the first match?
        if not port.wired() and name == prefix and isinstance(port, ArrayType):
           l = port.as_list()
           l = [array(l[i:i + n]) for i in range(0, len(l), n)]
           for i in range(len(l)):
               args += ['{}{}'.format(prefix,i), l[i]]
        else:
           args += [name, port]
    return AnonymousCircuit( args )


def row(f, n):
    return [f(x) for x in range(n)]

def col(f, n):
    return [f(y) for y in range(n)]

def map_(f, n):
    return [f() for _ in range(n)]
