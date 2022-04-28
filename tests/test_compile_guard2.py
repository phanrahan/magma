import magma as m


def test_basic():

    class _(m.Circuit):
        with m.compile_guard2("X"):
            with m.compile_guard2("Y", "undefined"):
                inst = m.Register(m.Bit)()

        assert inst._compile_guard2s_[0].cond == "X"
        assert inst._compile_guard2s_[0].cond_type.name == "defined"
        assert inst._compile_guard2s_[1].cond == "Y"
        assert inst._compile_guard2s_[1].cond_type.name == "undefined"


def test_nested_circuit_definition():
    # This test checks that when we nest circuit definitions (usually in the
    # case of calling generators inside of definitions), we isolate their
    # compile guard stacks.

    class _Gen(m.Generator2):
        def __init__(self, n):
            T = m.Bits[n]
            self.io = m.IO(I=m.In(T), O=m.Out(T))
            with m.compile_guard2("Y"):
                self.io.O @= ~self.io.I

    class _(m.Circuit):
        with m.compile_guard2("X"):
            inst = _Gen(8)()

            # Check that the compile_guard2 invokations in this circuit and _Gen
            # stay isolated.
            assert len(inst._compile_guard2s_) == 1
            assert inst._compile_guard2s_[0].cond == "X"
            assert len(type(inst).instances[0]._compile_guard2s_) == 1
            assert type(inst).instances[0]._compile_guard2s_[0].cond == "Y"
