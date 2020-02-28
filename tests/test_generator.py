import magma as m
from magma.generator import Generator, ParamDict
from magma.testing import check_files_equal


def test_add_gen():
    class Add(Generator):
        @staticmethod
        def generate(width):
            """
            Define and return magma circuit
            """
            class AddPrim(m.Circuit):
                io = m.IO(
                    I0=m.In(m.Bits[width]),
                    I1=m.In(m.Bits[width]),
                    O=m.Out(m.Bits[width]),
                )

            class _Add(m.Circuit):
                io = m.IO(
                    I0=m.In(m.Bits[width]),
                    I1=m.In(m.Bits[width]),
                    O=m.Out(m.Bits[width]),
                )
                io.O <= AddPrim()(io.I0, io.I1)
            return _Add

    # Reference the generated circuit definition using generate method
    m.compile("build/AddGen8", Add.generate(8))
    assert check_files_equal(__file__, f"build/AddGen8.v", f"gold/AddGen8.v")

    class Top(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bits[8]),
            I1=m.In(m.Bits[8]),
            O=m.Out(m.Bits[8]),
        )

        # Define and instance circuit by instancing the generator class
        io.O <= Add(8, name='add8')(io.I0, io.I1)

    m.compile("build/AddGen8Top", Top)
    assert check_files_equal(__file__, f"build/AddGen8Top.v",
                             f"gold/AddGen8Top.v")


def test_gen_cache():
    class Add(Generator):
        @staticmethod
        def generate(params: ParamDict):
            class AddPrim(m.Circuit):
                io = m.IO(
                    I0=m.In(m.Bits[params["width"]]),
                    I1=m.In(m.Bits[params["width"]]),
                    O=m.Out(m.Bits[params["width"]]),
                )

            class _Add(m.Circuit):
                io = m.IO(
                    I0=m.In(m.Bits[params["width"]]),
                    I1=m.In(m.Bits[params["width"]]),
                    O=m.Out(m.Bits[params["width"]]),
                )
                io.O <= AddPrim()(io.I0, io.I1)
            return _Add

    assert Add.generate(ParamDict(width=8)) is Add.generate(ParamDict(width=8))

    class AddNoCache(Generator):
        cache = False

        @staticmethod
        def generate(params: ParamDict):
            class AddPrim(m.Circuit):
                io = m.IO(
                    I0=m.In(m.Bits[params["width"]]),
                    I1=m.In(m.Bits[params["width"]]),
                    O=m.Out(m.Bits[params["width"]]),
                )

            class _Add(m.Circuit):
                io = m.IO(
                    I0=m.In(m.Bits[params["width"]]),
                    I1=m.In(m.Bits[params["width"]]),
                    O=m.Out(m.Bits[params["width"]]),
                )

                io.O <= AddPrim()(io.I0, io.I1)
            return _Add

    assert AddNoCache.generate(ParamDict(width=8)) is not \
        AddNoCache.generate(ParamDict(width=8))
