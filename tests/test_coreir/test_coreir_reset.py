import magma as m
import coreir


def _coreir_context(reset=False) -> coreir.Context:
    if reset:
        m.frontend.coreir_.ResetCoreIR()
    return m.backend.coreir.coreir_runtime.coreir_context()


def _compile_to_coreir(mcircuit: m.Circuit) -> coreir.Module:
    assert issubclass(mcircuit, m.Circuit)
    backend = m.frontend.coreir_.GetCoreIRBackend()
    backend.compile(mcircuit)
    return backend.get_module(mcircuit)


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
