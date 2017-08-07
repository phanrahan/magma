from .port import *
from .array import *
from .wire import *
from .circuit import *

__ALL__  = ['compose']
__ALL__ += ['curry', 'uncurry']
__ALL__ += ['row', 'col', 'map']
__ALL__ += ['fork', 'join', 'flat']
__ALL__ += ['fold', 'scan']
__ALL__ += ['braid']

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
        args += ['input %s' % iarg, iargs[0]]
    if not nooarg:
        args += ['output %s' % oarg, array(*oargs)]
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
        args += ['input %s' % iarg, iargs[0]]
    if not nooarg:
        args += ['output %s' % oarg, array(*oargs)]
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
        args += ['input %s' % iarg, iargs[0]]
    if not nooarg:
        args += ['output %s' % oarg, oargs[n-1]]
    return args

def rfoldarg(iarg, oarg, interfaces, noiarg=False, nooarg=False):
    iargs = getarg(iarg, interfaces)
    oargs = getarg(oarg, interfaces)
    n = len(interfaces)
    for i in range(n-1):
        wire(oargs[i+1], iargs[i])
    args = []
    if not noiarg:
        args += ['input %s' % iarg, iargs[0]]
    if not nooarg:
        args += ['output %s' % oarg, oargs[n-1]]
    return args

# return ["input arg", args] from a list of interfaces
def forkarg(arg, interfaces):
    iargs = getarg(arg, interfaces)
    oarg = type(iargs[0])()
    for iarg in iargs:
         wire(oarg, iarg)
    return ['input %s' % arg, oarg]

# return ["input/output arg", array] from a list of interfaces
def joinarg(arg, interfaces):
    args = getarg(arg, interfaces)
    direction = getdirection(args)
    #print('joinarg', args)
    return ['%s %s' % (direction, arg), array(*args)]

# return ["input/output arg", array] from a list of interfaces
def flatarg(arg, interfaces):
    args = getarg(arg, interfaces)
    direction = getdirection(args)
    flatargs = []
    for a in args:
        for i in range(len(a)):
            flatargs.append(a[i])
    return ['%s %s' % (direction, arg), array(*flatargs)]


def braid(circuits, 
            forkargs=[],
            joinargs=[],
            flatargs=[],
            foldargs={}, rfoldargs={},
            scanargs={}, rscanargs={}):

    forkargs = list(forkargs)

    # by default, clkargs are added to foldargs
    for clkarg in ['RESET', 'SET', 'CE', 'CLK']:
        if clkarg in forkargs: continue
        if clkarg in joinargs: continue
        if clkarg in flatargs: continue
        if clkarg in foldargs.keys(): continue
        if clkarg in rfoldargs.keys(): continue
        if clkarg in scanargs.keys(): continue
        if clkarg in rscanargs.keys(): continue
        forkargs.append(clkarg)

    interfaces = [circuit.interface for circuit in circuits]

    nojoinargs = []
    # scans
    for k, v in scanargs.items():
        nojoinargs.append(k)
        nojoinargs.append(v)
    for k, v in rscanargs.items():
        nojoinargs.append(k)
        nojoinargs.append(v)

    # folds
    for k, v in foldargs.items():
        nojoinargs.append(k)
        nojoinargs.append(v)
    for k, v in rfoldargs.items():
        nojoinargs.append(k)
        nojoinargs.append(v)

    # fork
    for k in forkargs:
        nojoinargs.append(k)

    # flat
    for k in flatargs:
        nojoinargs.append(k)

    #print('nojoin', nojoinargs)

    joinargs = []
    for name in interfaces[0].ports.keys():
        #print(name, name in nojoinargs)
        if name not in nojoinargs: 
            joinargs.append(name)

    #print('join', joinargs)
    #print('flat', flatargs)
    #print('fork', forkargs)
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

        elif key in flatargs:
            #print('flattening', key)
            args += flatarg(key, interfaces)

    #print(args)
    return AnonymousCircuit(args)

def flat(*circuits):
    if len(circuits) == 1: circuits = circuits[0]
    flatargs = getargbydirection(circuits[0].interface, INPUT)
    return braid(circuits, flatargs=flatargs)

def fork(*circuits):
    """Wire input to all the inputs, concatenate output"""
    if len(circuits) == 1: circuits = circuits[0]
    forkargs = getargbydirection(circuits[0].interface, INPUT)
    return braid(circuits, forkargs=forkargs)

def join(*circuits):
    """concatenate input and concatenate output"""
    if len(circuits) == 1: circuits = circuits[0]
    return braid(circuits)

def fold(*circuits, **kwargs):
    """fold"""
    if len(circuits) == 1: circuits = circuits[0]
    return braid(circuits, **kwargs)

def scan(*circuits, **kwargs):
    """scan"""
    if len(circuits) == 1: circuits = circuits[0]
    return braid(circuits, **kwargs)



def inputargs(circuit):
    return circuit.interface.inputargs()

def outputargs(circuit):
    return circuit.interface.outputargs()

def compose(circuit1, circuit2):
    # check that circuit2.outputs == circuit1.inputs
    wire(circuit2, circuit1)
    args = []
    args += inputargs(circuit2)
    args += outputargs(circuit1)
    return AnonymousCircuit(args)


#
# this could be generalized to break apart an argument which
# is an array into a list of new arguments
#
# the naming convention here is arbitrary and should be improved
#
def curry(circuit, prefix='I'):
    args = []
    for name, port in circuit.interface.ports.items():
        if name == prefix and port.isinput():
           for i in range(len(port)):
               args.append('input %s%d' % (name, i))
               args.append(port[i])
        else:
           if   port.isinput():  d = INPUT
           elif port.isoutput(): d = OUTPUT
           elif port.isinout():  d = INOUT
           args.append('%s %s' % (d, name))
           args.append(port)

    #print(args)
    return AnonymousCircuit(args)



def inputs(circuit):
    input = circuit.interface.inputs()
    if len(input) == 1:
        return input[0]
    else:
        return array(*input)

def outputs(circuit):
    output = circuit.interface.outputs()
    if len(output) == 1:
        return output[0]
    else:
        return Array(*output)

def uncurry(circuit, prefix='I'):

    uncurryargs = []
    for name, port in circuit.interface.ports.items():
        if name.startswith(prefix):
           assert port.direction == INPUT 
           uncurryargs.append(port)

    args = ['input %s' % prefix, array(*uncurryargs)]

    for name, port in circuit.interface.ports.items():
        if not name.startswith(prefix):
           args += ['%s %s' % (port.direction, name), port]

    #print(args)
    return AnonymousCircuit(args)


def row(f, n):
    return [f(x) for x in range(n)]

def col(f, n):
    return [f(y) for y in range(n)]

