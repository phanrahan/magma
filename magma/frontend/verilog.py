from __future__ import absolute_import
from __future__ import print_function
import warnings

from mako.template import Template

from ..circuit import DeclareCircuit, DefineCircuit, EndDefine


from ..logging import root_logger
from .pyverilog_utils import *

_logger = root_logger().getChild('from_verilog')


__all__  = ['DeclareFromVerilog']
__all__ += ['DeclareFromVerilogFile']
__all__ += ['DeclareFromTemplatedVerilog']
__all__ += ['DeclareFromTemplatedVerilogFile']
__all__ += ['DefineFromVerilog']
__all__ += ['DefineFromVerilogFile']
__all__ += ['DefineFromTemplatedVerilog']
__all__ += ['DefineFromTemplatedVerilogFile']


def ParseVerilogModule(node, type_map):
    args = []
    ports = []

    param_map = {}
    for param in node.paramlist.params:
        for p in param.list:
            param_map[p.name] = get_value(p.value, param_map)

    for port in node.portlist.ports:
        if isinstance(port, Ioport):
            io = port.first
            args.append(io.name)
            args.append(get_type(io, type_map, param_map))
        elif isinstance(port, Port):
            ports.append(port.name)
        else:
            raise NotImplementedError(type(port))

    if ports:
        assert not args, "Can we have mixed declared and undeclared types in a Verilog module?"
        for port in ports:
            found = False
            for child in node.children():
                if isinstance(child, Decl):
                    for sub_child in child.children():
                        if isinstance(sub_child, (parser.Input, parser.Output, parser.Inout)) and \
                                sub_child.name == port:
                            args.append(sub_child.name)
                            args.append(get_type(sub_child, type_map, param_map))
                            found = True
                            break
                if found:
                    break
            else:
                raise Exception(f"Could not find type declaration for port {port}")
    for child in node.children():
        if isinstance(child, Decl):
            for sub_child in child.children():
                if isinstance(sub_child, parser.Parameter):
                    param_map[sub_child.name] = get_value(sub_child.value, param_map)

    return node.name, args, param_map


def FromVerilog(source, func, type_map, target_modules=None, shallow=False,
                external_modules={}, param_map={}):
    if param_map:
        warnings.warn("param_map keyword parameter for verilog import is no "
                      "longer required, magma will infer the parameters "
                      "instead", DeprecationWarning)

    parser = VerilogParser()
    ast = parser.parse(source)
    visitor = ModuleVisitor(shallow)
    visitor.visit(ast)
    if not shallow:
        visitor.sort()

    def _get_lines(start_line, end_line):
        if shallow:
            return source
        lines = source.split("\n")
        return "\n".join(lines[start_line - 1:end_line])

    if not external_modules.keys().isdisjoint(visitor.defns.keys()):
        intersection = external_modules.keys() & visitor.defns.keys()
        raise Exception(f"Modules defined in both external_modules and in "
                        f"parsed verilog: {intersection}")
    magma_defns = external_modules.copy()
    for name, verilog_defn in visitor.defns.items():
        parsed_name, args, default_params = ParseVerilogModule(verilog_defn,
                                                               type_map)
        assert parsed_name == name
        magma_defn = func(name, *args)
        magma_defn.coreir_config_param_types = {key: type(value) for key, value
                                                in default_params.items()}
        magma_defn.default_kwargs = default_params
        if func == DefineCircuit:
            # Attach relevant lines of verilog source.
            magma_defn.verilogFile = _get_lines(
                verilog_defn.lineno, verilog_defn.end_lineno)
            if not shallow:
                for instance in visitor.get_instances(verilog_defn):
                    instance_defn = magma_defns[instance.module]
                    instance_defn()
            EndDefine()
        magma_defn.verilog_source = source
        magma_defns[name] = magma_defn

    if len(magma_defns) == 0:
        _logger.warning(f"Did not import any modules from verilog, either "
                        f"could not parse or could not find any of the "
                        f"target_modules ({target_modules})")
    # Filter back out external modules.
    magma_defns = {name : magma_defns[name] for name in visitor.defns}
    if target_modules is None:
        return list(magma_defns.values())
    # Filter modules based on target_modules list.
    return [v for k, v in magma_defns.items() if k in target_modules]

def FromVerilogFile(file, func, type_map, target_modules=None, shallow=False,
                    external_modules={}, param_map={}):
    if file is None:
        return None
    verilog = open(file).read()
    result = FromVerilog(verilog, func, type_map, target_modules, shallow,
                         external_modules, param_map=param_map)
    # Store the original verilog file name, currently used by m.compile to
    # generate a .sv when compiling a circuit that was defined from a verilog
    # file
    for item in result:
        item.verilog_file_name = file
    return result

def FromTemplatedVerilog(templatedverilog, func, type_map, **kwargs):
    verilog = Template(templatedverilog).render(**kwargs)
    return FromVerilog(verilog, func, type_map)

def FromTemplatedVerilogFile(file, func, type_map, **kwargs):
    if file is None:
        return None
    templatedverilog = open(file).read()
    return FromTemplatedVerilog(templatedverilog, func, type_map, **kwargs)


def DeclareFromVerilog(source, type_map={}, param_map={}):
    return FromVerilog(source, DeclareCircuit, type_map, param_map=param_map)

def DeclareFromVerilogFile(file, target_modules=None, type_map={}, param_map={}):
    return FromVerilogFile(file, DeclareCircuit, type_map, target_modules, param_map=param_map)

def DeclareFromTemplatedVerilog(source, type_map={}, **kwargs):
    return FromTemplatedVerilog(source, DeclareCircuit, type_map, **kwargs)

def DeclareFromTemplatedVerilogFile(file, type_map={}, **kwargs):
    return FromTemplatedVerilogFile(file, DeclareCircuit, type_map, **kwargs)


def DefineFromVerilog(source, type_map={}, target_modules=None, shallow=False,
                      external_modules={}, param_map={}):
    return FromVerilog(source, DefineCircuit, type_map, target_modules,
                       shallow=shallow, external_modules=external_modules,
                       param_map=param_map)

def DefineFromVerilogFile(file, target_modules=None, type_map={},
                          shallow=False, external_modules={}, param_map={}):
    return FromVerilogFile(file, DefineCircuit, type_map, target_modules,
                           shallow=shallow, external_modules=external_modules,
                           param_map=param_map)

def DefineFromTemplatedVerilog(source, type_map={}, **kwargs):
    return FromTemplatedVerilog(source, DefineCircuit, type_map, **kwargs)

def DefineFromTemplatedVerilogFile(file, type_map={}, **kwargs):
    return FromTemplatedVerilogFile(file, DefineCircuit, type_map, **kwargs)
