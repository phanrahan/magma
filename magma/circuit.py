import sys
import six
import inspect
from functools import wraps
if sys.version_info > (3, 0):
    from functools import reduce
from . import cache_definition
import operator
from collections import namedtuple, Counter
from .interface import *
from .wire import *
from .t import Flip
from .array import ArrayType
from .tuple import TupleType
from .bit import VCC, GND
from .debug import get_callee_frame_info, debug_info
from .logging import warning
from .port import report_wiring_warning
from .is_definition import isdefinition


__all__  = ['AnonymousCircuitType']
__all__ += ['AnonymousCircuit']

__all__ += ['CircuitType']
__all__ += ['Circuit']
__all__ += ['DeclareCircuit']
__all__ += ['DefineCircuit', 'EndDefine', 'EndCircuit']
__all__ += ['getCurrentDefinition']

__all__ += ['CopyInstance']
__all__ += ['circuit_type_method']
__all__ += ['circuit_generator']


circuit_type_method = namedtuple('circuit_type_method', ['name', 'definition'])


def circuit_to_html(cls):
    if isdefinition(cls):
        # Avoid circular dependency so dot backend can use passes
        from .backend.dot import to_html
        return to_html(cls)
    else:
        return repr(cls)

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
        #print('CircuitKind new:', name)

        # override circuit class name
        if 'name' not in dct:
            dct['name'] = name
        name = dct['name']

        if 'renamed_ports' not in dct:
            dct['renamed_ports'] = {}

        if 'primitive' not in dct:
            dct['primitive'] = False

        if 'coreir_lib' not in dct:
            dct['coreir_lib'] = "global"
        if "debug_info" not in dct:
            callee_frame = inspect.getframeinfo(inspect.currentframe().f_back.f_back)
            module = inspect.getmodule(inspect.stack()[2][0])
            dct["debug_info"] = debug_info(callee_frame.filename,
                                           callee_frame.lineno, module)

        # create a new circuit class
        cls = type.__new__(metacls, name, bases, dct)

        for method in dct.get('circuit_type_methods', []):
            setattr(cls, method.name, method.definition)

        # create interface for this circuit class
        if hasattr(cls, 'IO') and not isinstance(cls.IO, InterfaceKind):
            # turn IO attribite into an Interface
            cls.IO = DeclareInterface(*cls.IO)
            cls.interface = cls.IO

        return cls

    def __call__(cls, *largs, **kwargs):
        #print('CircuitKind call:', largs, kwargs)
        debug_info = get_callee_frame_info()
        self = super(CircuitKind, cls).__call__(*largs, **kwargs)
        self.set_debug_info(debug_info)

        # instance interface for this instance
        if hasattr(cls, 'IO'):
            self.setinterface(cls.IO(inst=self, renamed_ports=cls.renamed_ports))

        return self

    def __str__(cls):
        interface = ""
        if hasattr(cls, "interface"):
            interface = ", ".join(f"{name}: {_type}" for name, _type in cls.interface.items())
            interface = f"({interface})"
        return f"{cls.__name__}{interface}"

    def __repr__(cls):
        name = cls.__name__
        args = str(cls.IO)
        if hasattr(cls,"instances"):
            s = '{} = DefineCircuit("{}", {})\n'.format(name, name, args)

            # emit instances
            for instance in cls.instances:
                s += repr(instance) + '\n'

            # emit wires from instances
            for instance in cls.instances:
                s += repr(instance.interface)

            # for input in cls.interface.inputs():
            s += repr( cls.interface )

            s += "EndCircuit()"
        else:
            s = '{} = DeclareCircuit("{}", {})'.format(name, name, args)

        return s

    def _repr_html_(cls):
        return circuit_to_html(cls)

    def rename(cls, new_name):
        old_name = cls.name
        cls.name = new_name
        cls.coreir_name = new_name
        cls.verilog_name = new_name
        cls.__name__ = new_name

        # NOTE(rsetaluri): This is a very hacky way to try to rename wrapped
        # verilog. We simply replace the first instance of "module <old_name>"
        # with "module <new_name>". This ignores the possibility of "module
        # <new_name>" existing anywhere else, most likely in comments etc. The
        # more robust way to do this would to modify the AST directly and
        # generate the new verilog code.
        if cls.verilogFile:
            find_str = f"module {old_name}"
            replace_str = f"module {new_name}"
            assert cls.verilogFile.find(find_str) != -1
            cls.verilogFile = cls.verilogFile.replace(find_str, replace_str, 1)

    def find(cls, defn):
        name = cls.__name__
        if not isdefinition(cls):
            return defn
        for i in cls.instances:
            type(i).find(defn)
        if name not in defn:
            defn[name] = cls
        return defn

