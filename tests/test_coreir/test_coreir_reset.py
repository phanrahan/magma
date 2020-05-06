import magma as m
import coreir

def CoreIRContext(reset=False) -> coreir.Context:
    if reset:
        m.frontend.coreir_.ResetCoreIR()
    coreir_singleton = m.backend.coreir_.CoreIRContextSingleton()
    return coreir_singleton.get_instance()

def compile_to_coreir(mcircuit: m.Circuit) -> coreir.Module:
    assert issubclass(mcircuit, m.Circuit)
    backend = m.frontend.coreir_.GetCoreIRBackend()
    backend.compile(mcircuit)
    cname = mcircuit.coreir_name
    return backend.modules[cname]

def gen_circuit():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        m.wire(io.I, io.O)
    return Foo

def test_reset():
    c1 = CoreIRContext(reset=False)
    c2 = CoreIRContext(reset=True)
    assert c1.context != c2.context

    foo = gen_circuit()
    cfoo = compile_to_coreir(foo)
    assert cfoo.context == c2

    c3 = CoreIRContext(reset=True)
    assert c3 != c2
    foo = gen_circuit()
    cfoo = compile_to_coreir(foo)
    assert cfoo.context == c3

