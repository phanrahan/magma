from magma.backend.coreir_ import CoreIRBackend
from magma.circuit import Circuit
from magma import cache_definition

@cache_definition
def DefineModuleWrapper(cirb: CoreIRBackend, coreirModule):
    class ModuleWrapper(Circuit):
        name = coreirModule.name
        IO = cirb.get_ports_as_list(cirb.get_ports(coreirModule.type))
        wrappedModule = coreirModule
    return ModuleWrapper

def ModuleFromGeneratorWrapper(cirb: CoreIRBackend, namespace: str, generator: str,
                               dependentNamespaces: list, genargs: dict = {}, modargs: dict = {}):
    moduleToWrap = cirb.context.import_generator(namespace,generator)(**genargs)
    cirb.context.run_passes(["rungenerators"], [namespace] + dependentNamespaces)
    return DefineModuleWrapper(cirb, moduleToWrap)(**modargs)

def GetCoreIRModule(cirb: CoreIRBackend, circuit: Circuit):
    """
    Get the CoreIR module corresponding to the Magma circuit

    :param cirb: The CoreIR backend currently be used.
    :param circuit: The magma circuit to get the coreIR backend for
    :return: A CoreIR module
    """
    if (hasattr(circuit, "wrappedModule")):
        return circuit.wrappedModule
    else:
        return cirb.compile(circuit)[circuit.name]