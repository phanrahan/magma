import six
import inspect
from .interface import *
from .wire import *

__all__  = ['CircuitType']

__all__ += ['DeclareCircuit'] 

__all__ += ['DefineCircuit', 'EndCircuit']
__all__ += ['Circuit']
__all__ += ['isdefinition']
__all__ += ['isprimitive']
__all__ += ['CopyInstance']

__all__ += ['AnonymousCircuit']


# create an attribute for each port
def setports(self, ports):
    #print('setports', ports)
    for name, port in ports.items():
        #print(self, port, type(port))
        if isinstance(name, str):
            setattr(self, name, port)

#
# Metaclass for creating circuits
#
class CircuitKind(type):
    
    def __new__(metacls, name, bases, dct):
        #print('DefineCircuitKind new:', name)

        # override circuit class name
        if 'name' not in dct:
             dct['name'] = name
        name = dct['name']

        if 'primitive' not in dct:
            dct['primitive'] = False

        # create a new circuit class
        self = type.__new__(metacls, name, bases, dct)

        # create interface for this circuit class 
        if hasattr(self, 'IO'):
            # turn IO attribite into an Interface
            self.IO = DeclareInterface(*self.IO)

        return self

    def __call__(cls, *largs, **kwargs):
        #print('DefineCircuitKind call:', largs, kwargs)
        self = super(CircuitKind, cls).__call__(*largs, **kwargs)

        # instance interface for this instance
        if hasattr(cls, 'IO'):
            self.setinterface(cls.IO(inst=self))

        return self

    def __str__(cls):
        return cls.__name__

    def getarea(cls):
        return (1, cls.cells)

#
# Abstract base class for circuits
#
@six.add_metaclass(CircuitKind)
class _CircuitType(object):

    def __init__(self, *largs, **kwargs):
        self.largs = largs
        self.kwargs = kwargs

        self.name = kwargs['name'] if 'name' in kwargs else ""

        self.loc = kwargs['loc'] if 'loc' in kwargs else None
        if self.loc and len(self.loc) == 2:
            self.loc = (self.loc[0], self.loc[1], 0)

        self.interface = None
        self.defn = None
        self.used = False


    def __str__(self):
        return self.name

    def __getitem__(self, key):
        return self.interface[key]

    def __call__(input, *outputs, **kw):

        # if the argument is a single circuit, 
        #   replace it with the circuit's outputs
        if len(outputs) == 1 and isinstance(outputs[0], _CircuitType):
             outputs = outputs[0].interface.outputs()

        # wire up argument list, if present
        no = len(outputs)
        if no != 0:
            inputs = input.interface.inputs()
            ni = len(inputs)
            if ni != no:
                if no > ni:
                    print("Warning: wiring only %d of the %d arguments"
                        % (ni, no))
                else:
                    print("Warning: wiring only %d of the %d circuit inputs"
                        % (no, ni))

            for i in range(min(ni,no)):
                wire(outputs[i], inputs[i])

        # wire up extra arguments, name to name
        for key, value in kw.items():
            if key == 'ce':    key = 'CE'
            if key == 'set':   key = 'SET'
            if key == 'reset': key = 'RESET'
            if hasattr(input, key):
                i = getattr(input, key)
                wire( value, getattr(input, key) )
            else:
                print('Warning: circuit does not have', key)

        o = input.interface.outputs()
        return o[0] if len(o) == 1 else tuple(o)

    def setinterface(self, interface):
        setports(self, interface.ports)
        self.interface = interface
        return self

    def on(self):
        self.used = True
        return self

    def off(self):
        self.used = False
        return self

    def rename(self, name):
        self.name = name
        return self

    def isclocked(self):
        return self.interface.isclocked()

    def clockargs(self):
        return self.interface.clockargs()

    def inputargs(self):
        return self.interface.inputargs()

    def outputargs(self):
        return self.interface.outputargs()


# Maintain a current definition and stack of nested definitions

currentDefinition = None
currentDefinitionStack = []

def pushDefinition(defn):
    global currentDefinition
    if currentDefinition:
        currentDefinitionStack.append(currentDefinition)
    currentDefinition = defn

def popDefinition():
    global currentDefinition
    if len(currentDefinitionStack) > 0:
        currentDefinition = currentDefinitionStack.pop()
    else:
        currentDefinition = None

#  A circuit is a definition if it has instances
def isdefinition(circuit):
    'Return whether a circuit is a module definition'
    return hasattr(circuit, "instances")

def isprimitive(circuit):
    return circuit.primitive

