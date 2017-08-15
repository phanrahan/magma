from collections import OrderedDict
from magma.backend.verilog import find
from magma.array import ArrayKind, ArrayType
from magma.wire import wiredefaultclock
import coreir

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
        assert isinstance(t, BitType)
        return ""

# return the verilog module args


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

    #s = '(* loc="%d,%d/%d" *)\n' % self.loc if self.loc else ""

    s = str(self.__class__.__name__)
    if len(params):
        if len(params) > 2:
            s += ' #(' + ",\n".join(params) + ')'
        else:
            s += ' #(' + ", ".join(params) + ')'
    s += ' ' + str(self.name)

    return '%s (%s)' % (s, ', '.join(args))

def compiledefinition(cls, context, coreir_stdlib):

    # for now only allow Bit or Array(n, Bit)
    for name, port in cls.interface.ports.items():
        if isinstance(port, ArrayKind):
            if not isinstance(port.T, BitKind):
                print('Error: Argument', port, 'must be a an Array(n,Bit)')
                assert True


    args = convert_interface_to_coreir_args(cls.interface)
    s = 'module %s (%s);\n' % (cls.__name__, args)
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


class CoreIRBackend:
    def __init__(self):
        self.context = coreir.Context()
        self.coreir_stdlib = self.context.get_namespace("coreir")

    def check_interface(self, definition):
        # for now only allow Bit or Array(n, Bit)
        for name, port in definition.interface.ports.items():
            if isinstance(port, ArrayKind):
                if not isinstance(port.T, BitKind):
                    error('Error: Argument {} must be a an Array(n,Bit)'.format(port))

    def convert_interface_to_module_type(self, interface):
        args = {}
        for name, port in interface.ports.items():
            # FIXME: Logic taken from verilog backend, why do we flip?
            if port.isinput(): 
                _type = self.context.Bit()
            elif port.isoutput():
                _type = self.context.BitIn()
            else: 
                raise NotImplementedError
            if isinstance(port, ArrayType):
                _type = self.context.Array(port.N, _type)
            args[name] = _type
        return self.context.Record(args)

    def compile_instance(self, instance, module_definition):
        # for key, value in instance.interface.ports.items():
        #     if value.isinput():
        #         # Find the output connected to value
        name = instance.__class__.__name__
        len_prefix = len("coreir_")
        assert "coreir_" == name[:len_prefix]
        instantiable = self.coreir_stdlib.instantiables[name[len_prefix:]]
        if instantiable.kind == coreir.Module:
            return module_definition.add_module_instance(instance.name, instantiable)
        elif instantiable.kind == coreir.Generator:
            gen_args = self.context.newArgs({"width": instance.kwargs["WIDTH"]})
            return module_definition.add_generator_instance(instance.name, instantiable, gen_args)
        else:
            raise NotImplementedError()

    def compile_definition(self, definition):
        self.check_interface(definition)
        module_type = self.convert_interface_to_module_type(definition.interface)
        module = self.context.G.new_module(definition.__name__, module_type)
        module_definition = module.new_definition()
        output_ports = {}
        for name, port in definition.interface.ports.items():
            if port.isoutput():
                output_ports[port] = str(port).replace(definition.__name__, "self")
        for instance in definition.instances:
            wiredefaultclock(definition, instance)
            coreir_instance = self.compile_instance(instance, module_definition)
            for name, port in instance.interface.ports.items():
                if port.isoutput():
                    output_ports[port] = str(port)
        for instance in definition.instances:
            for name, port in instance.interface.ports.items():
                if port.isinput():
                    module_definition.connect(
                        module_definition.select(str(output_ports[port.value()])),
                        module_definition.select(str(port)))
        module.definition = module_definition
        return module

    def compile(self, defn):
        modules = {}
        for key, value in defn.items():
            print('compiling', key)
            modules[key] = self.compile_definition(value)
        return modules

def compile(main, file_name):
    defn = find(main, OrderedDict())
    modules = CoreIRBackend().compile(defn)
    modules[main.__name__].save_to_file(file_name)
