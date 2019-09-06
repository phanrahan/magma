from magma import *
import coreir

context = coreir.Context()

def get_lib(lib):
    if lib in {"coreir", "mantle", "corebit", "memory"}:
        return context.get_namespace(lib)
    elif lib == "global":
        return context.global_namespace
    else:
        return context.load_library(lib)

def import_generator(lib, name):
    generator = get_lib(lib).generators[name]
    def _generator(**kwargs):
        return import_circuit(generator(**kwargs))
    return _generator

def to_magma_type(typ):
    if typ.kind == "Array":
        return Array(len(typ), to_magma_type(typ.element_type))
    elif typ.kind == "BitIn":
        return In(Bit)
    elif typ.kind == "Bit":
        return Out(Bit)
    raise ValueError(f"Cannot convert type: {typ.kind}")

def import_circuit(module):
    if not isinstance(module, coreir.Module):
        raise ValueError(f"Excepted module, not {module}")
    io = []
    for name, typ in module.type.items():
        io += [name, to_magma_type(typ)]
    if module.definition is None:
        circ = DeclareCircuit(module.name, *io)
    else:
        circ = DefineCircuit(module.name, *io)
        raise NotImplementedError()
    return circ
