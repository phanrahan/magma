from .backend.coreir_ import CoreIRBackend
from .circuit import Circuit
from magma import cache_definition

@cache_definition
def DefineModuleWrapper(cirb: CoreIRBackend, coreirModule):
    class ModuleWrapper(Circuit):
        name = coreirModule.name
        IO = cirb.get_ports_as_list(cirb.get_ports(coreirModule.type))
        wrappedModule = coreirModule
    return ModuleWrapper

def ModuleFromGeneratorWrapper(cirb: CoreIRBackend, namespace: str, generator: str,
                               dependentNamespaces: list, genargs = {}, modargs = {}):
    moduleToWrap = cirb.context.import_generator(namespace,generator)(**genargs)
    cirb.context.run_passes(["rungenerators"], [namespace] + dependentNamespaces)
    return DefineModuleWrapper(cirb, moduleToWrap)(**modargs)