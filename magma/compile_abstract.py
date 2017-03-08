from collections import OrderedDict
from .port import INPUT, OUTPUT, INOUT
from .circuit import *
from .circuitdefn import *

# COMPILATION_PRIMITIVES: Operations that abstract over the underlying circuit language
COMPILATION_PRIMITIVES = {}
# Operations:
# DECLARE_MODULE(name, module args)
# INLINE_VERILOG_PREAMBLE
# DECLARE_IMPORT_WIRES
# ASSIGN
# FINISH_MODULE

# MODULE_INSTANCE_ARGUMENT(k, v) (like kwargs)
# MODULE_INSTANCE(class, instancename, params, args)

def hierarchy(circuit, indent=0):
    name = indent * ' ' + str(circuit)
    if isinstance(type(circuit), DefineCircuitKind):
        for i in circuit.instances:
            hierarchy(i, indent+2)

def find(circuit, defn):
    name = circuit.__name__
    #print('find', name)
    if not isinstance(circuit, DefineCircuitKind):
        return defn
    for i in circuit.instances:
        find(type(i), defn)
    if name not in defn:
        #print('adding defn',  name)
        defn[name] = circuit
    return defn

def compiledefinitions(file,inst):
    defn = find(inst,OrderedDict())

    text = ''
    for k, v in defn.items():
         text += compiledefinition(v) + '\n'

    open(file,'w').write(text)

def compiledefinition(cls):

    s = COMPILATION_PRIMITIVES["DECLARE_MODULE"](cls.__name__, cls.interface.vmoduleargs())

    if cls.verilog:
        s += COMPILATION_PRIMITIVES["INLINE_VERILOG"](cls.verilog + '\n')

    else:
        # output a wire for each instance output
        for instance in cls.instances:
            for port in instance.interface.ports.values():
                if port.direction == OUTPUT:
                    s += COMPILATION_PRIMITIVES["IMPORT_WIRE"](port.vdecl(), port.lvalue())
    
        # output the structured verilog for all the instances
        for instance in cls.instances:
            # Wire up the clocks
            if hasattr(cls, 'CLK'):
                #print(instance, type(instance).__name__)
                CLK = None
                if   hasattr(instance, 'CLK'):
                    #print('wiring clock to CLK')
                    CLK = instance.CLK
                elif hasattr(instance, 'CLKA'):
                    #print('wiring clock to CLKA')
                    CLK = instance.CLKA
                elif hasattr(instance, 'CLKB'):
                    #print('wiring clock to CLKB')
                    CLK = instance.CLKB
                elif hasattr(instance, 'WCLK'):
                    #print('wiring clock to WCLK')
                    CLK = instance.WCLK
                elif type(instance).__name__ == "FDRSE" and hasattr(instance,'C'):
                    #print('wiring clock to FDRSE')
                    CLK = instance.C
                if CLK and not CLK.wired():
                    #print('wiring clock to', CLK)
                    wire(cls.CLK, CLK)
            s += compileinstance(instance)

        # output assigments to module output arguments
        for port in cls.interface.inputs():
            if port.direction == INOUT:
                print("warning: skipping INOUT assign completely")
                pass
            else:
                s += COMPILATION_PRIMITIVES["ASSIGN"](port.lvalue(), port.value())

    s += COMPILATION_PRIMITIVES["FINISH_MODULE"]()

    return s

def compileinstance(self):

    def arg(k,v):
        if not isinstance(v, str): v = str(v)
        return COMPILATION_PRIMITIVES["INSTANCE_ARGUMENT"](k, v)

    # print("COMPILEINSTANCE", self)

    args = []
    for k, v in self.interface.ports.items():
        #print('arg', k, v)
        w = v.value()
        if w is None:
            print(k, 'not connected')
        else:
            if k[0].isdigit():
                if not isinstance(w, str): w = str(w)
                a = w
            else:
                a = arg(k,w)
            args.append(a)

    params = [arg(k, v) for k, v in self.parameters.items()]

    s = COMPILATION_PRIMITIVES["INSTANCE"](str(self.__class__.__name__), self.name, self.parameters.items(), args)
    return s

def compileucf(file,fpga):
    open(file,'w').write(fpga.ucf())

def compile(filename, main):
    compiledefinitions(filename, main)
    compileucf(filename+'.ucf', main.fpga)