#
# Abstract base class for circuits
#
@six.add_metaclass(CircuitKind)
class AnonymousCircuitType(object):

    def __init__(self, *largs, **kwargs):

        self.kwargs = kwargs
        if hasattr(self, 'default_kwargs'):
            for key in self.default_kwargs:
                if key not in kwargs:
                    self.kwargs[key] = self.default_kwargs[key]

        self.name = kwargs['name'] if 'name' in kwargs else ""

        self.loc = kwargs['loc'] if 'loc' in kwargs else None
        if self.loc and len(self.loc) == 2:
            self.loc = (self.loc[0], self.loc[1], 0)

        self.interface = None
        self.defn = None
        self.used = False
        self.is_instance = True

        self.debug_info = None

    def set_debug_info(self, debug_info):
        self.debug_info = debug_info

    def __str__(self):
        if self.name:
            return f"{self.name}<{type(self)}>"
        else:
            name = f"AnonymousCircuitInst{id(self)}"
            interface = ""
            interface = ", ".join(f"{name}: {type(value)}" for name, value in self.interface.ports.items())
            return f"{name}<{interface}>"

    def __repr__(self):
        args = []
        for k, v in self.interface.ports.items():
            args.append('"{}"'.format(k))
            args.append(repr(v))
        if self.name:
            return '{} = {}({})'.format(self.name, type(self).__name__, ', '.join(args))
        else:
            return '{}({})'.format(type(self).__name__, ', '.join(args))

        #return '{} = {}({})  # {} {}'.format(str(self), str(type(self)),
        #    ', '.join(args), self.filename, self.lineno)

    def _repr_html_(self):
        return circuit_to_html(self)

    def __getitem__(self, key):
        return self.interface[key]

    # wire a list of outputs to the circuit's inputs
    def wireoutputs(self, outputs, debug_info):
        inputs = self.interface.inputs()
        ni = len(inputs)
        no = len(outputs)
        if ni != no:
            report_wiring_warning(f"Number of inputs is not equal to the number of outputs, expected {ni} inputs, got {no}. Only {min(ni,no)} will be wired.",  # noqa
                    debug_info)
        for i in range(min(ni,no)):
            wire(outputs[i], inputs[i], debug_info)

    # wire a single output to the circuit's inputs
    def wire(self, output, debug_info):

        if hasattr(output, 'interface'):
            # wire the circuit's outputs to this circuit's inputs
            self.wireoutputs(output.interface.outputs(), debug_info)
        else:
            # wire the output to this circuit's input (should only have 1 input)
            inputs = self.interface.inputs()
            ni = len(inputs)
            if ni == 0:
                report_wiring_warning("Wiring an output to a circuit with no input arguments, skipping", debug_info)
                return
            if ni != 1:
                report_wiring_warning(f"Wiring an output to a circuit with more than one input argument, using the first input {inputs[0].debug_name}", debug_info)
            inputs[0].wire( output, debug_info )


    @property
    def debug_name(self):
        defn_str = ""
        if hasattr(self, 'defn') and self.defn is not None:
            defn_str = str(self.defn.name)
        return f"{defn_str}.{self.name}"

    def __call__(input, *outputs, **kw):
        debug_info = get_callee_frame_info()

        no = len(outputs)
        if len(outputs) == 1:
            input.wire(outputs[0], debug_info)
        elif len(outputs) >= 1:  # In case there are only kw
            input.wireoutputs(outputs, debug_info)

        # wire up extra arguments, name to name
        #
        # this code should be changed to use clock types ...
        #
        for key, value in kw.items():
            if key == 'enable': key = 'CE'
            if key == 'reset':  key = 'RESET'
            if key == 'set':    key = 'SET' # NYI
            if key == 'ce':     key = 'CE'  # depreciated
            if hasattr(input, key):
                i = getattr(input, key)
                wire( value, getattr(input, key), debug_info)
            else:
                report_wiring_warning('Instance {} does not have input {}'.format(input.debug_name, key), debug_info)

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

