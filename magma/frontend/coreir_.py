from magma.backend.coreir_ import CoreIRBackend
from magma.circuit import DefineCircuitKind, Circuit, definitionCache
from magma import cache_definition

@cache_definition
def DefineModuleWrapper(cirb: CoreIRBackend, coreirModule, uniqueStrForArgs):
    class ModuleWrapper(Circuit):
        name = coreirModule.name + "_" + uniqueStrForArgs
        IO = cirb.get_ports_as_list(cirb.get_ports(coreirModule.type))
        wrappedModule = coreirModule
    return ModuleWrapper

def DefineCircuitFromGeneratorWrapper(cirb: CoreIRBackend, namespace: str, generator: str,
                                      dependentNamespaces: list, uniqueStrForArgs: str,
                                      genargs: dict = {}):
    moduleToWrap = cirb.context.import_generator(namespace,generator)(**genargs)
    cirb.context.run_passes(["rungenerators"], [namespace] + dependentNamespaces)
    return DefineModuleWrapper(cirb, moduleToWrap, uniqueStrForArgs)

def CircuitInstanceFromGeneratorWrapper(cirb: CoreIRBackend, namespace: str, generator: str,
                                        dependentNamespaces: list, uniqueStrForArgs: str,
                                        genargs: dict = {}, modargs: dict = {}):
    return DefineCircuitFromGeneratorWrapper(cirb, namespace, generator,
                                             dependentNamespaces, uniqueStrForArgs,
                                             genargs)(**modargs)

def GetCoreIRModule(cirb: CoreIRBackend, circuit: DefineCircuitKind):
    """
    Get the CoreIR module corresponding to the Magma circuit or circuit instance

    :param cirb: The CoreIR backend currently be used.
    :param circuit: The magma circuit to get the coreIR backend for
    :return: A CoreIR module
    """
    if (hasattr(circuit, "wrappedModule")):
        return circuit.wrappedModule
    else:
        # if this is an instance, compile the class, as that is the circuit
        if circuit.is_instance:
            circuitNotInstance = circuit.__class__
        else:
            circuitNotInstance = circuit
        return cirb.compile(circuitNotInstance)[circuitNotInstance.name]