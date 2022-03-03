from mako.template import Template

from magma.circuit import DeclareCircuit, DefineCircuit, EndDefine
from magma.common import deprecated
from magma.config import config, RuntimeConfig
from magma.frontend.dummy_verilog_importer import DummyVerilogImporter
from magma.frontend.verilog_importer import ImportMode


_pyverilog_importer_initialized = False
# We register a runtime configuration for allowing dynamically setting the
# verilog importer. By default, it is set to a dummy importer so that pyverilog
# is only imported on demand.
config._register(verilog_importer=RuntimeConfig(DummyVerilogImporter()))


def _init_pyverilog_importer():
    global _pyverilog_importer_initialized
    if _pyverilog_importer_initialized:
        return
    if not isinstance(config.verilog_importer, DummyVerilogImporter):
        return
    from magma.frontend.pyverilog_importer import PyverilogImporter
    config.verilog_importer = PyverilogImporter({})
    _pyverilog_importer_initialized = True


def _from_verilog(source, func, *, target_modules=None, type_map={}):
    _init_pyverilog_importer()
    importer = config.verilog_importer
    importer.reset(type_map=type_map)
    mode = ImportMode.DECLARE if func is DeclareCircuit else ImportMode.DEFINE
    importer.import_(source, mode)
    modules = importer._magma_modules.copy()
    if target_modules is None:
        return modules

    def _filter(mod):
        return mod.name in target_modules

    return list(filter(_filter, modules))


def _from_verilog_file(file, func, *, target_modules=None, type_map={}):
    if file is None:
        return None
    with open(file) as f:
        verilog = f.read()
    circuits = _from_verilog(verilog, func, target_modules=target_modules,
                             type_map=type_map)
    # Store the original verilog file name, currently used by m.compile to
    # generate a .sv when compiling a circuit that was defined from a verilog
    # file.
    for circuit in circuits:
        circuit.verilog_file_name = file
    return circuits


def set_verilog_importer(importer):
    """Convenience function for setting the runtime verilog importer"""
    config.verilog_importer = importer


def declare_from_verilog(source, *, target_modules=None, type_map={}):
    return _from_verilog(source, DeclareCircuit, target_modules=target_modules,
                         type_map=type_map)


def declare_from_verilog_file(file, *, target_modules=None, type_map={}):
    return _from_verilog_file(file, DeclareCircuit,
                              target_modules=target_modules,
                              type_map=type_map)


def define_from_verilog(source, *, target_modules=None, type_map={}):
    return _from_verilog(source, DefineCircuit,
                         target_modules=target_modules,
                         type_map=type_map)


def define_from_verilog_file(file, *, target_modules=None, type_map={}):
    return _from_verilog_file(file, DefineCircuit,
                              target_modules=target_modules,
                              type_map=type_map)


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
