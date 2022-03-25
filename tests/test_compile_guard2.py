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
