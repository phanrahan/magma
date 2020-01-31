from mako.template import Template
from ..circuit import DeclareCircuit, DefineCircuit, EndDefine
from ..common import deprecated
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
__all__ += ['declare_from_verilog']
__all__ += ['declare_from_verilog_file']
__all__ += ['define_from_verilog']
__all__ += ['define_from_verilog_file']


def _from_verilog(source, func, type_map, target_modules=None, shallow=False,
                  external_modules={}, param_map={}):
    importer = PyverilogImporter(type_map, external_modules, shallow)
    mode = ImportMode.DECLARE if func is DeclareCircuit else ImportMode.DEFINE
    importer.import_(source, mode)
    return importer._magma_modules


def _from_verilog_file(file, func, type_map, target_modules=None, shallow=False,
                       external_modules={}, param_map={}):
    if file is None:
        return None
    with open(file) as f:
        verilog = f.read()
    circuits = _from_verilog(verilog, func, type_map, target_modules, shallow,
                             external_modules, param_map=param_map)
    # Store the original verilog file name, currently used by m.compile to
    # generate a .sv when compiling a circuit that was defined from a verilog
    # file
    for circuit in circuits:
        circuit.verilog_file_name = file
    return circuits


def declare_from_verilog(source, type_map={}, param_map={}):
    return _from_verilog(source, DeclareCircuit, type_map, param_map=param_map)


def declare_from_verilog_file(file, target_modules=None, type_map={},
                              param_map={}):
    return _from_verilog_file(file, DeclareCircuit, type_map, target_modules,
                              param_map=param_map)


def define_from_verilog(source, type_map={}, target_modules=None, shallow=False,
                        external_modules={}, param_map={}):
    return _from_verilog(source, DefineCircuit, type_map, target_modules,
                         shallow=shallow, external_modules=external_modules,
                         param_map=param_map)


def define_from_verilog_file(file, target_modules=None, type_map={},
                             shallow=False, external_modules={}, param_map={}):
    return _from_verilog_file(file, DefineCircuit, type_map, target_modules,
                              shallow=shallow,
                              external_modules=external_modules,
                              param_map=param_map)


# The following functions call their analagous functions above, formatted as
# snake_case rathern than CamelCase. These functions are marked as deprecated.
@deprecated(msg="Use _from_verilog instead")
def FromVerilog(*args, **kwargs):
    return _from_verilog(*args, **kwargs)


@deprecated(msg="Use _from_verilog_file instead")
def FromVerilogFile(*args, **kwargs):
    return _from_verilog_file(*args, **kwargs)


@deprecated(msg="Use declare_from_verilog instead")
def DeclareFromVerilog(*args, **kwargs):
    return declare_from_verilog(*args, **kwargs)


@deprecated(msg="Use declare_from_verilog_file instead")
def DeclareFromVerilogFile(*args, **kwargs):
    return declare_from_verilog_file(*args, **kwargs)


@deprecated(msg="Use define_from_verilog instead")
def DefineFromVerilog(*args, **kwargs):
    return define_from_verilog(*args, **kwargs)


@deprecated(msg="Use define_from_verilog_file instead")
def DefineFromVerilogFile(*args, **kwargs):
    return define_from_verilog_file(*args, **kwargs)


# The functions (Declare|Define)FromTemplatedVerilog(|File) are now deprecated.
@deprecated
def FromTemplatedVerilog(templatedverilog, func, type_map, **kwargs):
    verilog = Template(templatedverilog).render(**kwargs)
    return FromVerilog(verilog, func, type_map)


@deprecated
def FromTemplatedVerilogFile(file, func, type_map, **kwargs):
    if file is None:
        return None
    templatedverilog = open(file).read()
    return FromTemplatedVerilog(templatedverilog, func, type_map, **kwargs)


@deprecated
def DeclareFromTemplatedVerilog(source, type_map={}, **kwargs):
    return FromTemplatedVerilog(source, DeclareCircuit, type_map, **kwargs)


@deprecated
def DeclareFromTemplatedVerilogFile(file, type_map={}, **kwargs):
    return FromTemplatedVerilogFile(file, DeclareCircuit, type_map, **kwargs)


@deprecated
def DefineFromTemplatedVerilog(source, type_map={}, **kwargs):
    return FromTemplatedVerilog(source, DefineCircuit, type_map, **kwargs)


@deprecated
def DefineFromTemplatedVerilogFile(file, type_map={}, **kwargs):
    return FromTemplatedVerilogFile(file, DefineCircuit, type_map, **kwargs)
