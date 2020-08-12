from magma import cache_definition
from magma.backend.coreir_ import CoreIRBackend, CoreIRContextSingleton
from magma.circuit import DefineCircuitKind, Circuit
from magma import cache_definition, Clock, Array, BitIn, BitOut, Product
from coreir.generator import Generator

@cache_definition
def GetCoreIRBackend():
    return CoreIRBackend()

def GetMagmaContext():
    return CoreIRContextSingleton().get_instance()

def ResetCoreIR():
    CoreIRContextSingleton().reset_instance()
    backend = GetCoreIRBackend()
    backend.reset()

_coreirNamedTypeToPortDict = {
    "clk": Clock,
    "coreir.clkIn": Clock
}


def _get_ports_as_list(ports):
    return [item for i in range(len(ports.keys())) for item in
            [list(ports.keys())[i], list(ports.types())[i]]]


def _get_ports(coreir_type, renamed_ports):
    if (coreir_type.kind == "Bit"):
        return BitOut
    elif (coreir_type.kind == "BitIn"):
        return BitIn
    elif (coreir_type.kind == "Array"):
        return Array[len(coreir_type), _get_ports(coreir_type.element_type, renamed_ports)]
    elif (coreir_type.kind == "Record"):
        elements = {}
        for item in coreir_type.items():
            name = item[0]
            # replace  the in port with I as can't reference that
            if name == "in":
                name = "I"
                renamed_ports[name] = "in"
            elements[name] = _get_ports(item[1], renamed_ports)
        return Product.from_fields("anon", elements)
    elif (coreir_type.kind == "Named"):
        # exception to handle clock types, since other named types not handled
        if coreir_type.name in _coreirNamedTypeToPortDict:
            return In(_coreirNamedTypeToPortDict[coreir_type.name])
        else:
            raise NotImplementedError("not all named types supported yet")
    else:
        raise NotImplementedError("Trying to convert unknown coreir type to magma type")


def DefineModuleWrapper(cirb: CoreIRBackend, coreirModule, uniqueName, deps):
    class ModuleWrapper(Circuit):
        name = uniqueName
        renamed_ports = {}
        IO = _get_ports_as_list(_get_ports(coreirModule.type, renamed_ports))
        wrappedModule = coreirModule
        coreir_wrapped_modules_libs_used = set(deps)

        @classmethod
        def definition(cls):
            pass
    return ModuleWrapper

def DefineCircuitFromGeneratorWrapper(cirb: CoreIRBackend, namespace: str, generator: str,
                                      uniqueName: str, dependentNamespaces: list = [],
                                      genargs: dict = {}, runGenerators = True):
    moduleToWrap = cirb.context.import_generator(namespace,generator)(**genargs)

    deps = [namespace] + dependentNamespaces
    if runGenerators:
        cirb.context.run_passes(["rungenerators"], deps)
    print(cirb, cirb.context, cirb.context.context)
    print(moduleToWrap, moduleToWrap.context, moduleToWrap.context.context)
    return DefineModuleWrapper(cirb, moduleToWrap, uniqueName, deps)

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
        backend = GetCoreIRBackend()
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
