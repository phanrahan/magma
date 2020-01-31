from mako.template import Template
from ..circuit import DeclareCircuit, DefineCircuit, EndDefine
from ..logging import root_logger
from .pyverilog_importer import PyverilogImporter
from .verilog_importer import ImportMode


_logger = root_logger().getChild('from_verilog')

__all__ = ['DeclareFromVerilog']
__all__ += ['DeclareFromVerilogFile']
__all__ += ['DeclareFromTemplatedVerilog']
__all__ += ['DeclareFromTemplatedVerilogFile']
__all__ += ['DefineFromVerilog']
__all__ += ['DefineFromVerilogFile']
__all__ += ['DefineFromTemplatedVerilog']
__all__ += ['DefineFromTemplatedVerilogFile']


def FromVerilog(source, func, type_map, target_modules=None, shallow=False,
                external_modules={}, param_map={}):
    importer = PyverilogImporter(type_map, external_modules, shallow)
    mode = ImportMode.DECLARE if func is DeclareCircuit else ImportMode.DEFINE
    importer.import_(source, mode)
    return importer._magma_modules


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


def DeclareFromVerilogFile(file, target_modules=None, type_map={},
                           param_map={}):
    return FromVerilogFile(file, DeclareCircuit, type_map, target_modules,
                           param_map=param_map)


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
