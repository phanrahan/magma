from magma.backend.coreir_ import CoreIRBackend
from magma.circuit import DefineCircuitKind, Circuit, definitionCache
from magma import cache_definition
from coreir.generator import Generator

@cache_definition
def DefineModuleWrapper(cirb: CoreIRBackend, coreirModule, uniqueName):
    class ModuleWrapper(Circuit):
        name = uniqueName
        IO = cirb.get_ports_as_list(cirb.get_ports(coreirModule.type))
        wrappedModule = coreirModule

        @classmethod
        def definition(cls):
            pass
    return ModuleWrapper

def DefineCircuitFromGeneratorWrapper(cirb: CoreIRBackend, namespace: str, generator: str,
                                      uniqueName: str, dependentNamespaces: list = [],
                                      genargs: dict = {}, runGenerators = True):
    if uniqueName in definitionCache:
        return definitionCache[uniqueName]
    moduleToWrap = cirb.context.import_generator(namespace,generator)(**genargs)
    if runGenerators:
        cirb.context.run_passes(["rungenerators"], [namespace] + dependentNamespaces)
    return DefineModuleWrapper(cirb, moduleToWrap, uniqueName)

def CircuitInstanceFromGeneratorWrapper(cirb: CoreIRBackend, namespace: str, generator: str,
                                        uniqueName: str, dependentNamespaces: list,
                                        genargs: dict = {}, modargs: dict = {}):
    return DefineCircuitFromGeneratorWrapper(cirb, namespace, generator,
                                             uniqueName, dependentNamespaces,
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
        if hasattr(circuit, 'is_instance') and circuit.is_instance:
            circuitNotInstance = circuit.__class__
        else:
            circuitNotInstance = circuit
        moduleOrGenerator = cirb.compile(circuitNotInstance)[circuitNotInstance.name]
        # compile can giv eme back the coreIR module or the coreIR generator. if this is
        # the CoreIR generator, call it with the Magma arguments converted to CoreIR ones.
        if isinstance(moduleOrGenerator, Generator):
            return moduleOrGenerator(**circuitNotInstance.coreir_genargs)
        else:
            return moduleOrGenerator

def DeclareCoreIRGenerator(lib : str, name : str, typegen = None, backend = None):
    if backend is None:
        backend = CoreIRBackend()
    if typegen is not None:
        # This is for generators which we don't have access to
        raise NotImplementedError()
    else:
        # Assume the generator is available, create a wrapped circuit
        def Define(**kwargs):
            kwargs_str = "_".join(f"{key}_{value}" for key, value in kwargs.items())
            unique_name = f"{lib}_{name}_{kwargs_str}"
            return DefineCircuitFromGeneratorWrapper(backend, lib, name, unique_name, genargs=kwargs, runGenerators=False)
        return Define

def coreir_typegen(fn):
    def wrapped(*args, **kwargs):
        return None
    return wrapped
