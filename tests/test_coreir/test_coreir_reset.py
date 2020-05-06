import magma as m
import coreir


def _coreir_context(reset=False) -> coreir.Context:
    if reset:
        m.frontend.coreir_.ResetCoreIR()
    coreir_singleton = m.backend.coreir_.CoreIRContextSingleton()
    return coreir_singleton.get_instance()


def _compile_to_coreir(mcircuit: m.Circuit) -> coreir.Module:
    assert issubclass(mcircuit, m.Circuit)
    backend = m.frontend.coreir_.GetCoreIRBackend()
    backend.compile(mcircuit)
    cname = mcircuit.coreir_name
    return backend.modules[cname]


def _gen_circuit():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        m.wire(io.I, io.O)
    return Foo


def test_reset():
    c1 = _coreir_context(reset=False)
    c2 = _coreir_context(reset=True)
    assert c1.context != c2.context

    foo = _gen_circuit()
    cfoo = _compile_to_coreir(foo)
    assert cfoo.context == c2

    c3 = _coreir_context(reset=True)
    assert c3 != c2
    foo = _gen_circuit()
    cfoo = _compile_to_coreir(foo)
    assert cfoo.context == c3
