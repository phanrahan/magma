from collections import OrderedDict
from ..bit import Bit, Digital
from ..array import Array
from magma.passes.clock import drive_undriven_clock_types_in_inst
from ..compiler import make_compiler
from .verilog import find

def get_type(port):
    if isinstance(port, Array):
        width = port.N
    else:
        assert isinstance(port, Bit)
        width = 1
    return "UInt<{}>".format(width)

def get_name(port):
    if isinstance(port, Digital) and port.const():
        return ("UInt<1>(\"h1\")"
                if port is type(port).VCC
                else "UInt<1>(\"h0\")")

    if isinstance(port, Array):
        if not port.iswhole():
            # the sequence of values is concantenated
            port = [get_name(i) for i in port.ts]
            port.reverse()
            if len(port) == 1:  # FIXME: Hack to make single length bit arrays work
                return port[0]
            return '{' + ','.join(port) + '}'
    assert not port.anon()
    return port.name.qualifiedname(sep="_")

def compileinstance(instance):
    instance_name = str(instance.name)
    s = "inst {} of {}\n".format(instance_name, str(instance.__class__.__name__))
    for name, port in instance.interface.ports.items():
        if port.is_input():
            value = port.value()
            if not value:
                print('Warning (firrtl): input', str(port), 'not connected to an output')
                value = port
        else:
            value = port
        # if isinstance(value, Array):
        #     for index, subport in enumerate(value.ts):
        #         s += "{}.{}[{}] <= {}\n".format(instance_name, name, index, get_name(subport))
        # else:
        value_name = get_name(value)
        if port.is_input():
            s += "{}.{} <= {}\n".format(instance_name, name, value_name)
        else:
            s += "{} <= {}.{}\n".format(value_name, instance_name, name)
    return s


def compile_primitive(instance):
    op = instance.firrtl_op
    instance_name = str(instance.name)
    # s = "inst {} of {}\n".format(instance_name, str(instance.__class__.__name__))
    outputs = instance.interface.outputs()
    assert len(outputs) == 1, "FIRRTL primitive should only have one output"
    port = outputs[0]
    args = []
    for name, port in instance.interface.ports.items():
        if port.is_input():
            value = port.value()
            if not value:
                print('Warning (firrtl): input', str(port), 'not connected to an output')
                value = port
            args.append(get_name(value))
    return "{} <= {}({})\n".format(get_name(port), instance.firrtl_op, ", ".join(args))

def compiledefinition(cls):

    # for now only allow Bit or Array(n, Bit)
    for name, port in cls.interface.ports.items():
        if isinstance(port, ArrayKind):
            if not isinstance(port.T, BitKind):
                print('Error: Argument', port, 'must be a an Array(n,Bit)')

    s = 'module {} :\n'.format(cls.__name__)
    for name, port in cls.interface.ports.items():
        if port.is_input():
            direction = "output"
        elif port.is_output():
            direction = "input"
        else:
            raise NotImplementedError()  # Does FIRRTL have an inout?
        s += '{} {} : {}\n'.format(direction, name, get_type(port))
    s += "\n"  # Newline after port declaration for readability

    import re
    if cls.firrtl:
        s += cls.firrtl + '\n'
    else:
        # declare a wire for each instance output
        for instance in cls.instances:
            for port in instance.interface.ports.values():
                if port.is_output():
                    s += 'wire {} : {}\n'.format(get_name(port), get_type(port))

        #print('compile instances')
        # emit the structured verilog for each instance
        for instance in cls.instances:
            if getattr(instance, "firrtl_op", False):
                s += compile_primitive(instance)
            else:
                drive_undriven_clock_types_in_inst(cls, instance)
                s += compileinstance(instance)

        # assign to module output arguments
        for input in cls.interface.inputs():
            output = input.value()
            if output:
                iname = get_name(input)
                oname = get_name(output)
                s += '%s <= %s\n' % (iname, oname)

    return "\n  ".join(s.splitlines())


def compile(main):
    defn = find(main,OrderedDict())

    code = 'circuit main :\n'
    for k, v in defn.items():
         print('compiling', k)
         code += "  " + "\n  ".join(compiledefinition(v).splitlines()) + '\n'
    return code


FirrtlCompiler = make_compiler("fir", compile)