#
# AnonymousCircuits are like macros - the circuit instances are not placed
#
def AnonymousCircuit(*decl):
    if len(decl) == 1:
        decl = decl[0]
    return AnonymousCircuitType().setinterface(Interface(decl))


#
# Placed circuit - instances placed in a definition
#
class CircuitType(AnonymousCircuitType):
    def __init__(self, *largs, **kwargs):
        super(CircuitType, self).__init__(*largs, **kwargs)

        # Circuit instances are placed if within a definition
        global currentDefinition
        if currentDefinition:
             currentDefinition.place(self)

    def __repr__(self):
        args = []
        for k, v in self.kwargs.items():
            if isinstance(v, tuple):
                 # {   # Format identifier
                 # 0:  # first parameter
                 # #   # use "0x" prefix
                 # 0   # fill with zeroes
                 # {1} # to a length of n characters (including 0x), defined by the second parameter
                 # x   # hexadecimal number, using lowercase letters for a-f
                 # }   # End of format identifier
                 if len(v) == 2:
                     v = "{0:#0{1}x}".format(v[0], v[1] // 4)
            else:
                 v = '"{}"'.format(v)
            args.append("%s=%s"%(k, v))
        if self.name:
            return '{} = {}({})'.format(self.name, type(self).__name__, ', '.join(args))
        else:
            return '{}({})'.format(type(self).__name__, ', '.join(args))

        #return '{} = {}({})  # {} {}'.format(str(self), str(type(self)),
        # cls.filename, cls.lineno)

# DeclareCircuit Factory
def DeclareCircuit(name, *decl, **args):
    debug_info = get_callee_frame_info()
    dct = dict(
        IO=decl,
        debug_info=debug_info,
        is_definition=False,
        primitive=args.get('primitive', True),
        stateful=args.get('stateful', False),
        simulate=args.get('simulate'),
        firrtl_op=args.get('firrtl_op'),
        circuit_type_methods=args.get('circuit_type_methods', []),
        coreir_lib=args.get('coreir_lib', "global"),
        coreir_name=args.get('coreir_name', name),
        coreir_genargs=args.get('coreir_genargs', None),
        coreir_configargs=args.get('coreir_configargs', {}),
        verilog_name=args.get('verilog_name', name),
        default_kwargs=args.get('default_kwargs', {}),
        renamed_ports=args.get('renamed_ports', {})
    )
    return CircuitKind( name, (CircuitType,), dct )



# Maintain a current definition and stack of nested definitions

currentDefinition = None
currentDefinitionStack = []

def getCurrentDefinition():
    global currentDefinition
    return currentDefinition

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

class DefineCircuitKind(CircuitKind):
    def __new__(metacls, name, bases, dct):

        if 'name' not in dct:
            # Check if we are a subclass of something other than Circuit
            for base in bases:
                if base is not Circuit:
                    if not issubclass(base, Circuit):
                        raise Exception("Must subclass from Circuit or a "
                                "subclass of Circuit. {}".format(base))
                    # If so, we will inherit the name of the first parent
                    dct['name'] = base.name
                    break
            else:
                dct['name'] = name
        name = dct['name']
        dct["renamed_ports"] = dct.get("renamed_ports", {})

        self = CircuitKind.__new__(metacls, name, bases, dct)

        self.verilog = None
        self.verilogFile = None
        self.verilogLib = None

        self.verilog_name = dct.get('verilog_name', name)
        self.coreir_name = dct.get('coreir_name', name)
        self.coreir_genargs = dct.get('coreir_genargs', None)
        self.coreir_configargs = dct.get('coreir_configargs', {})
        self.default_kwargs = dct.get('default_kwargs', {})

        self.firrtl = None

        self._instances = []
        self.instanced_circuits_counter = Counter()
        self._is_definition = dct.get('is_definition', False)
        self.is_instance = False

        if hasattr(self, 'IO'):
            # instantiate interface
            self.interface = self.IO(defn=self, renamed_ports=dct["renamed_ports"])
            setports(self, self.interface.ports)

            # create circuit definition
            if hasattr(self, 'definition'):
                 pushDefinition(self)
                 self.definition()
                 self._is_definition = True
                 EndCircuit()

        return self

    @property
    def is_definition(self):
        return self._is_definition or self.verilog or self.verilogFile

    @property
    def instances(self):
        return self._instances

    #
    # place a circuit instance in this definition
    #
    def place(cls, inst):
        if not inst.name:
            inst.name = f"{type(inst).name}_inst{str(cls.instanced_circuits_counter[type(inst).name])}"
            cls.instanced_circuits_counter[type(inst).name] += 1
        inst.defn = cls
        inst.stack = inspect.stack()
        cls.instances.append(inst)


# Register graphviz repr if running in IPython.
# There's a bug in IPython which breaks visual reprs
# on types.
try:
    ip = get_ipython()
    html_formatter = ip.display_formatter.formatters['text/html']
    html_formatter.for_type(DefineCircuitKind, circuit_to_html)
    html_formatter.for_type(CircuitKind, circuit_to_html)
except NameError:
    # Not running in IPython right now?
    pass


@six.add_metaclass(DefineCircuitKind)
class Circuit(CircuitType):
    pass


# DefineCircuit Factory
def DefineCircuit(name, *decl, **args):
    debug_info = get_callee_frame_info()
    global currentDefinition
    if currentDefinition:
        currentDefinitionStack.append(currentDefinition)

    dct = dict(IO             = decl,
               is_definition  = True,
               primitive      = args.get('primitive', False),
               stateful       = args.get('stateful', False),
               simulate       = args.get('simulate'),
               debug_info     = debug_info,
               verilog_name   = args.get('verilog_name', name),
               coreir_name    = args.get('coreir_name', name),
               coreir_lib     = args.get('coreir_lib', "global"),
               coreir_genargs = args.get('coreir_genargs', None),
               coreir_configargs = args.get('coreir_configargs', None),
               default_kwargs = args.get('default_kwargs', {}),
               renamed_ports = args.get('renamed_ports', {}))

    currentDefinition = DefineCircuitKind( name, (Circuit,), dct)
    return currentDefinition

def EndDefine():
    if currentDefinition:
        debug_info = get_callee_frame_info()
        currentDefinition.end_circuit_filename = debug_info[0]
        currentDefinition.end_circuit_lineno   = debug_info[1]
        popDefinition()
    else:
        raise Exception("EndDefine called without Define/DeclareCircuit")

EndCircuit = EndDefine

def CopyInstance(instance):
    circuit = type(instance)
    new_instance = circuit()
    new_instance.kwargs = instance.kwargs
    return new_instance

def hex(i):
    if i < 10: return chr(ord('0')+i)
    else:      return chr(ord('A')+i-10)


def hstr(init, nbits):
    bits = 1 << int(nbits)
    format = "0x"
    nformat = []
    for i in range(bits//4):
        nformat.append(init%16)
        init //= 16
    nformat.reverse()
    if nformat:
        return format + reduce(operator.add, map(hex, nformat))
    return format


GeneratorArguments = namedtuple('GeneratorArguments', ['args', 'kwargs'])


def circuit_generator(func):
    @cache_definition
    @wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        # Store arguments to generate the circuit
        result._generator_arguments = GeneratorArguments(args, kwargs)
        return result
    return wrapped

from magma.syntax.combinational import combinational
from magma.syntax.sequential import sequential