# 
# Placed circuit - instances placed in a definition
#
class CircuitType(_CircuitType):
    def __init__(self, *largs, **kwargs):
        super(CircuitType, self).__init__(*largs, **kwargs)

        # Circuit instances are placed if within a definition
        global currentDefinition
        if currentDefinition:
             currentDefinition.place(self)

#
# AnonymousCircuits are like macros - the circuit instances are not placed
#
def AnonymousCircuit(*decl):
    n = len(decl)
    if   n == 0: 
        return None
    elif n == 1:
        decl = decl[0]

    # instance an unplaced circuit 
    return _CircuitType().setinterface(Interface(decl))



# DeclareCircuit Factory
def DeclareCircuit(name, *decl, **args):
    dct = dict(IO=decl, cells=args.get('cells', 0), alignment=1, primitive=args.get('primitive', True), stateful=args.get('stateful', False), simulate=args.get('simulate'))
    return CircuitKind( name, (CircuitType,), dct )



Cache = {}

def __magma_clear_circuit_cache():
    """
    Used in testing to clear Cache to prevent name conflicts from different
    tests
    """
    Cache.clear()

class DefineCircuitKind(CircuitKind):
    def __new__(metacls, name, bases, dct):

        # override name if present in dict
        if 'name' not in dct:
             dct['name'] = name
        name = dct['name']

        # circuit definition are cached
        if name in Cache:
            #print(name, 'cached')
            return Cache[name]

        self = CircuitKind.__new__(metacls, name, bases, dct)
        Cache[name] = self

        self.orientation = 'vertical'
        self.alignment = 1

        self.verilog = None
        self.verilogLib = None

        self.instances = []

        if hasattr(self, 'IO'):
            # instantiate interface
            self.interface = self.IO(defn=self)
            setports(self, self.interface.ports)

            # create circuit definition
            if hasattr(self, 'definition'):
                 pushDefinition(self)
                 self.definition()
                 EndCircuit()

        return self

    # 
    # place a circuit instance in this definition
    #
    def place(cls, inst):
        if not inst.name:
            inst.defn = cls
            inst.name = 'inst' + str(len(cls.instances))
            # osnr's suggested name
            #inst.name = 'inst' + str(len(cls.instances)) + '_' + inst.__class__.name
            #print('naming circuit instance', inst.name)
        #print('placing', inst, 'in', cls)
        inst.stack = inspect.stack()
        cls.instances.append(inst)


    def setlayout(cls, orientation='vertical', alignment=1):
        cls.orientation = orientation
        cls.alignment = alignment

    def getarea(cls):
        x = 0
        z = 0
        for inst in cls.instances:
            clsinst = type(inst)
            dx, dz = clsinst.getarea()
            z = (z+clsinst.alignment-1)/clsinst.alignment
            if   cls.orientation == 'vertical':
                x = max(x, dx)
                z += dz
            elif cls.orientation == 'horizontal':
                x += dx
                z = max(z, dz)
        return (x,z)

    def layout(cls, x=0, y=0):
        orientation = cls.orientation
        alignment = cls.alignment
        z = 0
        for inst in cls.instances:
            clsinst = type(inst)
            dx, dz = clsinst.getarea()
            z = (z+alignment-1)/alignment
            print('placing', inst, 'at', x, y+z/8, z%8)
            inst.loc = (x, y+z/8, z%8)
            if   orientation == 'vertical':
                z += dz
            elif orientation == 'horizontal':
                x += dx

@six.add_metaclass(DefineCircuitKind)
class Circuit(CircuitType):
    pass


# DefineCircuit Factory
def DefineCircuit(name, *decl, **args):
    global currentDefinition
    if currentDefinition:
        currentDefinitionStack.append(currentDefinition)

    dct = dict(IO=decl,
               orientation=args.get('orientation', 'vertical'), 
               alignment=args.get('alignment', 1),
               primitive=args.get('primitive', False),
               stateful=args.get('stateful', False),
               simulate=args.get('simulate'))

    currentDefinition = DefineCircuitKind( name, (Circuit,), dct)
    return currentDefinition

def EndCircuit():
    popDefinition()

def CopyInstance(instance):
    circuit = type(instance)
    new_instance = circuit()
    new_instance.kwargs = instance.kwargs
    return new_instance

if __name__ == '__main__':
    from magma.bit import Bit
    C0 = DeclareCircuit("C", "a", In(Bit), "b", Out(Bit))
    print(C0)
    c0 = C0()
    print(c0)
