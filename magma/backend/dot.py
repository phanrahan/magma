from ..array import Array
from ..bit import Bit, Digital
from ..compiler import make_compiler
from ..passes.debug_name import DebugNamePass
from ..passes.clock import WireClockPass
from collections import OrderedDict
from ..logging import root_logger
from graphviz import Digraph
import re


_logger = root_logger()


# Initially based on the firrtl backend.
def escape(s):
    # Escape special characters for graphviz labels.
    return re.sub(r'([<>])', r'\\\1', s)

def get_type(port):
    return str(type(port))

def get_name(dot, port):
    if isinstance(port, Digital) and port.const():
        return "1" if port is type(port).VCC else "0"

    if isinstance(port, Array):
        if not port.iswhole():
            # the sequence of values is concantenated
            port = [get_name(dot, i) for i in port.ts]
            port.reverse()
            if len(port) == 1:  # FIXME: Hack to make single length bit arrays work
                return port[0]
            name = '[' + ','.join(port) + ']'
            dot.node(name, '{{' + '|'.join(port) + '}|}')
            for sub in port:
                dot.edge(sub, name + ':' + sub)
            return name
    assert not port.anon()
    return port.name.qualifiedname(sep="_")

def compileinstance(dot, instance):
    instance_backend_name = str(instance.name)
    instance_cls_name = str(instance.__class__.__name__)

    inputs = []
    outputs = []

    for name, port in instance.interface.ports.items():
        if port.is_input():
            inputs.append('<{0}> {0}'.format(str(name)))
            value = port.value()
            if value is None:
                _logger.warning(f'Input {port.debug_name} not connected to an output')
                continue
        else:
            outputs.append('<{0}> {0}'.format(str(name)))
            value = port
        # if isinstance(value, Array):
        #     for index, subport in enumerate(value.ts):
        #         s += "{}.{}[{}] <= {}\n".format(instance_backend_name, name, index, get_name(subport))
        # else:
        value_name = get_name(dot, value)
        if port.is_input():
            # s += "{}.{} <= {}\n".format(instance_backend_name, name, value_name)
            dot.edge(value_name, '{}:{}'.format(instance_backend_name, name))
        else:
            # s += "{} <= {}.{}\n".format(value_name, instance_backend_name, name)
            dot.edge('{}:{}'.format(instance_backend_name, name), value_name)

    instance_label = '{' + '|'.join(inputs) + '}|'
    if instance.decl is not None:
        instance_label += '{} ({})\\n{}'.format(instance.decl.varname, instance_backend_name, instance_cls_name)
    else:
        instance_label += '{}\\n{}'.format(instance_backend_name, instance_cls_name)

    instance_label += '|{' + '|'.join(outputs) + '}'
    dot.node(instance_backend_name, '{' + instance_label + '}')

def compiledefinition(dot, cls):
    # Each definition maps to an entire self-contained graphviz digraph.

    # for now only allow Bit or Array(n, Bit)
    for name, port in cls.interface.ports.items():
        if isinstance(port, Array):
            if not issubclass(port.T, Bit):
                print('Error: Argument', port, 'must be a an Array(n,Bit)')

    for name, port in cls.interface.ports.items():
        # TODO: Check whether port.is_input() or .is_output().
        dot.node(name,
                 escape('{}\\n{}'.format(name, get_type(port))),
                 shape='ellipse')

    # declare a wire for each instance output
    for instance in cls.instances:
        for port in instance.interface.ports.values():
            if port.is_output():
                dot.node(get_name(dot, port),
                         escape('{}\\n{}'.format(get_name(dot, port), get_type(port))),
                         shape='none')

    # Emit the graph node (with ports) for each instance.
    for instance in cls.instances:
        compileinstance(dot, instance)

    # Assign to module output arguments.
    for input in cls.interface.inputs():
        output = input.value()
        if output is not None:
            iname = get_name(dot, input)
            oname = get_name(dot, output)
            dot.edge(oname, iname)

def find(circuit, defn):
    name = circuit.name
    if not hasattr(circuit, "instances"):
        return defn
    for i in circuit.instances:
        find(type(i), defn)
    if name not in defn:
        defn[name] = circuit
    return defn

def dots(main):
    defn = find(main,OrderedDict())

    dots = []
    for k, v in defn.items():
         # print('compiling', k, v)
         dot = Digraph(k,
                       graph_attr={'label': str(v), 'rankdir': 'LR'},
                       node_attr={'shape': 'record'})
         compiledefinition(dot, v)
         dots.append(dot)

    return dots

def to_html(main):
    DebugNamePass(main).run()
    WireClockPass(main).run()
    return "\n".join([dot._repr_svg_() for dot in dots(main)])

def compile(main):
    DebugNamePass(main).run()
    WireClockPass(main).run()
    return "\n".join([str(dot) for dot in dots(main)]) + '\n'

DotCompiler = make_compiler("dot", compile)
