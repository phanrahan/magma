from .backend.coreir_ import CoreIRBackend
from coreir.type import Record
from .circuit import Circuit

@cache_definition
def DefineModuleWrapper(cirb: CoreIRBackend, coreirModule):
    class ModuleWrapper(Circuit):
        # since no defintion, just declaration, magma won't try to inspect
        # as long as it has an IO and name objects, can conncet it, but won't analyze this
        # if this doesn't work, try declarecircuti with no class
        # readline crashing is a bug, report that
        name = coreirModule.name
        IO = cirb.get_ports_as_list(cirb.get_ports(coreirModule.type))
        wrappingModule = coreirModule
        # convert IO to list
        #args = Record(coreirModule.type.ptr, cirb.context)
        #argsNames = [k for (k, _) in list(args)]
